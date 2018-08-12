import sys
import numpy as np
sys.path.insert(0, '/home/prdx/Documents/CS6200-Summer/A1/')

from utils.statistics import IndexStatistics
from utils.statistics import DocumentStatistics
from utils.text import * 
from utils.es import *

class JelinekMercerUnigramLMModel(object):
    def query(self, keywords = '', tf_collection = [], total_tf_wd = [], total_doc_length = 0):
        p_laplace = 0
        result = {}

        words = keywords.split(' ')
        print "Calculating the unigram LM with Jelinek Mercer"
        file_list = get_file_list()
        for doc in file_list:
            p_laplace = 0
            for i in range(len(words)):
                # For background
                p_laplace += self.jelinekmercer_unigram_lm(doc, tf_collection[i][doc], total_tf_wd[i], total_doc_length)

            result[doc] = p_laplace
        return result

    def jelinekmercer_unigram_lm(self, doc_no = '', tf_wd = 0, total_tf_wd = 0, total_doc_length = 0):
        corpus_prob = 0.2
        
        doc_length = self.document_statistics[doc_no]

        if doc_length == 0 or (tf_wd == 0 and total_tf_wd == 0):
            return 0
        foreground = corpus_prob * (float(tf_wd) / doc_length)

        _corpus_prob = 1.0 - corpus_prob
        _tf_wd = total_tf_wd - tf_wd
        _doc_length = total_doc_length - doc_length
        
        background = _corpus_prob * (float(_tf_wd) / _doc_length)

        p_laplace_wd = foreground + background 

        # To debug
        if p_laplace_wd == 0:
            print background 
            print foreground
            print "tf_wd: {0}".format(tf_wd)
            print "_tf_wd: {0}".format(_tf_wd)
            print "doc_length: {0}".format(doc_length)
            print "_doc_length: {0}".format(_doc_length)
            print "corpus_prob: {0}".format(corpus_prob)
            print "_corpus_prob: {0}".format(_corpus_prob)
        return np.log(p_laplace_wd)

    def __init__(self, document_statistics):
        self.index_statistics = IndexStatistics()
        self.document_statistics = document_statistics
