from app import parser
import xml.etree.ElementTree
import sys
import json
import os
file = open("accuracy/data.txt", "w")
root = xml.etree.ElementTree.parse('accuracy/dataset/dataset.xml').getroot()

# Preparing dataset, one in a text file and second in a List
# Format of Dataset List 
# ['1', 'सुस्पष्ट और विस्तृत इन्टरफेस है।', {'term': 'इन्टरफेस', 'to': '28', 'from': '20', 'polarity': 'pos'}]

dataset = []
fields = []
for child in root:
    child_split = child.attrib['id'].split('_')
    if(child_split[0] not in fields):
    	fields.append(child_split[0])

print(fields)