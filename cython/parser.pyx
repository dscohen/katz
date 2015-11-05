import os
import sys
import re
import codecs
from lxml import etree
import nltk.data



def process_element(elem1,elem2):
    docno = elem1.text
    text = elem2.text
    return (docno,text)


def parse(infile):
    pat = re.compile("<.*>")
    results = []
    f = codecs.open(infile, "r",encoding="utf-8")
    info = []
    intext = False
    for line in f:
        if "<docno>" in line:
            docno = (line[7:-9])
        if "</text>" in line:
            intext = False
            results.append((docno," ".join(info)))
            info = []
        # if pat.match(line) and "<text>" not in line:
        #     continue
        if intext:
            info.append(line)
        if "<text>" in line:
            intext = True
    return results

