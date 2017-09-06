from app import parser
import xml.etree.ElementTree
import sys
import json
import os

def check(field):
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
        if(child_split[0]==field):
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
    output = {}
    stats = {}
    for data in dataset:
        print(data)
        query = data[1]
        parsedOutput, scoreList, namesList, relationList = parser.parseText(query)
        polarityFeature,scores = parser.featurePolarity(scoreList, namesList, relationList, parsedOutput)
        print(polarityFeature)
        for parsedInput in data[2:]:
            for parsedOutput in polarityFeature:
                if(parsedInput['term'] == parsedOutput['term']):
                    countParsed = countParsed + 1
                    if(parsedInput['polarity'] == (parsedOutput['polarity'])):
                        true = true + 1
                        print("TRUE")
                        dataTemp = [query, parsedOutput]
                        output[data[0]] = dataTemp
                        break
                    else:
                        falsePolarity = falsePolarity + 1
                        parser.appendFalse(query, parsedOutput['sent'], falseSentiments)
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

    stats["Total Sentences"] = count
    stats["Correct Parsed"] = countParsed
    stats["Correct Parsed and Polarity"] = true
    stats["Parsed Polarity Accuracy"] = true/count
    stats["Parsing Accuracy"] =  countParsed/count
    # with open('accuracy/result.json', 'w') as fp:
    #     json.dump(falseSentiments,fp)

    # home_dir = os.getcwd()

    resultFile = 'accuracy/output/'+field+'/result.json'
    os.makedirs(os.path.dirname(resultFile), exist_ok=True)
    with open(resultFile, 'w', encoding='utf8') as json_file:
        data = json.dumps(falseSentiments, ensure_ascii=False, indent=4)
        # unicode(data) auto-decodes data to unicode if str
        json_file.write(data)
        print("result.json")

    outputFile = 'accuracy/output/'+field+'/output.json'
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)
    with open(outputFile, 'w', encoding='utf8') as json_file:
        data = json.dumps(output, ensure_ascii=False, indent=4)
        # unicode(data) auto-decodes data to unicode if str
        json_file.write(data)
        print("output.json printed")

    statsFile = 'accuracy/output/'+field+'/stats.json'
    os.makedirs(os.path.dirname(statsFile), exist_ok=True)
    with open(statsFile, 'w', encoding='utf8') as json_file:
        data = json.dumps(stats, ensure_ascii=False, indent=4)
        # unicode(data) auto-decodes data to unicode if str
        json_file.write(data)
        print("stats.json printed")

    return stats


# fields = ['app', 'cam', 'hea', 'hom', 'lap', 'mob', 'mov', 'sma', 'spe', 'tab', 'tra', 'tel']
fields = ['mov', 'mob']
dataStats = {}
trueTotal = 0
countParsedTotal = 0
countTotal = 0
for field in fields:
    fieldStats = check(field)
    countTotal = countTotal + fieldStats["Total Sentences"]
    countParsedTotal = countParsedTotal + fieldStats["Correct Parsed"]
    trueTotal = trueTotal + fieldStats["Correct Parsed and Polarity"]
    dataStats[field] = fieldStats

dataStats["Total Sentences"] = countTotal
dataStats["Correct Parsed"] = countParsedTotal
dataStats["Correct Parsed and Polarity"] = trueTotal
dataStats["Parsed Polarity Accuracy"] = trueTotal/countTotal
dataStats["Parsing Accuracy"] =  countParsedTotal/countTotal

statsTotalFile = 'accuracy/output/statsTotal.json'
os.makedirs(os.path.dirname(statsTotalFile), exist_ok=True)
with open(statsTotalFile, 'w', encoding='utf8') as json_file:
    data = json.dumps(dataStats, ensure_ascii=False, indent=4)
    # unicode(data) auto-decodes data to unicode if str
    json_file.write(data)
    print("stats.json printed")

