from HeuristicAbs import HeuristicAbs
import nltk
import string
from gensim import corpora, models, similarities

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

class HeuristicCosineSimilarity(HeuristicAbs):
    #
    # Obtains information about terms using freebase as a source

    def __init__(self, stop_words):
        self.stop_words = stop_words
        self._analyzed_sentences = []
        self.ids = []
        self.contexts = []

    def calculate(self, documentText, synsetContext, id):

        #texts = [[word for word in document.lower().split()] for document in documents]
        #texts = [preprocessor(text) for text in texts]
        texts = self.contexts
        print 'texts'
        print texts
        print '--------------------------'
        dictionary = corpora.Dictionary(texts)
        print 'dictionary'
        print dictionary
        print '--------------------------'
        corpus = [dictionary.doc2bow(text) for text in texts]
        print 'corpus'
        print corpus
        print '--------------------------'
        tfidf_model = models.TfidfModel(corpus)
        print 'tfidf_model'
        print tfidf_model
        print '--------------------------'
        tfidf_corpus = tfidf_model[corpus]
        print 'tfidf_corpus'
        print tfidf_corpus
        print '--------------------------'
        index = similarities.MatrixSimilarity(tfidf_corpus)
        print 'index'
        print index
        print '--------------------------'


        documentText = self.normalizeText(documentText)
        documentText_vector = dictionary.doc2bow(documentText)

        query_tfidf_vector = tfidf_model[documentText_vector]
        print 'query_tfidf_vector'
        print query_tfidf_vector
        print '--------------------------'
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
        print(results)
        logging.debug('RESULTADOS COSINE:')
        logging.debug(results)
        for result in results:
            print self.ids[result[0]]
            print result
            self._analyzed_sentences.append({"id":self.ids[result[0]], "value":result[1], "sentence":self.contexts[result[0]]})

    def addContext(self, synsetContext, id):
        logging.debug('Contexto: ' + synsetContext)
        synsetContext = self.normalizeText(synsetContext)
        self.ids.append(id)
        self.contexts.append(synsetContext)

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