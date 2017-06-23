#!/usr/bin/env python

from json2model import ScrapedPage
import json
import tarfile
from sys import argv
import cPickle as pickle

clef = "/l2/corpora/clef/ehealth_2013_task3.tgz"

#a generator that yields a dict with the raw page
def extract_pages(address,src):
    print("Extracting page data.")
    pages = src.extractfile(address)
    page_dict = {}
    page_text = ""
    for line in pages.readlines():
        if line[:4] == "#UID":
            #if we've pulled text, yield the dict
            if 'uid' in page_dict.keys() and len(page_text) > 0:
                print("Found a new entry, {}.".format(line).strip())
                page_dict['body'] = page_text
                print("Got data from page {}.".format(page_dict['uid']))
                #print("Beginning of body: {}".format(page_dict['body'][:100]))
                yield(page_dict)
                #and make a new one to keep going
                page_dict = {}
                page_dict['uid'] = line[4:].strip()
                page_text = ""
            else: #first time
                print("Found the first entry, {}".format(line))
                page_dict['uid'] = line[4:].strip()
        elif line[:4] == "#URL":
            page_dict['title'] = line[4:]
        #these lines don't have info we keep
        elif line[:4] in ["#DAT","#CON"]:
            continue
        else:
            if len(line) > 0:
            #append line to our running scrape of the page
                page_text = page_text + "\n" + line
    else:
        print("Got data from final entry, {}.".format(page_dict['uid']))
        page_dict['body'] = page_text
        yield(page_dict)

def pull_pages(address,src,out):
    i = 0
    print("Loaded {}".format(address))
    for page in extract_pages(address,src):
        modeled_page = ScrapedPage(page['body'],page['title'],page['uid'])
        if len(modeled_page.txt) > 0:
            pickle.dump(modeled_page,out)
            i += 1
        # if i % 100 == 0:
            print("Written out {} models from {}.".format(i,address))
    if i > 0:
        print("Wrote out a total of {} models from {}".format(i,address))

#deprecated command line interface
#lots of files so we'll read them from a txt file instead
"""
if len(argv) < 2:
    print("Too few arguments!")
    print("Usage: please pass me the name of the file or files I'm scraping.")
    exit()
#reads one file address
#to do more, call with a bash script
in_file = argv[1]

if len(argv) > 2:
    num_files_to_read = argv[2]
"""

list_file = "dat_files.txt"

to_read = []
with open(list_file, "r") as f:
    for line in f.readlines():
        to_read.append(line.strip())

out_file = "trained_models.ScrapedPage.p"
with tarfile.open(clef, "r:gz") as src:
    with open(out_file, "a") as out:
        for dat_file in to_read:
            print("Reading from {}".format(dat_file))
            pull_pages(dat_file,src,out)


