from .es import *

class IndexStatistics(object):
    doc_count = 0
    avg_doc_length = 0
    vocab_size = 0

    def get_doc_count(self):
        return get_doc_count()

    def get_avg_doc_length(self):
        field_statistics = get_field_statistics()
        return field_statistics['sum_ttf'] / field_statistics['doc_count']

    def get_vocab_size(self):
        return get_vocab_size()

    def __init__(self):
        self.doc_count = self.get_doc_count()
        self.avg_doc_length = self.get_avg_doc_length()
        self.vocab_size = self.get_vocab_size()



class DocumentStatistics(object):
    term_freq_dict = {}
    doc_no = ''

    def __init__(self, doc_no):
        self.doc_no = doc_no
        self.term_freq_dict = get_terms_statistics(doc_no)
