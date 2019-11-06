import xml.etree.ElementTree as etree

root = etree.Element("add")
doc = etree.Element("doc")
root.append(doc)

field_id = etree.Element("field", fieldname="id")
field_id.text = "1"

field_title = etree.Element("field", fieldname="title")
field_title.text = "This is the title"

field_text = etree.Element("field", fieldname="text")
field_text.text = "This is the text"

doc.append(field_id)
doc.append(field_title)
doc.append(field_text)

#print(etree.tostring(root))

etree.dump(root)

