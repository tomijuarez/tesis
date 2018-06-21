from HeuristicAbs import HeuristicAbs
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
import spacy

__author__ = 'Tomas Juarez y Damian Dominguez'

import logging

class HeuristicSpaCy(HeuristicAbs):

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))  # load stopwords

    def calculate(self, documentText, synsetContext):
        logging.debug('TEXTO: ')
        logging.debug(documentText)
        logging.debug('Contexto: ')
        logging.debug(synsetContext)
        nlp = spacy.load('en')
        a = nlp(unicode(documentText, "utf-8"))
        b = nlp(synsetContext)
        resultado = b.similarity(a)
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
        return sentence