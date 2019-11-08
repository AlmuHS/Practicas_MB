import re
import write_xml as writer


'''
This function parses the content of a LISA file, getting the items of each document stored in It
The function get the id, title and text of each document, and send them to write_xml function to generate XML file
'''

def parse_file(filename):
    items = dict();
    output_file = str(filename) + ".xml"

    #open input file
    with open(filename, 'r') as LISA:
    
        #read file line to line
        while True:
 
            line = LISA.readline()

            #if line is EOF, finish the loop 
            if(not line.strip()):
                break

            #get id (latest word in the line)
            line = line.split(" ")           
            id = line[len(line)-1].rstrip()

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
            print("title: " + title)


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
            print("text: " + text)


            #call to write_xml function, which fills all items in a xml structure, and write It to output_file
            writer.write_xml(items, output_file)



#items = read_file("../lisa/LISA5.627") 
#print(items["text"])
parse_file("../lisa/LISA3.001") 


