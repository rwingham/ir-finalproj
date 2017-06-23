#!/usr/bin/env python

qrel_files = ["q1-rels.txt","q2-rels.txt","q3-rels.txt","q4-rels.txt","q5-rels.txt"]
gold = "ehealth_2013_task3/training/qrels.clef2013ehealth.1-5-train.bin.txt"

def get_qrels(query):
    qrels = {}
    with open(query, "r") as f:
        i = 1
        for line in f.readlines():
            line = line.split(",")
            #seems backwards; will be flipped back around
            #in compare_to_gold
            qrels[line[0][1:]] = i
            i += 1
    return(qrels)

#this creates a dict 
#with numbers as keys and values
#ranking:relevant y/n
def compare_to_gold(query_num, qrels):
    with open(gold, "r") as f:
        judgments = {}
        for line in f.readlines():
            line = line.split(" ")
            if int(line[0]) == query_num:
                page = line[2]
                if page in qrels.keys():
                    judgments[qrels[page]] = line[3] 
    #if not mentioned, assume irrelevant
    for k, v in qrels.items():
        if v not in judgments.keys():
            judgments[v] = 0
    return judgments

def mean(numbers):
    return float(sum(numbers)/len(numbers))

#rels a list of binary relevances i.e. 1 or 0
def precision(rels):
    retrieved = float(len(rels))
    relevant = float(rels.count(1))
    return relevant/retrieved

def p_at_k(judgments,k):
    rels = []
    if k == 1:
        rels.append(judgments[1])
    for i in range(1,k):
        rels.append(judgments[i])
    return(precision(rels))

#the main function, pulls it all together
def show_all(query,query_num):
    qrels = get_qrels(query)
    print("Results for query {}".format(query_num))
    judgments = compare_to_gold(query_num,qrels)
    print(judgments)
    print("---p@k results---")
    p_results = {}
    for i in range(1,20):
        p_results[i] = p_at_k(judgments,i)
        print("p@{} : {} ".format(i,p_results[i]))
    print("---MAP---")
    print(mean(p_results.values()))

if __name__ == '__main__':
    show_all("q1-rels.txt",1)
    show_all("q2-rels.txt",2)
    show_all("q3-rels.txt",3)
    show_all("q4-rels.txt",4)
    show_all("q5-rels.txt",5)
