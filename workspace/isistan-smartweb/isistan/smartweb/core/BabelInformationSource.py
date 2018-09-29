import urllib
import urllib2
import httplib
import json
from InformationSource import InformationSource
from isistan.smartweb.preprocess.StringTransformer import StringTransformer
from isistan.smartweb.util.HttpUtils import HttpUtils
from HeuristicJaccard import HeuristicJaccard
from HeuristicSpaCy import HeuristicSpaCy
from HeuristicSorensenDice import HeuristicSorensenDice
from HeuristicCosineSimilarity import HeuristicCosineSimilarity
from isistan.smartweb.preprocess.variablesGlobales import variablesGlobales
import unicodedata

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
        # Para almacenar las palabras reconocidas y sus search_url de la consulta
        self._cacheEntity = {}
        # Para almacenar cada id de palabra y su synset
        self._cacheSynset = {}
        self.varGlobales = None

        self._heuristic = None
        #self._heuristic = HeuristicJaccard()
        #self._heuristic = HeuristicSpaCy()
        #self._heuristic = HeuristicSorensenDice()
        #self._heuristic = HeuristicCosineSimilarity()

    def _query_babelnet(self, query, text):
        query = query.encode('utf-8')
        n_retries = 0
        retry = True
        '''
        NO SE PUEDE DESCARTAR POR MAS QUE LA ENTIDAD YA HAYA SIDO BUSCADA, PUEDE QUE AHORA
        DEPENDA DE OTRO CONTEXTO.

        if query in self._cache:
            print 'found information for query: ' + query
            self.cached_entity_count += 1
            logging.debug('La entidad esta en el CACHE -> ' + repr(self.cached_entity_count))
            logging.debug(query)
            return self._cache[query]
        '''

        while retry and n_retries < self._NUMBER_OF_RETRIES:
            try:
                retry = False
                # En lugar de volver a hacer el query, se cachea el search_url junto con la
                # entidad, ya que eso no depende del contexto sino de la API
                if query in self._cacheEntity:
                    print 'La palabra' + query + 'ya ha sido reconocida y ya se tiene su conjunto de sinonimos: '
                    logging.debug('La palabra' + query + 'ya ha sido reconocida y ya se tiene su conjunto de sinonimos: ')
                else:
                    params = {
                            'word': query,
                            'pos': 'NOUN',
                            'langs': 'EN',
                            'key': self._api_key
                    }
                    search_url = self._SEARCH_SERVICE_URL + '?' + urllib.urlencode(params)
                    self._cacheEntity[query] = json.loads(HttpUtils.http_request(search_url))
                    self.count_queries += 1
                    print "QUERY -> " + str(self.count_queries)

                if len(self._cacheEntity[query]) > 0:
                    print 'cacheEntity['+query+']: '
                    print json.dumps(self._cacheEntity[query])
                    logging.debug('cacheEntity['+query+']: ')
                    logging.debug(json.dumps(self._cacheEntity[query]))

                    for elem in self._cacheEntity[query]:
                        if elem['pos'] == 'NOUN':
                            if elem['id'] in self._cacheSynset:
                                print 'Ya se consulto por este sinonimo: ' + elem['id']
                                logging.debug('Ya se consulto por este sinonimo: ' + elem['id'])
                                logging.debug(self._cacheSynset[elem['id']])
                            else:
                                params = {
                                    'id': elem['id'],
                                    'key': self._api_key
                                }
                                synset_url = self._TOPIC_SERVICE_URL + '?' + urllib.urlencode(params)
                                #logging.debug('SYNSET_URL -> ' + synset_url)
                                synset = json.loads(HttpUtils.http_request(synset_url))
                                print '**************************'
                                print synset_url
                                print '**************************'
                                self.count_queries += 1
                                print "QUERY -> " + str(self.count_queries)
                                self._cacheSynset[elem['id']] = synset
                        else:
                            print 'No es sustantivo: ' + elem['id']
                            logging.debug('No es sustantivo: ' + elem['id'])
                else:
                    print 'No hay conjunto de sinonimos'
                    logging.debug('No hay conjunto de sinonimos')
            except (urllib2.HTTPError, httplib.BadStatusLine, urllib2.URLError):
                print 'retry'
                logging.debug('retry')
                retry = True
                n_retries += 1


    def get_description(self, query, text):
        #Creando cada algoritmo para obtener los resultdos, y definiendo en cual se basa la ejecucion
        stop_words = self.varGlobales.get_stop_words()
        self._heuristic = HeuristicJaccard(stop_words)
        heuristicSorensenDice = HeuristicSorensenDice(stop_words)
        heuristicSpaCy = HeuristicSpaCy(stop_words)
        heuristicCosineSimilarity = HeuristicCosineSimilarity(stop_words)

        #se completa en las heuristicas si no es el documento de contextos.
        rowContexts = [self.varGlobales.get_current_document(), query]
        rowResults = [self.varGlobales.get_current_document(), query]

        print "Doc " + str(self.varGlobales.get_current_document())

        additional_words = []
        maxValue = -1
        similarSentence = ''
        self._query_babelnet(query, text)

        synset = self._cacheEntity.get(query, None) #Si la entidad no fue insertada en el dict devuelve None
        if synset is not None:
            for elem in self._cacheEntity[query]:
                if elem['pos'] == 'NOUN':
                    sentido = self._cacheSynset[elem['id']]
                    for g in sentido['glosses']:
                        print 'IdSinonimo: ' + g['sourceSense']
                        logging.debug('IdSinonimo: ' + g['sourceSense'])

                        self._heuristic.calculate(text, g['gloss'].replace(";", "."), g['sourceSense'])
                        heuristicSorensenDice.calculate(text, g['gloss'].replace(";", "."), g['sourceSense'])
                        heuristicSpaCy.calculate(text, g['gloss'].replace(";", "."), g['sourceSense'])
                        heuristicCosineSimilarity.addContext(g['gloss'].replace(";", "."), g['sourceSense'])

                        rowContexts.append(g['gloss'].replace(";", ".").encode('utf-8'))
                    if(len(sentido['glosses']) != 0):
                        heuristicCosineSimilarity.calculate(text,'',0)

        result = self._heuristic.getBetterSentence()
        resultSorensenDice = heuristicSorensenDice.getBetterSentence()
        resultSpaCy = heuristicSpaCy.getBetterSentence()
        resultCosineSimilarity = heuristicCosineSimilarity.getBetterSentence()

        if result is not None:
            print '---------------------------------------------'
            print 'babelnetSource'
            print result
            print '---------------------------------------------'

            #rowResults.append(unicode(result['id']))
            rowResults.append(unicodedata.normalize('NFKD', unicode(result['contexto'])).encode('ascii', 'ignore'))
            rowResults.append(result['value'])

            rowResults.append(unicodedata.normalize('NFKD', unicode(resultSpaCy['contexto'])).encode('ascii', 'ignore'))
            rowResults.append(resultSpaCy['value'])

            rowResults.append(unicodedata.normalize('NFKD', unicode(resultSorensenDice['contexto'])).encode('ascii', 'ignore'))
            rowResults.append(resultSorensenDice['value'])

            rowResults.append(unicodedata.normalize('NFKD', unicode(resultCosineSimilarity['contexto'])).encode('ascii', 'ignore'))
            rowResults.append(resultCosineSimilarity['value'])

            #Solo tomo la sentencia del algoritmo por defecto
            sentences = result['sentence']
            logging.debug(sentences)
            for i in range(0, min(len(sentences), self._NUMBER_OF_SENTENCES)): #Toma hasta 3 oraciones(si hay)
                transformer = StringTransformer()
                additional_sentence = transformer.transform(sentences[i]).get_words_list()
                additional_words.extend(additional_sentence)
            
            self.varGlobales.add_row(rowResults, 'results')
        self.varGlobales.add_row(rowContexts, 'contexts')
        logging.debug(additional_words)
        return additional_words


    def get_type(self, query):
        pass

    def get_aka(self, query):
        pass

    def getCountEntitys(self):
        count = len(self._cacheEntity)
        print 'La cantidad de conjuntos que se consulto es: ' + str(count)
        logging.debug('La cantidad de conjuntos que se consulto es: ' + str(count))

    def getCountSynsets(self):
        count = len(self._cacheSynset)
        print 'La cantidad de sinonimos que se consulto es: ' + str(count)
        logging.debug('La cantidad de sinonimos que se consulto es: ' + str(count))

    def setVarGlobales(self,var):
        self.varGlobales = var