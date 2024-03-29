import re
#import write_xml as writer
import pysolr
import sys
import string
import nltk
from nltk.corpus import stopwords


'''
This function set the connection to a solr local server
'''

def solr_connection(collection):
    solr = pysolr.Solr('http://localhost:8983/solr/' + collection, auth=None)
    return solr


'''
This function parses the content of a LISA file, getting the items of each document stored in It
The function get the id, title and text of each document, and upload them to solr server
'''

def upload_lisa(filename):

    #create dictionary to store the items of each document
    items = dict();

    #the output file will have the same name than input file, adding .xml extension
    #output_file = str(filename) + ".xml"

    #if output file exists, remove its content
    output = open(output_file, "w")
    output.close()

    #open solr
    solr = solr_connection("gettingstarted")

    #open input file
    with open(filename, 'r') as LISA:
    
        '''
        This loop read entire file until find EOL
        Each iteration parses the content of a document in the file
        After parse each document, their items will be added to solr to upload to the server
        The dictionary and variables will be recycled and overwritten in each iteration of the loop
        '''

        #read file line to line
        while True:
 
            line = LISA.readline()

            '''
            Python doesn't offers any function to find the EOF in a file.
            When readline() reach EOF, It returns a empty string.
            So, we use this strategy to break the infinite loop in EOF
            '''

            #if line is EOF, finish the loop
            if(not line.strip()):
                break

            #get id (latest word in the line)
            line = line.split(" ")           
            id = line[-1].rstrip()

            #store id in dictionary
            items["id"] = id
            print("id: " + id)
            
            '''
            This block read the title field of the document. 
            The title field is a couple of lines, followed by a blank line
            To get the content of this field, we read lines until find a blank line, which mark the end of this block
            Each line is added to "title" string, previously initialized as a empty string
            To fill all the title in a only line, we replace end of line (EOL) with spaces
            '''

            #Initialize title as empty string          
            title = ""
            
            #Read a line
            line = LISA.readline()

            #read lines until find blank line
            while(line.strip()):
                #add the new line to the title string
                title += line

                #read a new line
                line = LISA.readline()
                

            #store title in dictionary, replacing EOL with spaces
            items["title"] = title.replace("\n", " ")
            print("title: " + items["title"])


            '''
            This block read the text field of the document. 
            The text field is a couple of lines, followed with a line filled entirely with * sign
            To get the content of text field, we read line to line, until find a line which match with the pattern
            The pattern is described as a regular expression
            The content of each line is added to text string, previously initialized to empty string
            To fill all text in a only line, we replace EOL with spaces         
            '''

            #read a line
            line = LISA.readline()

            #initialize text as empty string
            text = ""

            #read lines until the line match with the end regex
            while(re.match("^\*+$", line) == None):
                text += line     
                line = LISA.readline()
                        
            #stores text in dictionary
            items["text"] = text.replace('\n', " ").replace("\r", " ")
            print("text: " + items["text"])

            #upload docs to solr
            solr.add([items])

            #call to write_xml function, which fills all items in a xml structure, and write It to output_file
            #writer.write_xml(items, output_file)


'''
This function execute a query, defined as a string using solr syntax 
(http://www.solrtutorial.com/solr-query-syntax.html), over a solr local server.
The function returns the results of this query, as a dictionary
'''

def execute_query(query):

    #set connection to solr local server
    solr = solr_connection("gettingstarted")

    '''
    This line execute the query, defined as a string, over the solr server
    The results includes score field, and will be sortered from highest score to lowest score

    https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html

    This call return the results in JSON, as a dictionary
    '''

    #execute query over the server, adding score field to the results, and sort them using score 
    results = solr.search(query, **{'fl':'*,score', 'rows':'50', 'sort': 'score desc'})

    '''
    #print results, separated by a blank line
    for doc in results:
        print(doc)
        print("\n")
    '''

    #return results in a dictionary
    return results

