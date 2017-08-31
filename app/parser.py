import os
import subprocess
import codecs
import networkx as nx
import time
def appendFalse(sentence, term, dictionary):
    if term in dictionary:
        dictionary[term].append(sentence)
    else:
        dictionary[term] = [sentence]

def getNames(words, parsedOutput):
    wordNames= []
    for word in words:
        wordNames.append(parsedOutput[int(word)-1][1])
    return wordNames

def getName(word, parsedOutput):
    return parsedOutput[int(word)-1][1]

def getRelation(network, aList, bList):
    tempL = []
    abRelation = []
    try:
        for aWord in aList:
            for bWord in bList:
                tempL.append(network[aWord][bWord])
            abRelation.append((int(aWord), int(bList[tempL.index(min(tempL))])))
            tempL.clear()
    except ValueError:
        print("ValueError at getRelation")
    
    return abRelation

def formatScore(score):
    if(score[1]>score[0]):
        score[0] = -1 * score[1]
    return score

def polarityScore(score):
    if(score[0]==0):
        score[1] = 0
    elif(score[0]>0):
        score[1] = 1
    else:
        score[1] = -1
    return score

def typeScore(score, placeholder):
    score[1] = float(placeholder)
    return score

def polarityFromScore(score):
    if score>0:
        return "pos"
    elif score<0:
        return "neg"
    else:
        return "neu"
def printRealtion(relation,parsedOutput):
    print(parsedOutput[realtion[0]-1][1],"---",parsedOutput[relation[1]-1][1])

