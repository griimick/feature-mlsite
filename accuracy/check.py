from app import parser
import xml.etree.ElementTree
import sys
import json

# log output to a file
# f = open("test.out", 'w')
# sys.stdout = f

# Parsing XML Data
file = open("accuracy/data.txt", "w")
root = xml.etree.ElementTree.parse('accuracy/dataset/dataset.xml').getroot()

# Preparing dataset, one in a text file and second in a List
# Format of Dataset List 
# ['1', 'सुस्पष्ट और विस्तृत इन्टरफेस है।', {'term': 'इन्टरफेस', 'to': '28', 'from': '20', 'polarity': 'pos'}]

dataset = []
for child in root:
    child_split = child.attrib['id'].split('_')
    if(child_split[0]=='spe'):
        sentence_number = child_split[1]
        sentence_text = child[0].text
        if(len(child)>1):
            sentence_aspectTerms = child[1]
            # droppping out unnecessary attributes from dataset
            del sentence_aspectTerms[0].attrib['to']
            del sentence_aspectTerms[0].attrib['from'] 
            file.write(str.join(" ", (sentence_number, sentence_text, str(sentence_aspectTerms[0].attrib), "\n")))
            dataset.append([sentence_number, sentence_text, sentence_aspectTerms[0].attrib])
        else:
            file.write(str.join(" ", (sentence_number, sentence_text, "\n")))
            dataset.append([sentence_number, sentence_text])
file.close()
# List out the error features and sentiments
errFeature = []
errSentiment = []


# query = "इस फ़िल्म की कहानी कमज़ोर नहीं है, गीत मधुर हैं पर निर्देशन बहुत बुरा नहीं है।"
# print(query)
# parsedOutput, scoreList, namesList, relationList = parser.parseText(query)
# polarityFeature,scores = parser.featurePolarity(scoreList, namesList, relationList, parsedOutput)
# print(polarityFeature)

# Dataset loop will start here
# query = "इस फ़िल्म की कहानी कमज़ोर नहीं है, गीत मधुर हैं पर निर्देशन बहुत बुरा है।"
count = 0
countParsed = 0
true = 0
falsePolarity = 0
falseParse = 0
falseSentiments = {} #{feat:"", line:""}
falseFeatures = {} #{sent:"", freq:""}
for data in dataset:
    print(data)
    query = data[1]
    parsedOutput, scoreList, namesList, relationList = parser.parseText(query)
    polarityFeature,scores = parser.featurePolarity(scoreList, namesList, relationList, parsedOutput)
    print(polarityFeature)
    for parsedInput in data[2:]:
        for parsedOutput in polarityFeature:
            if(parsedInput["term"] == parsedOutput["term"]):
                countParsed = countParsed + 1
                if(parsedInput['polarity'] == (parsedOutput['polarity'])):
                    true = true + 1
                    print("TRUE")
                    break
                else:
                    falsePolarity = falsePolarity + 1
                    parser.appendFalse(parsedOutput['sent'], falseSentiments)
                break
    count = count+1
    print("--------------------------------------------------------------")
    print("count: ", count, " countParsed: ", countParsed, " true: ", true)
    print("Parsed Polarity Accuracy: ", true/count)
    print("Parsing Accuracy: ", countParsed/count) 
    print("--------------------------------------------------------------")
    print("False Sentiments")
    print(falseSentiments)
    print("\n")
falseSentiments["Parsed Polarity Accuracy"] = true/count
falseSentiments["Parsing Accuracy"] =  countParsed/count
with open('accuracy/result.json', 'w') as fp:
    json.dump(falseSentiments,fp)



