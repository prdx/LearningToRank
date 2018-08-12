from utils.es import *

class BuiltInModel(object):
    def query(self, keywords = ""):
        return search(keywords)
