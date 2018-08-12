from es import *


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
    doc_no = ''
    length = 0

    def get_document_length(self, term_vectors):
        doc_length = 0

        if len(term_vectors) == 0:
            return 0
        else:
            terms = term_vectors['text']['terms']
            for term in terms:
                doc_length += terms[term]['term_freq']
            return doc_length

    def __init__(self, doc_no):
        self.doc_no = doc_no
        term_vectors = get_term_vectors(doc_no) 
        self.length = self.get_document_length(term_vectors) 
