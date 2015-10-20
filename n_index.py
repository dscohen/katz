
import os,sys,pickle
import marisa_trie
from nltk import word_tokenize

def counts_creator():
    """accepts trie, creates list of grams with occurrences > k and < k
    returns > k list, and < k list"""


def good_turing_smoothing():
    """accepts trie, calculated smoothed counts and adds them to trie"""


def build_trie():
    """accepts TREC style corpus, build trie for each doc"""
    all_grams  = get_grams(corpus,3)

    #format of storage is (uint,uint) in  byte format
    fmt = "<II"
    trie = marisa_trie.RecordTrie(fmt,all_grams.items())
    return trie

def build_all(mypath,stem=None):
    """mypath is path to where files are stored"""
    t_dict = {}
    files = [f for f in os.listdir(mypath) if isfile(join(mypath,f))]
    for fil in files:
        f = open(fil,'r')
        corpus = word_tokenize(f.read())
        if stem != None:
            corpus = stem(corpus)
        t_dict = {fil:build_trie(corpus)}
        f.close()

    with open('trie_dict.pkl','wb') as handle:
        pickle.dump(a,handle)






