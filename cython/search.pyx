import n_index.ngrams as ngrams
import sys
import katz


def get_q():
    f = open(sys.argv[1])
    queries = []
    for line in f:
        q = line.split("\t")
        queries.append([q[0],q[1]])
    return queries


def query(expr,k,d_trie):
    terms = ngrams(expr,3,3)
    #might not be needed for the for loop
    find_scores(d_trie,terms,k)


def find_scores(d_trie,terms,k):
    """
    d_trie = dictonary of tries, terms = trigrams of q
    """
    results = []
    #key is all docs stored in trie
    for key in d_trie.keys():
        #calculate katz score for all of them
        results.append([key,sum([katz.katz(term,d_trie[key][0],k) for term in terms])])
    #TODO sort then return


def run_queries():
    queries = get_q()
    evals = []
    for q in queries:
        #run the desc through katz, which returns a ranked list of top results
        #Add it to a dict and then store it later
        evals[q[0]] = query(q[1])

