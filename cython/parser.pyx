import os
import sys
import re
from lxml import etree
import nltk.data



def process_element(elem1,elem2):
    docno = elem1.text
    text = elem2.text
    return (docno,text)


def parse(infile):
    results = []
    f = open(infile)
    info = []
    intext = False
    for line in f:
        if "<DOCNO>" in line:
            docno = (line[7:-8])
        if "<TEXT>" in line:
            info.append(line[6:])
            intext = True
        if "</TEXT>" in line:
            info.append(line[:-7])
            intext = False
            results.append((docno," ".join(info)))
            info = []
        if intext:
            info.append(line)
    return results