def parseText(query):
    print("Parsing...", end=" ")
    start = time.process_time()
    # Variables to be used for parsing different components afterwards
    features = []
    sentiments = []
    scoreList = {}
    selfNodes = []
    linkNodes = []
    edges = []
    parsedOutput = []
    featureNames = []
    sentimentNames = []
    catalystNames = []
    catalysts = []
    negativeNames = []
    negatives = []

    # Parser uses file system for parsing
    upload_dir = "app/tmp/"
    if not os.path.exists(upload_dir+"hindi.input.txt"):
        open(upload_dir+"hindi.input.txt", 'w')
    file_text=codecs.open(upload_dir+"hindi.input.txt","w","utf8")
    # print(query)
    file_text.write(query)
    file_text.close()

    file3=codecs.open(upload_dir+"hindi.input.txt","r","utf8")
    lines3=file3.readlines()
    file3.close()

    # Subprocess that needs python and JAVA to start parsing the  hindi.input.txt file
    os.chdir("app/static/hindi-dependency-parser-2.0")
    make_process = subprocess.Popen("make", shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out,err = make_process.communicate()
    # print(out)
    # print(err)
    # print("make file complete")
    make_process.wait() #wait for process to end

    file2 = codecs.open("HSWN.txt", "r", "utf8")
    lines2 = file2.readlines()
    file2.close()

    os.chdir("../../..")

    file1=codecs.open(upload_dir+"hindi.output","r","utf8")
    lines=file1.readlines()
    file1.close()
    os.remove(upload_dir+"hindi.output")

    for line in lines:
        parsedArray = line.split()
        if (len(parsedArray) >= 4):
            parsedOutput.append(parsedArray)
            

    for word in parsedOutput:
        if(word[5]=="mod"):
            temp = parsedOutput[int(word[4])-1]
            # print(temp)
            temp[1] = " ".join((word[1],temp[1])) 
            temp[2] = " ".join((word[2],temp[2]))
            parsedOutput[int(word[4])-1] = temp
            # parsedOutput.pop(int(word[0])-1)

    for word in parsedOutput:
        if(word[5] != "mod"):
            if (word[3] == "NN" or word[3] == "NNP"):
                features.append(word[0])
            elif (word[3] == "JJ"):
                sentiments.append(word[0])
            elif (word[3] == "INTF"):
                catalysts.append(word[0])
            elif (word[3] == "NEG"):
                negatives.append(word[0])          
            selfNodes.append(word[0])
            linkNodes.append(word[4])

    # print(parsedOutput)
    for node1, node2 in zip(selfNodes, linkNodes):
        edges.append((node1,node2))

    #print(edges)

    #HSWN.txt to dictionary named sentList
    for line in lines2:
        parsedArray = line.split()
        words = parsedArray[4].split(",")
        for word in words:
            if (word.find("_")>-1):
                word = word.split("_")[0]
            scoreList[word] = [parsedArray[2], parsedArray[3]]

    # for feature in features:
    #     featureName = getName(feature, parsedOutput)
    #     if featureName in scoreList:
    #         sentiments.append(feature)
    #         features.remove(feature)

    featureNames = getNames(features, parsedOutput)
    sentimentNames = getNames(sentiments, parsedOutput)
    catalystNames = getNames(catalysts, parsedOutput)
    negativeNames = getNames(negatives, parsedOutput)

    # print(selfNodes)
    # print(linkNodes)
    # print(edges)

    #Construct Graph
    G = nx.Graph()
    G.add_nodes_from(selfNodes)
    G.add_edges_from(edges)
    spl = nx.all_pairs_shortest_path_length(G)

    #Feature and Sentiment Relation
    sentFeature = getRelation(spl, sentiments, features)
    negSent = getRelation(spl, negatives, sentiments)
    catSent = getRelation(spl, catalysts, sentiments)
    
    relationList = [sentFeature, negSent, catSent]
    namesList = [featureNames, sentimentNames, catalystNames, negativeNames]

    print(time.process_time()-start, "secs")
    return parsedOutput, scoreList, namesList, relationList

def featurePolarity(scoreList, namesList, relationList, parsedOutput):
    start = time.process_time()
    print("Calculating...", end=" ")
    sentimentNames = namesList[1]
    catalystNames = namesList[2]

    sentFeature = relationList[0]
    negSent = relationList[1]
    catSent = relationList[2]

    scores={}
    polarityFeature=[]
    for sentiment in sentimentNames:
        if sentiment in scoreList:
            scores[sentiment]=formatScore([float(i) for i in scoreList[sentiment]])
            # scores[sentiment]=polarityScore(scores[sentiment])
            scores[sentiment]=typeScore(scores[sentiment], 2)
        else:
            scores[sentiment] = [0.0, 2]
    for catalyst in catalystNames:
        if catalyst in scoreList:
            scores[catalyst]=formatScore([float(i) for i in scoreList[catalyst]])
            # scores[catalyst]=polarityScore(scores[catalyst])
            scores[catalyst]=typeScore(scores[catalyst], 3)
            # print(scores[catalyst])
        else:
            scores[catalyst]= [0.0, 3]
    # print(parsedOutput)
    # print(sentFeature)
    tempScore = 0.0
   
    for sentiment in sentFeature:
        tempDict = {}
        tempScore = 0.0
        tempFeature = parsedOutput[sentiment[1]-1][1]
        tempDict["term"] = tempFeature
        tempSentiment = parsedOutput[sentiment[0]-1][1]
        tempDict["sent"] = tempSentiment
        print(tempDict["sent"])
        tempScore += scores[tempSentiment][0]
        print(tempScore)
        for catalyst in catSent:
            if(catalyst[1] == sentiment[0]):
                tempCatalyst = parsedOutput[catalyst[0]-1][1]
                tempDict["cat"]=tempCatalyst
                tempScore += scores[tempCatalyst][0]
        print("after catalyst score:", tempScore)
        for neg in negSent:
            if(neg[1] == sentiment[0]):
                tempScore *= -1
                tempNeg = parsedOutput[neg[0]-1][1]
                tempDict["neg"] = tempNeg
        print("after negation score:", tempScore)
        tempDict["score"] = tempScore
        tempDict["polarity"] = polarityFromScore(tempScore)
        polarityFeature.append(dict(tempDict))
    
    print(time.process_time()-start, "secs")
    return polarityFeature,scores