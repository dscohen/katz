import argparse
import sys
import n_index

if __name__ == "__main__":
    parser = argpase.ArgumentParser()
    parser.add_argument("-a","--algorithm",choices=["katz","katz_d"],
                        required=True,help = "language model algorithm")
    parser.add_argument("-s","--stemmer",choices=["porter"],
                        default=None,help = "stemming model")
    args = parser.parse_args()
    index = n_index(sys.argv[1],args.stemmer)


    #TODO implement pitman-yor process for unigrams in katz backoff model