'''
This function parses the content of a query files, where each query is written in natural language.
The function filter the most important words of each query, and send the query to solr local server
The results of each query are written to a file using TREC format, as trec_top_file
'''
def query_batch(filename, output_file):

    '''
    This list includes the stop words which will be considered irrelevant to the query
    The list not only includes single words, and includes some complex expressions too
    This stop words will be removed of the query before send It to solr
    '''

    #download stopwords list from nltk
    nltk.download('stopwords')                
    stop_words = list(stopwords.words('english'))

    #convert all stopwords to upper
    stop_words = [word.upper() for word in stop_words]    

    #add more stopwords
    stop_words += ["DOING","I", "AM", "INTERESTED IN","ALSO INTERESTED", "INTERESTED", "AVAILABLE", "TOPIC", "MORE INTERESTED", "INFORMATION", \
                "MY", "AT", "TO","DO", "OF", "ON", "CURRENTLY", "BOTH", "ALSO", "PAPERS", "PAPER", "DESCRIBING","TYPE", "ESPECIALLY", "LOOKING", "MAY",\
                 "FOR INSTANCE", "INSTANCE", "RECEIVE INFORMATION", "I AM CURRENTLY ENGAGED", "WILL", "INCLUDE", "BE", "SHOULD", "INTEND", "SEND",\
                 "WOULD", "RECEIVE", "GRATEFUL", "BE PLEASED TO", "PLEASED", "WOULD BE PLEASED", "THERE HAS", "THEIR", "USING", "NOT", "JUST",\
                  "INFORMATION ABOUT", "DISSERTATION IS", "DISSERTATION", "GIVING", "ANY", "CONCERNS", "SUCH AS", "WITH", "DISSERTATION", "DONE",\
                    "TO RECEIVE", "ALMOST", "ANYTHING", "TO DO WITH", "TO DO", "PROVISION", "E.G.", "CONCERNED", "THIS", "INTEREST", "COULD",\
                    "ELSEWHERE","ETC.", "ETC", "AND", "OR", "THE", "BOTH", "ANY", "EITHER", "LIKE", "ITSELF", "I.E.", "INCLUDING", "RESULTS",\
                     "IE","FOR", "FROM", "WHETHER", "EG", "REFERS", "STUDYING", "PARTICULARLY", "VARIOUS", "TYPES", "RELATED", "INVOLVES", \
                     "STUDIES", "PURPOSES", "PURPOSE"]

    #open query input file, and trec output file
    with open(filename, 'r') as lisa_query, open(output_file, 'w') as output:
        
        '''
        This loop parses the query file, filtering the most important keywords of each query document,
        and sending then to solr.

        Each iteration parses a query document, send the filtered query to solr, and write the results to a file,
        in trec_top_file format
        '''
        #read entire file and split in queries using # delimiter
        queries_list = lisa_query.read().split(' #')

        #read list to process and send each query
        for doc_counter, query in enumerate(queries_list[0:-1]):
                #remove all EOL of the query
                query = query.rstrip()

                #remove punctuation marks of the query
                query = query.translate(str.maketrans('', '', string.punctuation))

                #split the query in words
                query_words = query.split()
                filtered_query = ""
            
                #print query ID
                print(query_words[0] + "\t")

                #print(query_words)

                #create a new filtered_query removing stopwords
                for word in query_words[2:]:
                    if word not in stop_words:
                        filtered_query += f'{word} '

                print(filtered_query + "\n\n")

                '''
                Send filtered query to solr, and write results to a file
                '''
                #send query to solr, searching coincidences in text
                results = execute_query("text:" + filtered_query) 
                
                #write each result to output_file, using trec format
                for ranking,document in enumerate(results):
                    #if document["score"] > 0.5:
                    output.write(f'{doc_counter+1} Q0 {document["id"]} {ranking+1} {document["score"]} almuhs \n')                
                        
            

'''
This function parses the content of LISARJ.NUM file, and generate a file in trec_rel_format.
The function receives LISARJ.NUM as input, and generate trec_rel_file as output

LISARJ.NUM has the next structure:
QUERY_ID [LIST OF RELEVANTS DOCUMENTS]

LISARJ.NUM shows the results sorted by query ID.

trec_rel_file has different structure:
query 0 document relevant[1/0]
'''

