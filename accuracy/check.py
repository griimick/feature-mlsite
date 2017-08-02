import xml.etree.ElementTree

# Parsing XML Data
file = open("data.txt", "w")
root = xml.etree.ElementTree.parse('dataset/dataset.xml').getroot()
dataset = {}
for child in root:
	child_split = child.attrib['id'].split('_')
	if(child_split[0]=='app'):
		sentence_number = child_split[1]
		sentence_text = child[0].text
		if(len(child)>1):
			sentence_aspectTerms = child[1] 
			file.write(str.join(" ", (sentence_number, sentence_text, str(sentence_aspectTerms[0].attrib), "\n")))
		else:
			file.write(str.join(" ", (sentence_number, sentence_text, "\n")))
file.close()
		