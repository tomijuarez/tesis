import ner
from NamedEntityRecognizer import NamedEntityRecognizer

__author__ = 'ignacio'


class StandfordNER(NamedEntityRecognizer):
    #
    # Standford named entity recognizer

    ENTITY_ORGANIZATION = 'ORGANIZATION'

    def __init__(self, host='localhost', port=8080):
        self._engine = ner.SocketNER(host=host, port=port)

    def get_entities(self, text):
        return self._engine.get_entities(text)