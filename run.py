import argparse
import sys
import n_index

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--algorithm",choices=["katz","katz_d"],
                        required=True,help = "language model algorithm")
    parser.add_argument("-f","--file",
                        default=None,help = "stemming model")
    parser.add_argument("-s","--stemmer",choices=["porter"],
                        required=False,default=None,help = "stemming model")
    args = parser.parse_args()
    index = n_index.Index(args.file,args.stemmer,None)


    #TODO implement pitman-yor process for unigrams in katz backoff model
