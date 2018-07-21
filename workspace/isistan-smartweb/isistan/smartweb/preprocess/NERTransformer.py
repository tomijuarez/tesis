from Transformer import Transformer
from isistan.smartweb.core.InformationSource import InformationSource
from isistan.smartweb.core.NamedEntityRecognizer import NamedEntityRecognizer

__author__ = 'ignacio'

import logging


class NERTransformer(Transformer):
    #
    # Identifies entities in the words and add expands
    # the meaning by adding freebase information
    logging.basicConfig(filename='ner.log',
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s: %(message)s")


    def __init__(self, information_source, ner):
        self._cache = {}
        assert not issubclass(information_source, InformationSource)
        assert not issubclass(ner, NamedEntityRecognizer)
        self._ner = ner
        self._information_source = information_source
        self.varGlobales = None


    def setVarGlobales(self,var):
        self.varGlobales = var
        self._information_source.setVarGlobales(var)

    def transform(self, wordbag):
        string_data = wordbag.get_words_str()
        string_data = string_data.replace('API', '')
        string_data = string_data.replace('Api', '')
        entities = self._get_entities(string_data)
        if entities is not None:
            for entity in entities:
                print 'ENTITY: ' + entity
                self.varGlobales.increment_reconognized_entities()
                #logging.debug('ENTIDAD RECONOCIDA -> ' + repr(self.varGlobales.get_reconognized_entities()) + ' - '+ entity)

                additional_information = self._information_source.get_description(entity, string_data)
                if additional_information is not None:
                    wordbag.get_words_list().extend(additional_information)
                    #logging.debug('INFORMACION ADICIONAL AGREGADA')
                    #logging.debug(additional_information)
                print '**********************************'
                #logging.debug('**********************************')
        print ''
        return wordbag

    def _get_entities(self, text):
        print 'TEXTO: ' + text
        logging.debug('TEXTO: ' + text)
        entities = self._ner.get_entities(text)
        if self._ner.ENTITY_ORGANIZATION in entities:
            if entities[self._ner.ENTITY_ORGANIZATION] is not None:
                return entities[self._ner.ENTITY_ORGANIZATION]
            else:
                return None

    def print_count_queries(self):
        self._information_source.getCountEntitys()
        self._information_source.getCountSynsets()

    def get_variablesGlobales(self):
        return self.varGlobales
        
