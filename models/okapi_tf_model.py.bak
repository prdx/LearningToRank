import sys
sys.path.insert(0, '/home/prdx/Documents/CS6200-Summer/A1/')

from utils.statistics import IndexStatistics
from utils.statistics import DocumentStatistics
from utils.text import * 
from utils.es import *

class OkapiTFModel(object):
    """ Calculate Okapi TF in document
    """
    index_statistics = None
    document_statistics = {}

    def query(self, keywords = '', tf_collection = []):
        tf = 0
        result = {}

        words = keywords.split(' ')

        print "Calculating the okapi TF"
        
        file_list = get_file_list()
        for doc in file_list:
            tf = 0
            for i in range(len(words)):
                tf += self.okapi_tf(doc, tf_collection[i][doc])
            result[doc] = tf
                
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


# otf = OkapiTFModel()
# result = otf.query("nuclear united states")

# for key, value in sorted(result.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    # print "%s: %s" % (key, value)
