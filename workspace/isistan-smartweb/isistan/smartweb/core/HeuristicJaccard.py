from HeuristicAbs import HeuristicAbs
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

class HeuristicJaccard(HeuristicAbs):
    #
    # Obtains information about terms using freebase as a source

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))  # load stopwords

    def calculate(self, documentText, synsetContext):
        logging.debug('Contexto: ' + synsetContext)

        documentText = self.normalizeText(documentText)
        synsetContext = self.normalizeText(synsetContext)
        a = set(documentText)
        b = set(synsetContext)

        c = a.intersection(b)


        resultado = float(len(c)) / (len(a) + len(b) - len(c))
        logging.debug(str(len(c)) + ' / (' + str(len(a)) + ' + ' + str(len(b)) + ' - ' + str(len(c)) + ') = ' + str(resultado) )
        logging.debug('resultado: ' + str(resultado))
        self.analyzed_sentences.append({"value":resultado, "sentence":synsetContext})

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

    def getBetterSentence(self):
        sentence = ''
        maxValue = -1
        for elem in self.analyzed_sentences:
            #logging.debug(str(elem['value']) + ' - ' + str(elem['sentence']))
            if elem['value'] > maxValue:
                maxValue = elem['value']
                sentence = elem['sentence']
        #logging.debug('sentencia elegida: ')
        #logging.debug(sentence)
        return sentence