def gen_trec_rel(in_file, out_file):
    
    #open files
    with open(in_file, 'r') as input, open(out_file, 'w') as output:

        '''
        To distinct a query from another, we will check the first word of each line,
        using a query_counter to remember the current query ID.

        If the first word has the value of query_counter+1, It means this line is refered to the next query
        In other case, this line has more relevant documents of current query
        '''
        
        #initialize query_counter to first query
        query_counter = 1

        '''        
        To store the relevant documents of each query, we will use a dictionary of lists, indexed by query ID
        Each dictionary position has a list with the ID of the relevants documents of its query
        '''

        #create and initialize structures
        rel_docs = dict()
        all_docs = []
        rel_docs[1] = []


        '''
        Read file line to line.
        If first word of the line correspond with query_counter, add the rest of fields to the list of its position
        If this word is query_counter+1, initialize a new position in the dictionary, adding the fields to new position
        In other case, add the fields to the list of the current query 
        '''
        for line in input:
    
            #split the line in words
            fields = line.split()
            #num_docs = fields[1]

            #add documents of current query, excluding query ID
            if fields[0] == str(query_counter):
                rel_docs[query_counter] += fields[2:len(fields)]

            #add documents of next query, excluding query ID
            elif fields[0] == str(query_counter+1):
                query_counter += 1
                rel_docs[query_counter] = []
                rel_docs[query_counter] += fields[2:len(fields)]

            #add more documents of current query
            else:
                rel_docs[query_counter] += fields[0:len(fields)]

        '''
        Get all documents stored in Solr and add them to a dictionary
        '''
        solr = solr_connection("gettingstarted")
        all_docs = solr.search("*", **{'rows':'10000', 'sort': 'id asc'})

        '''
        Write results in trec_rel_file format
        
        For each query and each document, indicates if the document is relevant or not
        '''

        last_doc = 0

        for doc in all_docs:
            if int(doc['id']) > last_doc:
                last_doc = int(doc['id'])

        #last_doc = all_docs.docs[len(all_docs)-1]["id"]

        print(last_doc)

        for ref in rel_docs:		
            for id in range(1,last_doc+1):
                #generate string
                line = f'{ref} 0 {id} '
                
                if str(id) in rel_docs[ref]:
                    line += "1"
                else:
                    line += "0"

                #write new string to output_file
                output.write(line + "\n")                   

        #print lists
        print(rel_docs)
        print("\n\n")
        print(len(all_docs))

                        
'''
This function removes all documents stored in local solr server
'''

def delete_all():
    solr = solr_connection("gettingstarted")
    solr.delete(q='*:*')

                                    	
def main_menu():

    if(len(sys.argv) < 2):
        print("It needs two parameters")

    elif(str(sys.argv[1]) == 'add'):
        path = str(sys.argv[2])

        if(not "LISA" in path):
            print("Error: this is not a LISA file")
        else:
            upload_lisa(path)

    elif(str(sys.argv[1]) == 'query'):
        query = str(sys.argv[2])
        execute_query(query)

    elif(str(sys.argv[1]) == 'query_batch'):
        input_path = str(sys.argv[2])
        output_path = str(sys.argv[3])
        query_batch(input_path, output_path)

    elif(str(sys.argv[1]) == 'trec_eval'):
        input_path = str(sys.argv[2])
        output_path = str(sys.argv[3])
        gen_trec_rel(input_path, output_path)

    elif(str(sys.argv[1]) == 'delete_all'):
        delete_all()

    elif(len(sys.argv) > 1):
        print("The options available are:\n \
            query \"string\" - Execute a query over the collection \n \
            add [path] - Add a new LISA file from the path indicated by parameter \n \
            query_batch [input_path] [output_path] - Execute a set of query from input file indicated by input_path, storing the results in output_path\n \
            trec_eval [input_path] [output_path] - Parses LISARJ.NUM file, stored the items in trec_rel_file format\n \
            delete_all - Delete all documents indexed by Solr\n \
        ")



if __name__ == '__main__':        
    main_menu()


