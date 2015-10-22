import os
import sys
import re
from lxml import etree
import nltk.data

def fast_iter(context, func):
    results = []
    for event, elem in context:
        if elem.tag == 'DOCNO':
            elem_d = elem
        if elem.tag == 'TEXT':
            elem_t = elem
            results.append(func(elem_d,elem_t))
            elem.clear
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
    del context
    return results

def process_element(elem1,elem2,model):
    docno = elem1.text
    text = elem2.text
    return (docno,text)


def parse(fil):
    context = etree.iterparse(infile)
    result = fast_iter(context, process_element)
    return result
