import re
import write_xml as writer
import pysolr
import sys
import string

'''
This function parses the content of a LISA file, getting the items of each document stored in It
The function get the id, title and text of each document, and upload them to solr server
'''

def solr_connection(collection):
    solr = pysolr.Solr('http://localhost:8983/solr/' + collection, auth=None)
    return solr


def parse_file(filename):

    #create dictionary to store the items of each document
    items = dict();

    #the output file will have the same name than input file, adding .xml extension
    output_file = str(filename) + ".xml"

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


def execute_query(query):
    solr = solr_connection("gettingstarted")
    results = solr.search(query, **{'fl':'*,score', 'rows':200})

    for doc in results:
        print(doc)
        print("\n")

    return results


def query_batch(filename, output_file):

    stop_words = ["I", "AM", "INTERESTED IN","ALSO INTERESTED",  "MORE INTERESTED", \
                 "INTERESTED", "FOR INSTANCE", "INSTANCE", "RECEIVE INFORMATION", "ALSO",
                 "WOULD", "BE", "RECEIVE", "GRATEFUL", "BE PLEASED TO", "PLEASED", \
                  "INFORMATION ABOUT", "MY DISSERTATION IS", "GIVING" "ANY", "I AM DOING" "CONCERNS", "SUCH AS", \
                    "TO RECEIVE", "ALMOST", "ANYTHING", "TO DO WITH", "TO DO", "PROVISION", "E.G.", "CONCERNED", \
                     "ETC", "THE", "OF", "AND", "OR"]
                    

    with open(filename, 'r') as lisa_query, open(output_file, 'w') as output:

        doc_counter = 0
        
        while True:

            line = lisa_query.readline();
    
            #if line is EOF, finish the loop
            if(not line.strip()):
                break     
        
            id = line.split(" ")[0].rstrip();

            print(id)

            text = ""
            line = lisa_query.readline()
            
            while(re.match("^.*\.*#$", line) == None):
                text += line
                line = lisa_query.readline()

            text += line.replace(". #", "")
            text = text.replace("\n", " ")
           
            text = text.translate(str.maketrans('', '', string.punctuation))

            for word in stop_words:
                text = text.replace(word + " ", "")
            
            print(text)
            results = execute_query("text: " + text)

            doc_counter += 1

            for document in results:
                output.write(str(doc_counter) + "\t" + "Q0\t" + str(document["id"]) + "\t" + str(document["score"]) + "\n")
                                    	

def main_menu():

    if(len(sys.argv) < 2):
        print("It needs two parameters")

    elif(str(sys.argv[1]) == 'add'):
        path = str(sys.argv[2])

        if(not "LISA" in path):
            print("Error: this is not a LISA file")
        else:
            parse_file(path)

    elif(str(sys.argv[1]) == 'query'):
        query = str(sys.argv[2])
        execute_query(query)

    elif(str(sys.argv[1]) == 'query_batch'):
        input_path = str(sys.argv[2])
        output_path = str(sys.argv[3])
        query_batch(input_path, output_path)

    elif(len(sys.argv) > 1):
        print("The options available are:\n \
            query \"string\" - Execute a query over the collection \n \
            add path - Add a new LISA file from the path indicated by parameter")



if __name__ == '__main__':        
    main_menu()

