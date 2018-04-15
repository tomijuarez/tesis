import ner
from NamedEntityRecognizer import NamedEntityRecognizer

__author__ = 'Tomás Juárez y Damián Dominguez'


class SpacyNER(NamedEntityRecognizer):
    #
    # SpaCy named entity recognizer.

    # Agregar los tags que nos corresponden según el análisis que hicimos.
    ENTITY_ORGANIZATION = 'ORGANIZATION'

    def __init__(self):
        #self._engine = ... [instanciar]

    def get_entities(self, text):
        #Retornar las entidades en el formato adecuado [hacer]
