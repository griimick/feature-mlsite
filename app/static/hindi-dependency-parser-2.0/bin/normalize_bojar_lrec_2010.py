#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

vowels_to_be_replaced= {}

def replace_null(from_chr_num, to_chr_num):
    for x in range(from_chr_num, to_chr_num):
        vowels_to_be_replaced[chr(x)]= ""

#replace_null(0x0900, 0x0904)
#replace_null(0x093A, 0x0950)
#replace_null(0x0951, 0x0958)
#replace_null(0x0962, 0x0964)
#replace_null(0x0971, 0x0972)

vowels_to_be_replaced[b'0x0901']= b'0x0902'
vowels_to_be_replaced[""]= "न"
vowels_to_be_replaced["ऩ"]= "न"
vowels_to_be_replaced['ऱ']= "र"
vowels_to_be_replaced['ऴ']= "ळ"
vowels_to_be_replaced['क़']= "क"
vowels_to_be_replaced['ख़']= "ख"
vowels_to_be_replaced['ग़']= "ग"
vowels_to_be_replaced['ज़']= "ज"
vowels_to_be_replaced['ड़']= "ड"
vowels_to_be_replaced['ढ़']= "ढ"
vowels_to_be_replaced['फ़']= "फ"
vowels_to_be_replaced['य़']= "य"
vowels_to_be_replaced['ॠ']= "ऋ"
vowels_to_be_replaced['ॡ']= "ऌ"

def normalise(word):
    # Word should be unicode encoding
    nword=""
    for char in word:
        if char in vowels_to_be_replaced:
            nword+= vowels_to_be_replaced[char]
        else:
            nword+= char
    return nword

if __name__=="__main__":
    print((normalise("भागता")))
    print((normalise("तृष्णा")))            
