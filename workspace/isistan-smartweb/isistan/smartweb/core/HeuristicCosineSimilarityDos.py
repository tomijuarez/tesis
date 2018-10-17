from HeuristicAbs import HeuristicAbs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import string

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

stemmer = PorterStemmer()
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

class HeuristicCosineSimilarityDos(HeuristicAbs):
    #
    # Obtains information about terms using freebase as a source

    def __init__(self, stop_words):
        self.stop_words = stop_words
        self.originalContext = []
        self._analyzed_sentences = []

    def calculate(self, documentText, synsetContext, id):
      #Agrego el documento en la primer posicion\
      self.originalContext.insert(0,documentText)

      #vectorizer = TfidfVectorizer(stop_words='english')
      vectorizer = StemmedTfidfVectorizer(analyzer="word", stop_words='english')
      features = vectorizer.fit_transform(self.originalContext).todense() 
      #print( vectorizer.vocabulary_ )
      results = []
      for f in features:
          #print features[0]
          #print f
          #print( cosine_similarity(features[0], f) )
          results.append(cosine_similarity(features[0], f))
      
      logging.debug('RESULTADOS COSENO LIBRERIA:')
      print 'RESULTADOS COSENO'
      for i in range(1, len(results)):
          contextNormalized = self.normalizeText(self.originalContext[i]);
          logging.debug({"contexto":self.originalContext[i], "value":results[i][0][0], "sentence":contextNormalized})
          self._analyzed_sentences.append({"contexto":self.originalContext[i], "value":results[i][0][0], "sentence":contextNormalized})


    def addContext(self, synsetContext, id):
        logging.debug('Contexto: ' + synsetContext)
        #Guardo el contexto
        self.originalContext.append(synsetContext)

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