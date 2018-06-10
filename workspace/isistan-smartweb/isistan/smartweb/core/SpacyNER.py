import ner
from NamedEntityRecognizer import NamedEntityRecognizer
import spacy

__author__ = 'Tomas Juarez y Damian Dominguez'


class SpacyNER(NamedEntityRecognizer):
    #
    # SpaCy named entity recognizer.

    # Agregar los tags que nos corresponden segun el analisis que hicimos.
    ENTITY_ORGANIZATION = 'ORGANIZATION'
    types_labels = {"ORG"}

    def __init__(self):
        #self._engine = ... [instanciar]
        self.nlp = spacy.load('en') #cargo el modelo en ingles.


    def get_entities(self, text):
        #Retornar las entidades en el formato adecuado [hacer]
        results = []
        doc = self.nlp(text.decode('UTF-8'))
        for ent in doc.ents:
            if ent.label_ in self.types_labels:
                results.append(ent)

        return results