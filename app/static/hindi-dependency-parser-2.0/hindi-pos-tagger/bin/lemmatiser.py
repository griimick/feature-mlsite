#!/usr/bin/env python
'''
Usage: python lemmatiser.pl lemmaFile < input > output

The input should have two colums
<html>
word1	tag1
word2	tag2
.
'''

import sys
import re

lemmaDict= {}  # word : { pos : lemma}
def loadLemmatiser(file):
    for line in open(file):
        line=line.strip()
        word= line.split('\t')[0]
        tags= line.split('\t')[1:]
        if word not in lemmaDict:
            lemmaDict[word]= {}
        for t in tags:
            (tag, lemma)= t.split(' ')
            if tag in lemmaDict[word]:
                continue
            if lemma.strip()!="":
                lemmaDict[word][tag]= lemma

def lemmatise(f):
    for line in f:
        line= line.strip()
        if line=="":
            print(line)
        elif line[0]=='<':
            print(line)
        else:
            #line.sub("\t+")
            cols= line.split()
            if len(cols)!=2:
                #print cols
                print(line)
            else:
                if cols[0] in lemmaDict and cols[1] in lemmaDict[cols[0]]:
                    print("%s\t%s" %(line, lemmaDict[cols[0]][cols[1]]))
                else:
                    print("%s\t%s" %(line, cols[0]+"."))
            
loadLemmatiser(sys.argv[1])
lemmatise(sys.stdin)
