from HeuristicAbs import HeuristicAbs
import nltk
import string
from gensim import corpora, models, similarities
from nltk.stem.porter import PorterStemmer

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

class PorterPreprocessor(object):

    def __init__(self, stop_words):
        self._stemmer = PorterStemmer()
        self._stoplist = stop_words

    def process_term(self, term):
        stem_term = None
        term = term.lower()
        stops = set(self._stoplist)
        if term is not None and term not in stops:
            stem_term = self._stemmer.stem(term)
        return stem_term


class StringPreprocessor(PorterPreprocessor):
    #
    # String query preprocessor

    def __init__(self, stop_words):
        super(StringPreprocessor, self).__init__(stop_words)

    def __call__(self, *args):
        terms = []
        data = args[0]
        for term in data:
            processed_term = self.process_term(term)
            if processed_term is not None:
                terms.append(processed_term)

        logging.debug('Contexto procesado: ')
        logging.debug(processed_term)
        return terms


class HeuristicCosineSimilarity(HeuristicAbs):
    #
    # Obtains information about terms using freebase as a source

    def __init__(self, stop_words):
        self.stop_words = stop_words
        self._analyzed_sentences = []
        self.originalContext = []
        self.contexts = []
        self.processedContext = []
        self.preprocessor = StringPreprocessor(stop_words)

    def calculate(self, documentText, synsetContext, id):

        #Inicializando texts con cada contexto devuelto por Babelnet
        texts = self.processedContext

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf_model = models.TfidfModel(corpus)
        tfidf_corpus = tfidf_model[corpus]
        index = similarities.MatrixSimilarity(tfidf_corpus, num_features=len(dictionary))

        #Genera el vector del documento del que fue extraida la entidad
        documentText_vector = dictionary.doc2bow(self.preprocessor(documentText.split()))

        query_tfidf_vector = tfidf_model[documentText_vector]
        results = index[query_tfidf_vector]
        results = sorted(enumerate(results), key=lambda item: -item[1])

        ''' Se guarda un arreglo de pares(posicion_contexto, distancia) ordenados por el 
            valor de la distancia: 
            [
                (8, 0.62825805), 
                (7, 0.2801947), 
                ...
                (0, 0.0)
            ]
        '''
        logging.debug('RESULTADOS COSINE:')
        for result in results:
            logging.debug({"contexto":self.originalContext[result[0]], "value":result[1], "sentence":self.contexts[result[0]]})
            self._analyzed_sentences.append({"contexto":self.originalContext[result[0]], "value":result[1], "sentence":self.contexts[result[0]]})


    def addContext(self, synsetContext, id):
        logging.debug('Contexto: ' + synsetContext)
        self.originalContext.append(synsetContext)
        synsetContext = self.normalizeText(synsetContext)
        self.contexts.append(synsetContext)
        self.processedContext.append(self.preprocessor(synsetContext))

    def normalizeText(self, text):
        #Elimino los componentes de puntuacion
        text = filter(lambda x: x not in string.punctuation, text)

        #Cambiamos todo a minusculas
        text = text.lower()

        #Creamos las listas de palabras
        text = text.split(" ")

        # eliminar stopwords
        text = filter(lambda x: x not in self.stop_words, text)

        return text