from scipy import linalg
from numpy import c_, exp, log, inf, NaN, sqrt

def katz(q,trie,doc,k,good_turing_prob):
    count = trie[w][0]
    #calculate P if freq is above k
    if q_count > 0:
        return p_sample(q,trie)
    else:
        #backoff to mgram 2..m
        return alpha(q)*katz(backoff(q,front=1),trie,doc,k)






    #beta is 1 - katz_prob of of all w_i 
def alpha(trie,w_m1):
    #return beta function + sum of all samples with w_1^m greater than k
    #p_ample, trie(w[1:]) applies good turing smoothing to all counts greater than k
    #note, since alpha calculated P_s from w_2^m
    #using katz model in 1987 paper

    #all grams that are less than k in the corpus
    beta = probs(trie,backoff(w_m1,back=1),k)
    alpha = probs(trie,backoff(w_m1,front=1,back=1),k)
    return beta/alpha

def probs(trie,w,k):
    """
    Recieves w and trie, computes sum of all probabilities > 0, used for alpha and beta values
    """
    #TODO do I need unicode lookup for this?
    #w[1][0] is real counts
    min = len(w)
    #retrieve all grams that have w_m1 as prefix, and ignore w_m1 itself
    grams = [g[0] for g in trie.items(w) if (g[1][0] > 0 and len(g[0] != min))]
    return 1 - sum(map(p_sample,grams))


def p_sample(w,trie,nk):
    """accepts w = ngram and trie, returns P_s according to katz model"""

    w_1 = backoff(w,back=1)
    w_count = trie[w][0]
    w_gt_count = trie[w][1]
    dr = 1
    if w_count <= k:
        eq = ((k+1)(nk[1]))/nk[0]
        dr = (w_gt_count/w_count - eq)/(1-eq)
    return dr*w_count/trie[w_1][0]

