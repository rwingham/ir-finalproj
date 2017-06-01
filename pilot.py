#!/usr/bin/env python

import gzip
import timeit
from json import loads

clef = "/l2/corpora/clef/ehealth_2013_task3.tgz"


#https://stackoverflow.com/questions/15707056/get-time-of-execution-of-a-block-of-code-in-python-2-7
#answer 1
start_time = timeit.default_timer()

with gzip.open(clef, "rb") as data:
    i = 0
    js = 0
    njs = 0
    with open("tinycorpus.json", "w") as out:
        for thing in data:
            i += 1
        #print(i)
            try:
                thing = thing.strip()
                item = loads(thing.decode("utf-8"))
            #print(item)
                js += 1
                out.write(thing)
            except:
                print(thing)
                njs += 1
            if i % 10000 == 0:
                print("\n")
                print("************Read {} items!***************".format(i))
                print("JSON items: {}".format(js))
                print("Non-JSON items: {}".format(njs))
                print("Time elapsed: {}".format(timeit.default_timer() - start_time))
            if js > 1000:
                print("Found enough JSONs for a tiny corpus!")
                exit()

