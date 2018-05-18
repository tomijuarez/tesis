import urllib
import urllib2
import httplib
import json
from InformationSource import InformationSource
from isistan.smartweb.preprocess.StringTransformer import StringTransformer
from isistan.smartweb.util.HttpUtils import HttpUtils

__author__ = 'ignacio'

import logging

class FreebaseInformationSource(InformationSource):
    #
    # Obtains information about terms using freebase as a source

    logging.basicConfig(filename='ner.log',
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s: %(message)s")

    _NUMBER_OF_RETRIES = 10
    _NUMBER_OF_SENTENCES = 3
    _SEARCH_SERVICE_URL = 'https://www.googleapis.com/freebase/v1/search'
    _TOPIC_SERVICE_URL = 'https://www.googleapis.com/freebase/v1/topic'

    count_queries = 0
    cached_entity_count = 0

    def __init__(self, api_key):
        self._api_key = api_key
        self._cache = {}

    def _query_freebase(self, query):
        query = query.encode('utf-8')
        n_retries = 0
        retry = True
        if query in self._cache:
            print 'found information for query: ' + query
            self.cached_entity_count += 1
            logging.debug('La entidad esta en el CACHE -> ' + repr(self.cached_entity_count))
            logging.debug(query)            
            return self._cache[query]
        params = {
            'query': query,
            'key': self._api_key
        }
        search_url = self._SEARCH_SERVICE_URL + '?' + urllib.urlencode(params)
        while retry and n_retries < self._NUMBER_OF_RETRIES:
            try:
                retry = False
                response = json.loads(HttpUtils.http_request(search_url))
                self.count_queries += 1
                logging.debug('Query realizada -> ' + repr(self.count_queries))
                if len(response['result']) > 0:
                    logging.debug('Response: ')
                    logging.debug(json.dumps(response['result']))
                    topic_id = response['result'][0]['mid']
                    if topic_id in self._cache:
                        print 'found information for query: ' + query
                        logging.debug('found information for query: ' + query)
                        return self._cache[topic_id]
                    params = {
                        'key': self._api_key,
                        'filter': 'suggest'
                    }
                    topic_search_url = self._TOPIC_SERVICE_URL + topic_id + '?' + urllib.urlencode(params)
                    topic = json.loads(HttpUtils.http_request(topic_search_url))
                    self._cache[query] = topic
                    self._cache[topic_id] = topic
                    return topic
            except (urllib2.HTTPError, httplib.BadStatusLine, urllib2.URLError):
                print 'retry'
                logging.debug('retry')
                retry = True
                n_retries += 1

    def get_description(self, query):
        additional_words = []
        topic = self._query_freebase(query)
        if topic is not None:
            if '/common/topic/article' in topic['property']:
                if '/common/document/text' in topic['property']['/common/topic/article']['values'][0]['property']:
                    sentences = topic['property']['/common/topic/article']['values'][0]['property']['/common/document/text']['values'][0]['value'].split('.')
                    if sentences is not None:
                        print 'found information for query: ' + query                        
                        logging.debug('found information for query: ' + query)

                        for i in range(0, min(len(sentences), self._NUMBER_OF_SENTENCES)):
                            transformer = StringTransformer()
                            additional_sentence = transformer.transform(sentences[i]).get_words_list()
                            additional_words.extend(additional_sentence)
                    else:
                        print 'information not found for query: ' + query
                        logging.debug('information not found for query: ' + query)

                else:
                    print 'information not found for query: ' + query
                    logging.debug('information not found for query: ' + query)

            else:
                print 'information not found for query: ' + query
                logging.debug('information not found for query: ' + query)
        return additional_words

    def get_type(self, query):
        additional_words = []
        topic = self._query_freebase(query)
        if topic is not None:
            if '/common/topic/notable_types' in topic['property']:
                sentences = topic['property']['/common/topic/notable_types']['values'][0]['text']
                if sentences is not None:
                    print 'found parent type for query: ' + query
                    logging.debug('found parent type for query: ' + query)
                    transformer = StringTransformer()
                    additional_sentence = transformer.transform(sentences).get_words_list()
                    additional_words.extend(additional_sentence)
                else:
                    print 'parent type not found for query: ' + query
                    logging.debug('parent type not found for query: ' + query)
            else:
                print 'parent type not found for query: ' + query
                logging.debug('parent type not found for query: ' + query)
        else:
            print 'parent type not found for query: ' + query
            logging.debug('parent type not found for query: ' + query)

    def get_aka(self, query):
        additional_words = []
        topic = self._query_freebase(query)
        if topic is not None:
            if '/common/topic/alias' in topic['property']:
                sentences = topic['property']['/common/topic/alias']['values'][0]['text']
                if sentences is not None:
                    print 'found alias for query: ' + query
                    logging.debug('found alias for query: ' + query)
                    print sentences
                    logging.debug(sentences)
                    transformer = StringTransformer()
                    additional_sentence = transformer.transform(sentences).get_words_list()
                    additional_words.extend(additional_sentence)
                else:
                    print 'alias not found for query: ' + query
                    logging.debug('alias not found for query: ' + query)
            else:
                print 'alias not found for query: ' + query
                logging.debug('alias not found for query: ' + query)
        else:
            print 'alias not found for query: ' + query
            logging.debug('alias not found for query: ' + query)
