import sys
import numpy as np
sys.path.insert(0, '/home/prdx/Documents/CS6200-Summer/A1/')

from utils.statistics import IndexStatistics
from utils.statistics import DocumentStatistics
from utils.text import * 
from utils.es import *


class OkapiBM25(object):
    """Scoring for Okapi BM25
    """
    # Constants
    k1 = 1.2
    k2 = 100
    b = 0.75
    document_statistics = {}
        
    def query(self, keywords = '', wd_collection = [], tf_collection = []):
        tf = 0
        result = {}

        words = keywords.split(' ')

        print "Calculating the okapi BM25"
        
        file_list = get_file_list()
        for doc in file_list:
            tf = 0
            for i in range(len(words)):
                tf += self.bm25(doc, wd_collection[words[i]], tf_collection[i][doc])
            result[doc] = tf
                
        return result
    
    def bm25(self, doc_no = '', df_w = 0, tf_wd = 0):
        """
        """
        D = self.index_statistics.doc_count
        doc_length = self.document_statistics[doc_no]
        avg_doc_length = self.index_statistics.avg_doc_length
        d = doc_length / float(avg_doc_length)

        first_term = (D + 0.5) / (df_w + 0.5)
        first_term = np.log(first_term)

        second_term_numerator = tf_wd + self.k1 * tf_wd
        second_term_denominator = tf_wd + self.k1 * ((1 - self.b) + self.b * d)
        second_term = second_term_numerator / second_term_denominator

        # We consider the tf_wq = 1, thus we can ignore the third term
        
        return first_term * second_term


    def __init__(self, document_statistics):
        self.index_statistics = IndexStatistics()
        self.document_statistics = document_statistics
