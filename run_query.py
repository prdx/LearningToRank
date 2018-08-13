from models.es_built_in_model import BuiltInModel
from models.okapi_tf_model import OkapiTFModel
from models.tf_idf_model import TFIDFModel
from models.okapi_bm25 import OkapiBM25
from models.laplace_unigram_lm_model import LaplaceUnigramLMModel
from models.jelinekmercer_unigram_lm_model import JelinekMercerUnigramLMModel
from models.pseudo_relevance_feedback_model import PseudoRelevanceFeedbackModel 
from utils.constants import Constants
from utils.es import get_term_statistics
from utils.statistics import DocumentStatistics
from utils.text import build_query_list, get_stopwords, get_file_list, write_output
import sys
import os
import threading
import numpy as np

document_statistics = {}
tf_for_queries = {}
wfd_collection = {}
total_tf_wd = {}
query_list = {}
total_length = 0

def run_built_in():
    print("Processing: built in model")
    built_in = BuiltInModel()
    for key in query_list:
        results = built_in.query(query_list[key])['hits']['hits']
        rank = 1
        write_output(
                model = 'es',
                query_no = str(key),
                doc_no = result['_id'],
                rank = str(rank),
                score = str(result['_score']))
        rank += 1

def run_okapi_tf():
    print("Processing: Okapi TF model")
    okapi_tf = OkapiTFModel(document_statistics)
    for q_no in query_list:
        query = query_list[q_no]
        results = okapi_tf.query(query, tf_for_queries[q_no])
        rank = 1
        for key, value in sorted(iter(results.items()), key=lambda k_v: (k_v[1],k_v[0]), reverse=True):
            # if rank > Constants.MAX_OUTPUT:
                # break
            write_output(
                    model = 'okapi_tf',
                    query_no = str(q_no),
                    doc_no = str(key),
                    rank = str(rank),
                    score = str(value))
            rank += 1
    print("Okapi TF Done")

def run_tf_idf():
    print("Processing: TF-IDF model")
    tfidf = TFIDFModel(document_statistics)
    for q_no in query_list:
        query = query_list[q_no]
        results = tfidf.query(query, wfd_collection, tf_for_queries[q_no])
        rank = 1
        for key, value in sorted(iter(results.items()), key=lambda k_v1: (k_v1[1],k_v1[0]), reverse=True):
            # if rank > Constants.MAX_OUTPUT:
                # break
            write_output(
                    model = 'tfidf',
                    query_no = str(q_no),
                    doc_no = str(key),
                    rank = str(rank),
                    score = str(value))
            rank += 1
    print("TF-IDF Done")

def run_bm25():
    print("Processing: Okapi BM25 model")
    bm25 = OkapiBM25(document_statistics)
    for q_no in query_list:
        query = query_list[q_no]
        results = bm25.query(query, wfd_collection, tf_for_queries[q_no])
        rank = 1
        for key, value in sorted(iter(results.items()), key=lambda k_v2: (k_v2[1],k_v2[0]), reverse=True):
            # if rank > Constants.MAX_OUTPUT or value <= 0:
                # break
            write_output(
                    model = 'bm25',
                    query_no = str(q_no),
                    doc_no = str(key),
                    rank = str(rank),
                    score = str(value))
            rank += 1
    print("BM25 Done")

def run_laplace_unigram():
    print("Processing: Unigram LM with Laplace model")
    laplace_unigram = LaplaceUnigramLMModel(document_statistics)
    for q_no in query_list:
        query = query_list[q_no]
        results = laplace_unigram.query(query, tf_for_queries[q_no])
        rank = 1
        for key, value in sorted(iter(results.items()), key=lambda k_v3: (k_v3[1],k_v3[0]), reverse=True):
            # if rank > Constants.MAX_OUTPUT:
                # break
            write_output(
                    model = 'laplace_unigram',
                    query_no = str(q_no),
                    doc_no = str(key),
                    rank = str(rank),
                    score = str(value))
            rank += 1
    print("Unigram LM with Laplace done")

def run_jelmer_unigram():
    print("Processing: Unigram LM with Jelinek-Mercer model")
    jelmer_unigram = JelinekMercerUnigramLMModel(document_statistics)
    for q_no in query_list:
        query = query_list[q_no]
        results = jelmer_unigram.query(
                query,
                tf_for_queries[q_no],
                total_tf_wd[q_no],
                total_length)
        rank = 1
        for key, value in sorted(iter(results.items()), key=lambda k_v4: (k_v4[1],k_v4[0]), reverse=True):
            # if rank > Constants.MAX_OUTPUT:
                # break
            write_output(
                    model = 'jelmer_unigram',
                    query_no = str(q_no),
                    doc_no = str(key),
                    rank = str(rank),
                    score = str(value))
            rank += 1
    print("Unigram LM with Jelinek Mercer done")

def run_pseudo_feedback():
    print("Processing: Pseudo Relevance Feedback model")
    pseudo_feedback = PseudoRelevanceFeedbackModel(document_statistics)
    for q_no in query_list:
        query = query_list[q_no]
        results = pseudo_feedback.query(
                query,
                total_length)['hits']['hits']
        rank = 1
        for result in results:
            write_output(
                    model = 'pseudo_feedback',
                    query_no = str(q_no),
                    doc_no = result['_id'],
                    rank = str(rank),
                    score = str(result['_score']))
            rank += 1
    print("Pseudo feedback done")

def build_document_statistics():
    print("Building document statistics")
    total_length = 0
    file_list = get_file_list()
    for doc_no in file_list:
        stats = DocumentStatistics(doc_no)
        document_statistics[doc_no] = stats.length
        total_length += stats.length
    return total_length

def clean_results_folder():
    print("Removing all files in the results folder")
    result_files = os.listdir(Constants.RESULTS_PATH)
    for result_file in result_files:
        os.remove(Constants.RESULTS_PATH + result_file)

def build_tf_for_queries():
    print("Collecting the tf values")
    for q_no in query_list:
        query = query_list[q_no]
        tf_collection  = []
        words = query.split(' ')
        for word in words:
            w_d, tf = get_term_statistics(word)
            wfd_collection[word] = w_d
            tf_collection.append(tf)
        tf_for_queries[q_no] = tf_collection

def build_total_tf_wd(q_no):
    query = query_list[q_no]
    words = query.split(' ')
    total_tf_list = []
    
    for i in range(len(words)):
        total_tf_list.append(np.sum(list(tf_for_queries[q_no][i].values())))

    total_tf_wd[q_no] = total_tf_list

if __name__ == '__main__':
    """Main function
    """
    threads = []
    total_tf_threads = []
    clean_results_folder()
    query_list = build_query_list()
    thread_tf = threading.Thread(target=build_tf_for_queries)
    thread_tf.start()
    total_length = build_document_statistics()
    thread_tf.join()
    
    for q_no in query_list:
        total_tf_threads.append(threading.Thread(
            target=build_total_tf_wd, args=[q_no]))

    for t in total_tf_threads:
        t.start()


    # t0 = threading.Thread(target=run_built_in)
    # threads.append(t0)
    t1 = threading.Thread(target=run_okapi_tf)
    threads.append(t1)
    t2 = threading.Thread(target=run_tf_idf)
    threads.append(t2)
    t3 = threading.Thread(target=run_bm25)
    threads.append(t3)
    t4 = threading.Thread(target=run_laplace_unigram)
    threads.append(t4)

    for thread in threads:
        thread.run()

    # for thread in threads:
        # thread.join()
    for t in total_tf_threads:
        t.join()

    run_jelmer_unigram()
    # run_pseudo_feedback()
