#!/usr/bin/env python

#some parts of implementation (entropy, perplexity) heavily based on: 
#http://www.nltk.org/_modules/nltk/model/ngram.html#NgramModel
#which has been removed from current branches of nltk
#this is a bit less flexible as it's just made for my purposes with bigrams

#expect preprocessing was done outside these models.

from collections import defaultdict
from math import log

class NgramModel:

    def __init__(self,txt,n):
        self.txt = txt #list of sentences as lists
        self.n = n
        self.total = 0 #fill as words counted
        self.model = defaultdict(int)
        self.get_counts()
        self.add1 = -(log(1) - log(self.total)) #for words not found

    def get_counts(self):
        for sentence in self.txt:
            self.total += len(sentence)
            if self.n > 1:
                sentence = ["<s>" * (self.n - 1)] + sentence + ["<e>" * (self.n - 1)]
            for i in range(self.n-1, len(sentence)):
                ngram = " ".join(sentence[i:i+self.n])
                self.model[ngram] += 1
            #normalize and convert to negative log space
        for k,v in self.model.items():
            self.model[k] = -(log(v) - log(self.total))

        #based on nltk.models.NgramModel.logprob
    def prob(self,word):
        if word in self.model.keys():
            return(self.model[word])
        else:
            return(self.add1)

        #based on nltk.models.NgramModel.entropy
    def entropy(self,test):
        e = 0.0
        if self.n > 1:
            test = ["<s>" * (self.n - 1)] + test + ["<e>" * (self.n - 1)]
        for i in range (self.n-1,len(test)):
            ngram = " ".join(test[i:i+self.n])
            e += self.prob(ngram)
        return e / float(len(test) - (self.n - 1))

        #based on nltk.models.NgramModel.perplexity
    def perplexity(self,test):
        return pow(2.0, self.entropy(test))
    
if __name__ == '__main__':
    print("Testing bigram model.")
    test_corpus = [["this", "first", "test", "sentence"],["this", "second","test","sentence"],["this","test","sentence"]]
    test_model = NgramModel(test_corpus,2)
    print("Log-probabilities on tiny test corpus:")
    for k,v in test_model.model.items():
        print(k,v)
    print("Perplexity on test sentences:")
    print("this first test")
    print(test_model.perplexity(["this","first","test"]))
    print("this test sentence")
    print(test_model.perplexity(["this","test","sentence"]))
    print("this test flamingo")
    print(test_model.perplexity(["this","test","flamingo"]))
    print("flamingo macadamia nuts")
    print(test_model.perplexity(["flamingo","macadamia","nuts"]))
    print("this longer second test sentence flamingo test sentence")
    print(test_model.perplexity(["this","longer","second","test","sentence","flamingo","test","sentence"]))
