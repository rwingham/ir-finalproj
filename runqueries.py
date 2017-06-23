#!/usr/bin/env python

from json2model import ScrapedPage
from bigram import NgramModel
import pickle

class Query:

    def __init__(self,txt,qname,verbose=False):
        self.txt = txt #text to be searched
        self.qname = qname #which query it is
        self.top_n = 20 #return a sorted list of the top n results
        self.results = [] #list of 2tuples (uid,perplexity)
        self.verbose = verbose

    def judge_relevance(self,page):
        perplexity = page.model.perplexity(self.txt)
        qrel = (page.unique_id,perplexity)
        if len(self.results) < self.top_n:
            if self.verbose:
                print("Filling initial list.")
            self.results.append(qrel)
            self.results = sorted(self.results, key = lambda x: x[1])
        elif perplexity < self.results[-1][1]:
            if self.verbose:
                print("Found better contender {}".format(page.unique_id))
            if qrel not in self.results: #exclude duplicates
                self.results.append(qrel)
                self.results = sorted(self.results,key = lambda x: x[1])[:self.top_n]
        else: #it's worse than what we have
            pass


    def print_top_n(self):
        for (a,b) in self.results:
            print("Unique ID {} with perplexity {}".format(a,b))

    def write_results(self):
        filename = self.qname + "-rels.txt"
        with open(filename,"w") as f:
            f.write(self.qname)
            for (a,b) in self.results:
                line = str(a) + ", " + str(b)
                f.write(line)
                f.write("\n")

    def load(self,source):
        pass

           

#answer 2:
#https://stackoverflow.com/questions/20716812/saving-and-loading-multiple-objects-in-pickle-file
def load_models(data):
    while True:
        try:
            yield pickle.load(data)
        except EOFError:
            print("Reached end of models in this file.")
            break
        except (ImportError, IndexError,KeyError,TypeError):
            print("Excluding outdated model and continuing.")
            continue

if __name__ == '__main__':
    query1 = Query(["crohns disease"],"q1", verbose = True)
    query2 = Query(["metastases of adrenals and pain and pain treatment"],"q2", verbose = True)
    query3 = Query(["radial neck fracture and healing time"],"q3", verbose = True)
    query4 = Query(["cdiff"], "q4", verbose = True)
    query5 = Query(["group b streptococcus and treatment and renal"],"q5", verbose = True)
    queries = [query1, query2, query3, query4, query5]
    saved_data = ["trained_models.12.ScrapedPage.p", "trained_models.ScrapedPage.p"]
    for data in saved_data:
        with open(data, "r") as d:
            print("Now checking models from {}.".format(data))
            i = 0
            for model in load_models(d):
                for query in queries:
                    query.judge_relevance(model)
                    i += 1
                if i % 1000 == 0:
                    print("Compared to {} models from {}.".format(i,data))
                if i % 100000 == 0:   
                    for query in queries:
                        query.print_top_n()
                        query.write_results()
            for query in queries:
                query.print_top_n()
                query.write_results()
