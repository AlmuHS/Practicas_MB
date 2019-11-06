import read_LISA as reader
import xml.etree.ElementTree as etree

items = reader.read_file("../lisa/LISA5.627") 

root = etree.Element("add")
doc = etree.Element("doc")
root.append(doc)

field_id = etree.Element("field", fieldname="id")
field_id.text = items["id"]

field_title = etree.Element("field", fieldname="title")
field_title.text = items["title"]

field_text = etree.Element("field", fieldname="text")
field_text.text = items["text"]

doc.append(field_id)
doc.append(field_title)
doc.append(field_text)

#print(etree.tostring(root))

etree.dump(root)

