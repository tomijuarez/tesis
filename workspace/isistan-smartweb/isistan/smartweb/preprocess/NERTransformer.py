from Transformer import Transformer
from isistan.smartweb.core.InformationSource import InformationSource
from isistan.smartweb.core.NamedEntityRecognizer import NamedEntityRecognizer

__author__ = 'ignacio'


class NERTransformer(Transformer):
    #
    # Identifies entities in the words and add expands
    # the meaning by adding freebase information

    def __init__(self, information_source, ner):
        self._cache = {}
        assert not issubclass(information_source, InformationSource)
        assert not issubclass(ner, NamedEntityRecognizer)
        self._ner = ner
        self._information_source = information_source

    def transform(self, wordbag):
        string_data = wordbag.get_words_str()
        string_data = string_data.replace('API', '')
        string_data = string_data.replace('Api', '')
        entities = self._get_entities(string_data)
        if entities is not None:
            for entity in entities:
                #additional_information = self._information_source.get_description(entity)
                additional_information = self._information_source.get_description(entity.text)
                if additional_information is not None:
                    wordbag.get_words_list().extend(additional_information)
        return wordbag
    
    ''' VERSION ORIGINAL 
    def _get_entities(self, text):
        entities = self._ner.get_entities(text)
        if self._ner.ENTITY_ORGANIZATION in entities:
            if entities[self._ner.ENTITY_ORGANIZATION] is not None:
                return entities[self._ner.ENTITY_ORGANIZATION]
            else:
                return None
    
    '''
    #MODIFICACION PARA INTEGRAR SPACY
    def _get_entities(self, text):
        return self._ner.get_entities(text)