from scipy import linalg
from numpy import c_, exp, log, inf, NaN, sqrt

def katz(q,trie,doc,k,good_turing_prob):
    q_count,d_count = freq(q,doc,n)
    #calculate P if freq is above k
    if q_count > k:
        return p_sample(q,trie)
    else:
        #backoff to mgram 2..m
        return alpha(q)*katz(q[1:],trie,doc,k)


    #TODO, i don't like syntax erros so placeholder




    #beta is 1 - katz_prob of of all w_i 
def alpha(trie,w_m1):
    #return beta function + sum of all samples with w_1^m greater than k
    #p_ample, trie(w[1:]) applies good turing smoothing to all counts greater than k
    #note, since alha calculated P_s from w_2^m

    alph_counts = [w[1:] for w in lk_counts]
    return beta(len( w ))/ (1 - sum(map(p_sample,alph_counts)))

def p_sample(w,trie):
    """accepts w = ngram and trie, returns P_s according to katz model"""
    #first element stored true count, second element stores gt smoothed count

    return (trie[w][1]/trie[w][0]) * trie[w][0]/trie[w[:-1]][0]
