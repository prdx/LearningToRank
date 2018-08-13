from utils.constants import Constants
from utils.text import build_query_list
import random

def build_features_bm25():
    bm25 = {}
    with open("./results/bm25.txt", "r") as bm25_res:
        lines = bm25_res.read().split("\n")
    for line in lines:
        try:
            q_id, author, doc_id, rank, score, mode = line.split()
            if q_id in bm25:
                bm25[q_id][doc_id] = score
            else:
                bm25[q_id] = {}
                bm25[q_id][doc_id] = score
        except Exception as e:
            print(e)
    return bm25

def build_qrel(qrel_data):
    """ %qrel is a hash whose keys are topic IDs and whose values are
    references to hashes.  Each referenced hash has keys which are
    doc IDs and values which are relevance values.  In other words...

    %qrel				The qrel hash.
    $qrel{$topic}			Reference to a hash for $topic.
    $qrel{$topic}->{$doc_id}	The relevance of $doc_id in $topic.
    """
    qrel = {}
    for line in qrel_data:
        q_id, author, doc_id, relevance = line.split()
        try:
            qrel[q_id][doc_id] = relevance
        except KeyError:
            qrel[q_id] = {}
            qrel[q_id][doc_id] = relevance
    return qrel

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

def build_features_okapitf():
    okapi_tf = {}
    with open("./results/okapi_tf.txt", "r") as okapi_tf_res:
        lines = okapi_tf_res.read().split("\n")
    for line in lines:
        try:
            q_id, author, doc_id, rank, score, mode = line.split()
            if q_id in okapi_tf:
                okapi_tf[q_id][doc_id] = score
            else:
                okapi_tf[q_id] = {}
                okapi_tf[q_id][doc_id] = score
        except Exception as e:
            print(e)
    return okapi_tf

def build_features_tfidf():
    tfidf = {}
    with open("./results/tfidf.txt", "r") as tfidf_res:
        lines = tfidf_res.read().split("\n")
    for line in lines:
        try:
            q_id, author, doc_id, rank, score, mode = line.split()
            if q_id in tfidf:
                tfidf[q_id][doc_id] = score
            else:
                tfidf[q_id] = {}
                tfidf[q_id][doc_id] = score
        except Exception as e:
            print(e)
    return tfidf

def build_features_laplace_unigram():
    laplace_unigram = {}
    with open("./results/laplace_unigram.txt", "r") as laplace_unigram_res:
        lines = laplace_unigram_res.read().split("\n")
    for line in lines:
        try:
            q_id, author, doc_id, rank, score, mode = line.split()
            if q_id in laplace_unigram:
                laplace_unigram[q_id][doc_id] = score
            else:
                laplace_unigram[q_id] = {}
                laplace_unigram[q_id][doc_id] = score
        except Exception as e:
            print(e)
    return laplace_unigram

def build_features_jelmer_unigram():
    jelmer_unigram = {}
    with open("./results/jelmer_unigram.txt", "r") as jelmer_unigram_res:
        lines = jelmer_unigram_res.read().split("\n")
    for line in lines:
        try:
            q_id, author, doc_id, rank, score, mode = line.split()
            if q_id in jelmer_unigram:
                jelmer_unigram[q_id][doc_id] = score
            else:
                jelmer_unigram[q_id] = {}
                jelmer_unigram[q_id][doc_id] = score
        except Exception as e:
            print(e)
    return jelmer_unigram

def build_main_dict():
    main_dict = {}
    query_list = build_query_list()
    for q_id in query_list:
        main_dict[q_id] = {}

        with open("./stored_documents.txt", "r") as docs:
            lines = docs.read().split("\n")
            lines.pop()
            for doc_id in lines:
                main_dict[q_id][doc_id] = []

    return main_dict

def build_matrix():
    matrix = build_main_dict()
    bm25 = build_features_bm25()
    okapi_tf = build_features_okapitf()
    tfidf = build_features_tfidf()
    jelmer_unigram = build_features_jelmer_unigram()
    laplace_unigram = build_features_laplace_unigram()

    qrel = read_file("./AP_DATA/qrels.adhoc.51-100.AP89.txt")
    qrel = build_qrel(qrel)

    for qid in matrix:
        for doc_id in matrix[qid]:
            print("For Q_ID: {0} and Doc_ID: {1}".format(qid, doc_id))
            matrix[qid][doc_id].append(bm25[qid][doc_id])
            matrix[qid][doc_id].append(okapi_tf[qid][doc_id])
            matrix[qid][doc_id].append(tfidf[qid][doc_id])
            matrix[qid][doc_id].append(jelmer_unigram[qid][doc_id])
            matrix[qid][doc_id].append(laplace_unigram[qid][doc_id])
            try:
                matrix[qid][doc_id].append(qrel[qid][doc_id])
            except KeyError:
                matrix[qid][doc_id].append('0')

    return matrix


matrix = build_matrix()
query_ids = set(matrix.keys())
print(len(query_ids))
train_id = random.sample(query_ids, 20)

with open("matrix_train.csv", "w") as train, open("matrix_test.csv", "w") as test:
    for q_id in matrix:
        for doc_id in matrix[q_id]:
            print(matrix[q_id][doc_id])
            string = "{0},{1},{2}\n".format(doc_id, q_id, ",".join(matrix[q_id][doc_id]))
            if q_id in train_id:
                train.write(string)
            else:
                test.write(string)
