import xml.etree.ElementTree as etree

def write_xml(items, output_file):
	file = open(output_file, 'a+')

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

	string = etree.tostring(root).decode("utf-8")
	string = string.replace("field fieldname", "fieldname")

	#string = etree.dump(root)

	#et = etree.ElementTree(root)
	#et.write(output_file)
	file.write(str(string)+"\n")
