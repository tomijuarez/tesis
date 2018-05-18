import urllib
import urllib2
import httplib
import json
from InformationSource import InformationSource
from isistan.smartweb.preprocess.StringTransformer import StringTransformer
from isistan.smartweb.util.HttpUtils import HttpUtils

__author__ = 'ignacio'

import logging

class BabelInformationSource(InformationSource):
    #
    # Obtains information about terms using freebase as a source

    logging.basicConfig(filename='ner.log',
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s: %(message)s")

    _NUMBER_OF_RETRIES = 10
    _NUMBER_OF_SENTENCES = 3
    _SEARCH_SERVICE_URL = 'https://babelnet.io/v4/getSynsetIds'
    _TOPIC_SERVICE_URL = 'https://babelnet.io/v4/getSynset'

    count_queries = 0
    cached_entity_count = 0

    def __init__(self, api_key):
        self._api_key = api_key
        self._cache = {}

    def _query_babelnet(self, query):
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
                'word': query,
                'langs': 'EN',
                'key': self._api_key
        }
        search_url = self._SEARCH_SERVICE_URL + '?' + urllib.urlencode(params)
        while retry and n_retries < self._NUMBER_OF_RETRIES:
            try:
                retry = False
                response = json.loads(HttpUtils.http_request(search_url))
                self.count_queries += 1
                logging.debug('Query realizada -> ' + repr(self.count_queries))
                if len(response) > 0:
                    print 'Response:'
                    print json.dumps(response)
                    logging.debug('Response: ')
                    logging.debug(json.dumps(response))
                    
                    for elem in response:
                        if elem['pos'] == 'NOUN':
                            if elem['id'] in self._cache:
                                print 'found information for query: ' + query
                                logging.debug('Agregando entidad al cache')
                                logging.debug(query)
                                return self._cache[elem['id']]
                            params = {
                                'id': elem['id'],
                                'key': self._api_key
                            }
                            synset_url = self._TOPIC_SERVICE_URL + '?' + urllib.urlencode(params)
                            synset = json.loads(HttpUtils.http_request(synset_url))
                            self._cache[query] = synset
                            self._cache[elem['id']] = synset
                            return synset
            except (urllib2.HTTPError, httplib.BadStatusLine, urllib2.URLError):
                print 'retry'
                logging.debug('retry')
                retry = True
                n_retries += 1

    def get_description(self, query):
        additional_words = []
        synset = self._query_babelnet(query)
        if synset is not None:
            if len(synset) > 0:
                if len(synset['glosses']) > 0:
                    if 'gloss' in synset['glosses'][0]:
                        sentences = synset['glosses'][0]['gloss'].split('.')
                        print 'Description Result:'
                        print sentences
                        logging.debug('Description Result: ')
                        logging.debug(sentences)

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
            else:
                print 'information not found for query: ' + query
                logging.debug('information not found for query: ' + query)
        return additional_words

    def get_type(self, query):
        pass

    def get_aka(self, query):
        pass
