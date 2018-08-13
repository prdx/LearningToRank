from bs4 import BeautifulSoup
import os
from utils.constants import Constants
from utils.es import *
from utils.text import *

data_collection = []

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
            data = data.split("\n")
            data.pop()
            return data
    except Exception as e:
        print(e)
        raise IOError

def build_qrel(qrel_data):
    qrel_doc_list = set()
    for line in qrel_data:
        q_id, author, doc_id, relevance = line.split()
        qrel_doc_list.add(doc_id)
    return qrel_doc_list

if es.ping():
    # Delete already existing index
    delete_index()

    # Create initial index
    create_index()
    qrels = "./AP_DATA/qrels.adhoc.51-100.AP89.txt"

    qrel = read_file(qrels)
    print((len(qrel)))
    qrel_doc_list = build_qrel(qrel)
    print((len(qrel_doc_list)))
    found = set()
    not_found = set()
    doc_indexed = set()
    # Go through all of the corpus and store it
    for f in os.listdir(Constants.DATA_PATH):
        if f.startswith('ap'):
            with open(Constants.DATA_PATH + f, 'r') as d:
                d = d.read()
                docs = find_docs_by_regex(d)

                print(("Processing {0}, with {1} docs".format(f, len(docs))))

                for doc in docs:
                    doc_id = find_doc_no_by_regex(doc)
                    if doc_id not in qrel_doc_list:
                        not_found.add(doc_id)
                        continue
                    text = find_all_texts_by_regex(doc)
                    text = text.strip()
                    # doc_length = len(text.split(' '))
                    # if text != '':
                        # print "Empty doc found: {0}".format(doc_id)
                        # break

                    store_document(doc_id, text)
                    found.add(doc_id)

    doc_indexed.update(found)
    MAX_EXTRA_DATA = 25000
    counter = 0

    # Add extra 1000 documents per query
    for f in os.listdir(Constants.DATA_PATH):
        if f.startswith('ap'):
            with open(Constants.DATA_PATH + f, 'r') as d:
                d = d.read()
                docs = find_docs_by_regex(d)

                print(("Processing {0}, with {1} docs".format(f, len(docs)))) 

                for doc in docs:
                    if counter == MAX_EXTRA_DATA:
                        break
                    doc_id = find_doc_no_by_regex(doc)
                    if doc_id not in not_found:
                        continue
                    text = find_all_texts_by_regex(doc)
                    text = text.strip()
                    # doc_length = len(text.split(' '))
                    # if text != '':
                        # print "Empty doc found: {0}".format(doc_id)
                        # break

                    store_document(doc_id, text)
                    doc_indexed.add(doc_id)
                    counter += 1

    print(len(doc_indexed))
    with open("./stored_documents.txt", "w") as sd:
        for doc in doc_indexed:
            sd.write(doc + "\n")
