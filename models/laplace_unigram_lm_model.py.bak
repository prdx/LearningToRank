import sys
import numpy as np
sys.path.insert(0, '/home/prdx/Documents/CS6200-Summer/A1/')

from utils.statistics import IndexStatistics
from utils.statistics import DocumentStatistics
from utils.text import * 
from utils.es import *

class LaplaceUnigramLMModel(object):
    def query(self, keywords = '', tf_collection = []):
        p_laplace = 0
        result = {}

        words = keywords.split(' ')

        print "Calculating the unigram LM with Laplace"
        
        file_list = get_file_list()
        for doc in file_list:
            p_laplace = 0
            for i in range(len(words)):
                p_laplace += self.laplace_unigram_lm(doc, tf_collection[i][doc])
            result[doc] = p_laplace
            # print p_laplace
        return result

    def laplace_unigram_lm(self, doc_no = '', tf_wd = 0):
        doc_length = self.document_statistics[doc_no]
        V = self.index_statistics.vocab_size
        p_laplace_wd = (tf_wd + 1.0) / (doc_length + float(V))
        return np.log(p_laplace_wd)

    def __init__(self, document_statistics):
        self.index_statistics = IndexStatistics()
        self.document_statistics = document_statistics
