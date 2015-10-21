
import os,sys,pickle
import marisa_trie
from nltk import word_tokenize,bigrams
from collections import Counter

class Index:
    def __init__(self,mypath,stem=None):
        #if no trie index has been created, create then load it
        if 'trie_dict.pkl' not in os.listdir(mypath):
            self.build_all(mypath,stem)
        self.trie = pickle.load(open(mypath,"rb"))

    def build_all(mypath,stem):
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
            pickle.dump(t_dict,handle)

    def get_grams(corpus,k):
        """accepts tokenized corpus, returns dict of gram:(count)"""
        bgs = nltk.bigrams(corpus)
        tgs = nltk.trigrams(corpus)
        ugs = corpus
        bgc,tgc,ugc = map(nltk.FreqDist,[bgs,tgs,ugs])
        bgd, tgd, ugd = map(good_turing_smoothing,[bgc,tgc,ugc])
        #time efficient hash combining
        final_dict = dict(bgd, **tgd)
        final_dict.update(ugd)

        #get nk+1 and n1 counts for each gram for katz mode
        nks = map(get_nk_counts,[ugc,bgc,tgc])
        return final_dict,nks

    def build_trie():
        """accepts TREC style corpus, build trie for each doc"""
        all_grams,k_counts  = get_grams(corpus,3)

        #format of storage is (uint,uint) in  byte format
        fmt = "<II"
        trie = marisa_trie.RecordTrie(fmt,all_grams.items())
        return trie

    def get_nk_counts(self,bg):
        nk = []
        counts = gt.countOfCountsTable(bg)
        nk.append[counts[1]]
        nk.append[counts[k+1]]
        return nk







