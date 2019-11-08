import re
import write_xml as writer


def read_file(name):
    items = dict();
    output_file = str(name) + ".xml"

    with open(name, 'r') as LISA:
    
        while True:
 
            line = ""
            line = LISA.readline()

            if(not line.strip()):
                break

            line = line.split(" ")           

            id = line[len(line)-1].rstrip()

            items["id"] = id
            print("id: " + id)

            title = ""
            line = "."
            
            while(line.strip()):
                line = LISA.readline()
                title += line

            items["title"] = title.replace("\n", " ")
            print("title: " + title)

            line = LISA.readline()
            text = ""

            while(re.match("^\*+$", line) == None):
                line = LISA.readline()

                if(re.match("^\*+$", line) == None):
                    text += line 

            items["text"] = text.replace("\n", " ")
            print("text: " + text)

            parser.write_xml(items, output_file)



#items = read_file("../lisa/LISA5.627") 
#print(items["text"])
read_file("../lisa/LISA0.001") 


