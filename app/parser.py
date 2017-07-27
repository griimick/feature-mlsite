import os
import subprocess
import codecs
import networkx as nx

def parseText(query):

    features = []
    sentiments = []
    sentList = {}
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

    #hello
    upload_dir = "app/tmp/"
    if not os.path.exists(upload_dir+"hindi.input.txt"):
        open(upload_dir+"hindi.input.txt", 'w')
    file_text=codecs.open(upload_dir+"hindi.input.txt","w","utf8")
    print(query)
    file_text.write(query)
    file_text.close()

    file3=codecs.open(upload_dir+"hindi.input.txt","r","utf8")
    lines3=file3.readlines()
    file3.close()

    for l in lines3:
        print(l)

    os.chdir("app/static/hindi-dependency-parser-2.0")
    make_process = subprocess.Popen("make", shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out,err = make_process.communicate()
    print(out)
    print(err)
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


    for p in lines:
        print(p)

    for line in lines:
        parsedArray = line.split()
        if (len(parsedArray) >= 4):
            parsedOutput.append(parsedArray)
            selfNodes.append(parsedArray[0])
            linkNodes.append(parsedArray[4])
            if (parsedArray[3] == "NN" or parsedArray[3] == "NNP"):
                features.append(parsedArray[0])
            elif (parsedArray[3] == "JJ"):
                sentiments.append(parsedArray[0])
            elif (parsedArray[3] == "INTF"):
                catalysts.append(parsedArray[0])
            elif (parsedArray[3] == "NEG"):
                negatives.append(parsedArray[0])

    for node1, node2 in zip(selfNodes, linkNodes):
        edges.append((node1,node2))

    #print(edges)

    #HSWN.txt to dictionary
    for line in lines2:
        parsedArray = line.split()
        words = parsedArray[4].split(",")
        for word in words:
            if (word.find("_")>-1):
                word = word.split("_")[0]
            sentList[word] = [parsedArray[2], parsedArray[3]]

    for feature in features:
        featureNames.append(parsedOutput[int(feature)-1][1])

    for sentiment in sentiments:
        sentimentNames.append(parsedOutput[int(sentiment)-1][1])

    for catalyst in catalysts:
        catalystNames.append(parsedOutput[int(catalyst)-1][1])

    for neg in negatives:
        negativeNames.append(parsedOutput[int(neg)-1][1])

    #Construct Graph
    G = nx.Graph()
    G.add_nodes_from(selfNodes)
    G.add_edges_from(edges)
    spl = nx.all_pairs_shortest_path_length(G)

    #Feature and Sentiment Relation
    tempL = []
    featureSent = []
    negSent = []
    catSent = []

    for sentiment in sentiments:
        for feature in features:
            tempL.append(spl[sentiment][feature])
        featureSent.append((int(sentiment), int(features[tempL.index(min(tempL))])))
        tempL.clear()


    for neg in negatives:
        for sentiment in sentiments:
                tempL.append(spl[neg][sentiment])
        negSent.append((int(neg), int(sentiments[tempL.index(min(tempL))])))
        tempL.clear()
    print(negSent)

    for cat in catalysts:
        for sentiment in sentiments:
                tempL.append(spl[cat][sentiment])
        catSent.append((int(cat), int(sentiments[tempL.index(min(tempL))])))
        tempL.clear()
    print(catSent)


    #for (x,y) in featureSent:
        #print(parsedOutput[int(x)-1][1],parsedOutput[int(y)-1][1])
    

    return parsedOutput, featureNames, sentimentNames, catalystNames, negativeNames, featureSent, sentList, negSent, catSent