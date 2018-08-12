import sys
import numpy as np
sys.path.insert(0, '/home/prdx/Documents/CS6200-Summer/A1/')

from utils.statistics import IndexStatistics
from utils.text import * 
from utils.es import *

class TFIDFModel(object):
    document_statistics = {}

    def query(self, keywords = '', wd_collection = [], tf_collection = []):
        tf_idf = 0
        result = {}
        words = keywords.split(' ')

        print "Calculating the okapi TF"
        
        file_list = get_file_list()
        for doc in file_list:
            tf_idf = 0
            for i in range(len(words)):
                okapi_tf = self.okapi_tf(doc, tf_collection[i][doc])
                idf = self.index_statistics.doc_count / (1 + wd_collection[words[i]])

                tf_idf += okapi_tf * np.log(idf) 
            result[doc] = tf_idf
                
        return result

    def okapi_tf(self, doc_no = '', tf_wd = 0):
    
        doc_length = self.document_statistics[doc_no]
        avg_doc_length = self.index_statistics.avg_doc_length

        d = doc_length / float(avg_doc_length)
        denom = tf_wd + 0.5 + 1.5 * d
        result = (tf_wd / denom)
        return result 


    def __init__(self, document_statistics):
        self.index_statistics = IndexStatistics()
        self.document_statistics = document_statistics
