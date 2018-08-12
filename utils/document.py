class Document(object):
    doc_id = ""
    text = ""
    doc_length = 0

    def __init__(self, doc_id, text, doc_length):
        self.doc_id = doc_id
        self.text = text
        self.doc_length = doc_length
