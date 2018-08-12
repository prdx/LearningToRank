from utils.es import *
from utils.statistics import DocumentStatistics
import numpy as np

class PseudoRelevanceFeedbackModel(object):
    """Pseudo relevance feedback
    The general algorithm is:

    1. Retrieve the top k documents using one of the above retrieval models.
    2. Identify terms in these documents which are distinctive to the documents.
    3. Add the terms to the query, and re-run the retrieval process. Return the final results.
    """
    k = 0
    results_id = []
    doc_length_of_k = 0
    keywords = ""
    term_in_k = {}
    sum_of_term_tf = {}
    max_delta = -999999999
    relevant_keyword = ''
    total_doc_length = 0

    def query(self, keywords, total_doc_length):
        self.total_doc_length = total_doc_length
        self.keywords = keywords
        results = search(keywords)['hits']['hits']
        # Gather the id
        counter = 0
        for result in results:
            if counter == self.k:
                break
            self.results_id.append(result['_id'])
            counter += 1
        self.get_doc_length_of_k_result()
        self.gather_terms()
        self.get_max_delta()
        return search(keywords + " " + self.relevant_keyword)

    def get_doc_length_of_k_result(self):
        for _id in self.results_id:
            self.doc_length_of_k += DocumentStatistics(_id).length

    def get_sum_of_term_tf(self, word):
        try:
            w_d, tf = get_term_statistics(word)
            print "For word: {0}".format(word)
            # print tf
            self.sum_of_term_tf[word] = np.sum(tf.values())
        except Exception as exception:
            print exception
            

    def get_max_delta(self):
        # If a document appears often in the result but less in the corpus
        # The delta of the prob a word appear in the result - 
        # the prob a word appear in the entire corpus
        foreground = 0
        background = 0
        for term in self.term_in_k:
            try:
                foreground = float(self.term_in_k[term]) / self.doc_length_of_k
                background = float(self.sum_of_term_tf[term]) / self.total_doc_length
                delta = foreground - background
            except:
                delta = -999999999
            if delta >= self.max_delta:
                self.relevant_keyword = term
                self.max_delta = delta
                print "Relevant keyword: {0}".format(self.relevant_keyword)

        print foreground
        print background
                

    def gather_terms(self):
        for _id in self.results_id:
            terms = get_term_vectors(_id)['text']['terms']
            for term in terms:
                if term not in self.keywords:
                    self.get_sum_of_term_tf(term)
                    if term in self.term_in_k:
                        self.term_in_k[term] += terms[term]['term_freq']
                    else:
                        self.term_in_k[term] = terms[term]['term_freq']
                    
                    # if terms[term]['term_freq'] > max_term_freq:
                        # max_term_freq = terms[term]['term_freq']
                        # frequent_term = term
    

    def __init__(self, document_statistics, k = 10):
        self.document_statistics = document_statistics
        self.k = k
