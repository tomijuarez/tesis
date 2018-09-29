from HeuristicAbs import HeuristicAbs
#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
import nltk
import string

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

class HeuristicSorensenDice(HeuristicAbs):
    #
    # Obtains information about terms using freebase as a source

    def __init__(self, stop_words):
        #self.stop_words = set(stopwords.words("english"))  # load stopwords
        self.stop_words = stop_words
        self._analyzed_sentences = []

    def calculate(self, documentText, synsetContext, id):
        logging.debug('Contexto: ' + synsetContext)

        contexto = synsetContext

        documentText = self.normalizeText(documentText)
        synsetContext = self.normalizeText(synsetContext)
        a = set(documentText)
        b = set(synsetContext)

        c = a.intersection(b)


        resultado = (2 * float(len(c)))/ (len(a) + len(b))
        logging.debug('2 * ' + str(len(c)) + ' / (' + str(len(a)) + ' + ' + str(len(b)) + ') = ' + str(resultado) )
        logging.debug('resultado: ' + str(resultado))
        self._analyzed_sentences.append({"contexto":contexto, "value":resultado, "sentence":synsetContext})

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