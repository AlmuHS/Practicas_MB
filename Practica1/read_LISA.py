import re

def read_file(name):
    with open(name, 'r') as LISA:
        number = LISA.readline().split(" ")[1].rstrip()
        print("number: " + number)

        title = ""
        line = "."
        while(line[0] != " "):
            line = LISA.readline().replace("\n", " ")
            title += line

        print("title: " + title)

        line = LISA.readline()
        text = ""

        while(re.match("^\*+$", line) == None):
            line = LISA.readline()

            if(re.match("^\*+$", line) == None):
                text += line.replace("\n", " ") 

        print("text: " + text)



read_file("../lisa/LISA5.627") 

