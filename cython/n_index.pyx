import re
import string

import os,sys,pickle
import marisa_trie
import nltk
import parser
import gt_smoothing as gt
import spacy
from collections import defaultdict




class Index:
    def __init__(self,mypath,stem,corpus_smoothing):
        #if no trie index has been created, create then load it
        #TODO REad flags from stem and use correct one
        self.k = 5
        k = 5
        if 'trie_dict.pkl' not in os.listdir("./"):
            self._build_all(mypath,stem,k)
        self.trie = pickle.load(open('trie_dict.pkl',"rb"))

    # def backoff(self,front=0,back=0):

    # def get_count(self,gram):
    #     return self.trie[gram][0]

    # def get_gt_count(self,gram)
    def _build_all(self,mypath,stem,k):
        f = open("./stemmer/stopword.txt")
        stop_list = f.read().split("\n")
        stop = list(string.punctuation) + stop_list
        f.close()
        """mypath is path to where files are stored"""
        t_dict = {}
        files = [f for f in os.listdir(mypath) if os.path.isfile(mypath+f)]
        print files
        for fil in files:
            print fil
            if "trie_"+fil+".pkl" in os.listdir("./"):
                continue
            doc_text = parser.parse(mypath+fil)
            i = 0
            for docno,text in doc_text:
                print docno
                #stop words using stemmed method"
                corpus = [i for i in nltk.word_tokenize(text) if i not in stop]
                t_dict[docno] = self._build_trie(corpus,k)
            with open('trie_'+fil+'.pkl','wb') as handle:
                pickle.dump(t_dict,handle)
        with open('trie_dict.pkl','wb') as handle:
            pickle.dump(t_dict,handle)

    def _build_trie(self,corpus,k):
        """accepts robust style corpus, build trie for each doc"""
        all_grams,k_counts  = self._get_grams(corpus,k)

        #format of storage is (uint,uint) in  byte format
        fmt = "<ff"
        keys = map(unicode,all_grams.keys())
        vals = all_grams.values()
        trie = marisa_trie.RecordTrie(fmt,zip(keys,vals))
        return (trie,k_counts)

    def _combine(self,dol1,dol2):
        for k1 in dol1.keys():
            dol1[k1] = (dol1[k1],dol2[k1])
        return dol1


    def _freqs(self,corps):
        print corps
        d = defaultdict(int)
        for word in corps:
            d[word] += 1
        return d

    def _get_grams(self,corpus,k):
        """accepts tokenized corpus, returns dict of file:{(gram:(count),katz_counts)}"""
        bgc = ngrams(corpus,2,2)
        tgc = ngrams(corpus,3,3)
        ugc = ngrams(corpus,1,1)
        bgd, tgd, ugd = map(gt.simpleGoodTuringProbs,[bgc,tgc,ugc])
        gt_dict1 = dict(bgd, **tgd)
        gt_dict1.update(ugd)
        ct_dict2 = dict(bgc, **tgc)
        ct_dict2.update(ugc)
        final_dict = self._combine(ct_dict2,gt_dict1)

        #get nk+1 and n1 counts for each gram for katz mode
        nks = map(self._get_nk_counts,[ugc,bgc,tgc])
        return final_dict,nks

    def _get_nk_counts(self,bg):
        k = self.k
        """
        accepts tokens, returns tuple of [# with k+1 frequency,# with 1 frequency]
        """
        nk = []
        counts = gt.countOfCountsTable(bg)
        if len(counts.values()) == 0:
            print "No counts for nk"
            return [0,0]
        nk.append(counts[1])
        nk.append(counts.get(k+1,0))
        return nk



def ngrams(tokens, int MIN_N, int MAX_N):
    cdef Py_ssize_t i, j, n_tokens

    count = defaultdict(int)

    join_spaces = " ".join

    n_tokens = len(tokens)
    for i in xrange(n_tokens):
        for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
            count[join_spaces(tokens[i:j])] += 1

    return count




