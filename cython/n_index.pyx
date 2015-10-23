

import os,sys,pickle
import marisa_trie
import nltk
import parser
import gt_smoothing as gt

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
        """mypath is path to where files are stored"""
        t_dict = {}
        files = [f for f in os.listdir(mypath) if os.path.isfile(mypath+f)]
        for fil in files:
            doc_text = parser.parse(mypath+fil)
            for docno,text in doc_text:
                print "running ",docno
                corpus = nltk.word_tokenize(text)
                if stem != None:
                    corpus = stem(corpus)
                t_dict = {docno:self._build_trie(corpus,k)}
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


    def _get_grams(self,corpus,k):
        """accepts tokenized corpus, returns dict of file:{(gram:(count),katz_counts)}"""
        bgs = nltk.bigrams(corpus)
        tgs = nltk.trigrams(corpus)
        ugs = corpus
        bgc,tgc,ugc = map(nltk.FreqDist,[bgs,tgs,ugs])
        bgd, tgd, ugd = map(gt.simpleGoodTuringProbs,[bgc,tgc,ugc])
        #time efficient hash combining
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
        nk.append(counts[1])
        nk.append(counts.get(k+1,0))
        return nk







