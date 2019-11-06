import re
import parse_xml as parser


def read_file(name):
    items = dict();
    output_file = str(name) + ".xml"

    with open(name, 'r') as LISA:
        id = LISA.readline().split(" ")[1].rstrip()
        items["id"] = id
        #print("number: " + number)

        title = ""
        line = "."
        while(line[0] != " "):
            line = LISA.readline().replace("\n", " ")
            title += line

        items["title"] = title
        #print("title: " + title)

        line = LISA.readline()
        text = ""

        while(re.match("^\*+$", line) == None):
            line = LISA.readline()

            if(re.match("^\*+$", line) == None):
                text += line.replace("\n", " ") 

        items["text"] = text
        #print("text: " + text)

        parser.write_xml(items, output_file)

#items = read_file("../lisa/LISA5.627") 
#print(items["text"])
read_file("../lisa/LISA5.627") 


