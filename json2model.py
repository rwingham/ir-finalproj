#!/usr/bin/env python

import tarfile
import nltk
import json
from re import sub
from collections import defaultdict
from math import log

from bigram import NgramModel

clef = "/l2/corpora/clef/ehealth_2013_task3.tgz"

stemmer = nltk.SnowballStemmer("english")
tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
stops = nltk.corpus.stopwords.words("english")

def is_ascii(foo):
    try:
        foo.decode('ascii')
        return True
    except:
        return False

class ScrapedPage:
    def __init__(self, txt, title, unique_id, verbose = False):
        self.verbose = verbose
        self.title = title #webpage title 
        self.unique_id = unique_id #unique identifier from dataset
        self.txt = self.preprocess(txt)
        #using bigram model because texts are too small
        #for anything much larger, I think
        self.model = NgramModel(self.txt,2)
        if verbose:
            print("Model trained.")

    def preprocess(self,raw):
        if self.verbose:
            print("Preprocessing text...")
        sents = []
        raw = str(raw)
        raw = sub("\<[^\<]*\>","",raw) #get rid of all HTML tags
#https://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
        raw = filter(lambda x: is_ascii(x),raw) #otherwise tokenizer chokes
        raw = nltk.tokenize.sent_tokenize(raw)
        for sentence in raw:
            sentence = filter(lambda x: x.isalpha() or x == " ", sentence)
            sentence = tokenizer.tokenize(sentence)
            new_sent = []
            for word in sentence:
                word = word.lower()
                word = stemmer.stem(word)
            #nb: not robust to queries consisting only of stopwords
            #while this is a problem in general IR,
            #I don't think it's applicable to this corpus
                if word not in stops:
                    if len(word) < 25: #sanity check; trying to sort out long concatenated code bits 
                        new_sent.append(word)
            sents.append(new_sent)
        if self.verbose:
            print("Text processed.")
            print("Processed text: {}".format(sents))
        return(sents)

    def print_out(self):
        words = " ".join(self.txt)
        print(words)

    def perplex(self,query):
        query = self.preprocess(query)
        print(query)
        return(self.model.perplexity(query))

