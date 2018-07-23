from HeuristicAbs import HeuristicAbs
#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
import nltk
import string
import spacy

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

class HeuristicSpaCy(HeuristicAbs):

    def __init__(self, stop_words):
        #self.stop_words = set(stopwords.words("english"))  # load stopwords
        self.stop_words = stop_words
        self._analyzed_sentences = []

    def calculate(self, documentText, synsetContext, id):
        logging.debug('Contexto: ' + synsetContext)
        nlp = spacy.load('en')
        a = nlp(unicode(documentText, "utf-8"))
        b = nlp(synsetContext)
        resultado = b.similarity(a)
        logging.debug('resultado: ' + str(resultado))
        self._analyzed_sentences.append({"id":id, "value":resultado, "sentence":synsetContext})

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