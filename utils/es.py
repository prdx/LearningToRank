from elasticsearch5 import Elasticsearch
from .constants import Constants
from .text import get_file_list
import json

es = Elasticsearch()

def create_index():
    """Create new index
    """
    es.indices.create(Constants.INDEX_NAME, 
            body = get_es_script('index_create'))

def delete_index():
    """Delete existing index
    """
    es.indices.delete(index = Constants.INDEX_NAME, ignore = [400, 404])

def get_es_script(script_name):
    """Read es json file
    return dictionary of the body
    """
    with open(Constants.ES_SCRIPTS_PATH + script_name + '.json') as s:
        body = json.load(s)
    return body

def get_doc_count():
    """Retrieve document count from ES
    return int number of documents in the corpus
    """
    result = es.count(index = Constants.INDEX_NAME,
            doc_type = Constants.DOC_TYPE)
    return result['count']

def get_field_statistics(_id = 'AP890201-0001'):
    """Get field statistics
    return dictionary of field statistics
    """
    result = es.termvectors(index = Constants.INDEX_NAME, 
            doc_type = Constants.DOC_TYPE,
            id = _id, 
            body = get_es_script('term_vectors')) 
    return result["term_vectors"]['text']['field_statistics']

def get_term_vectors(_id = 'AP890201-0001'):
    """Get field statistics
    return dictionary of field statistics
    """
    result = es.termvectors(index = Constants.INDEX_NAME, 
            doc_type = Constants.DOC_TYPE,
            id = _id, 
            body = get_es_script('term_vectors')) 

    if 'term_vectors' in result:
        return result["term_vectors"]
    else:
        return {}

def get_term_statistics(term):
    """Get terms statistics
    return dictionary of term frequency of each documents
    """
    # print "Getting tf for term: {0}".format(term)
    file_list = get_file_list()
    tf_wd = {}
    df_w = 0

    for doc in file_list:
        tf_wd[doc] = 0

    body = get_es_script('tf')
    body['query']['match']['text'] = term
    body['script_fields']['index_tf']['script']['inline'] = \
            "_index['text']['" + term + "'].tf()"

    result = es.search(
        index = Constants.INDEX_NAME,
        doc_type= Constants.DOC_TYPE,
        size=5000,
        scroll='15m',
        body=body)

    scroll_id = result['_scroll_id']
    while True:
        if len(result['hits']['hits']) == 0:
            break
        for doc in result['hits']['hits']:
            doc_id = doc['_id']
            doc_info = doc['fields']
            tf_wd[doc_id] = doc_info['index_tf'][0]

            # Get total number of document 
            if tf_wd[doc_id] > 0:
                df_w += 1
        result = es.scroll(scroll_id = scroll_id, scroll = '15m')

    return df_w, tf_wd

def get_vocab_size():
    """Get vocabulary size of the corpus
    return int vocabulary size
    """
    body = get_es_script('agg_vocab_size')
    return search("", body)['aggregations']['vocabSize']['value']


def search(keywords = "", body = {}):
    """ES Built-in search command
    parameter string keyword to search
    return list of matched documents
    """
    if len(body) == 0 and keywords != "":
        body = get_es_script('search')
        body['query']['match']['text'] = keywords 
        body['size'] = Constants.MAX_OUTPUT
        

    res = es.search(index = Constants.INDEX_NAME,
            body = body
        )
    return res

def store_document(doc_id, text):
    es.index(index = Constants.INDEX_NAME,
            doc_type = Constants.DOC_TYPE,
            id = doc_id,
            body = {
                "doc_id": doc_id,
                "text": text
                }
            )
