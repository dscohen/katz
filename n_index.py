
import os,sys,pickle
import marisa_trie
from nltk import word_tokenize,bigrams
import parser

class Index:
    def __init__(self,mypath,stem,corpus_smoothing):
        #if no trie index has been created, create then load it
        #TODO REad flags from stem and use correct one
        if 'trie_dict.pkl' not in os.listdir(mypath):
            self._build_all(mypath,stem)
        self.trie = pickle.load(open(mypath,"rb"))

    # def backoff(self,front=0,back=0):

    # def get_count(self,gram):
    #     return self.trie[gram][0]

    # def get_gt_count(self,gram)
    def backoff(gram,front=0,back=0):
        """
        properly subdivide a ngram to either back off from the front or the back (for alpha lookup)
        """
        gram = gram.split(" ")
        return gram[front:(len(gram-back))]


    def _build_all(mypath,stem):
        """mypath is path to where files are stored"""
        t_dict = {}
        files = [f for f in os.listdir(mypath) if isfile(join(mypath,f))]
        for fil in files:
            doc_text = parser.parse(fil)
            for docno,text in doct_text:
                corpus = word_tokenize(text)
                if stem != None:
                    corpus = stem(corpus)
                t_dict = {docno:_build_trie(corpus)}
        with open('trie_dict.pkl','wb') as handle:
            pickle.dump(t_dict,handle)

    def _build_trie():
        """accepts robust style corpus, build trie for each doc"""
        all_grams,k_counts  = _get_grams(corpus,3)

        #format of storage is (uint,uint) in  byte format
        fmt = "<II"
        trie = marisa_trie.RecordTrie(fmt,all_grams.items())
        return (trie,k_counts)

    def _get_grams(corpus,k):
        """accepts tokenized corpus, returns dict of file:{(gram:(count),katz_counts)}"""
        bgs = nltk.bigrams(corpus)
        tgs = nltk.trigrams(corpus)
        ugs = corpus
        bgc,tgc,ugc = map(nltk.FreqDist,[bgs,tgs,ugs])
        bgd, tgd, ugd = map(good_turing_smoothing,[bgc,tgc,ugc])
        #time efficient hash combining
        final_dict = dict(bgd, **tgd)
        final_dict.update(ugd)

        #get nk+1 and n1 counts for each gram for katz mode
        nks = map(_get_nk_counts,[ugc,bgc,tgc])
        return final_dict,nks

    def _get_nk_counts(self,bg):
        """
        accepts tokens, returns tuple of [# with k+1 frequency,# with 1 frequency]
        """
        nk = []
        counts = gt.countOfCountsTable(bg)
        nk.append[counts[1]]
        nk.append[counts[k+1]]
        return nk







