import abc
import ConfigParser

from os.path import join

from isistan.smartweb.persistence.WordBag import WordBag
from isistan.smartweb.preprocess.DummyTransformer import DummyTransformer
from isistan.smartweb.preprocess.WADLTransformer import WADLTransformer
from isistan.smartweb.preprocess.WSDLTransformer import WSDLTransformer
from isistan.smartweb.preprocess.WSDLSimpleTransformer import WSDLSimpleTransformer
from isistan.smartweb.preprocess.NERTransformer import NERTransformer
from isistan.smartweb.preprocess.WordNetTransformer import WordNetTransformer
from isistan.smartweb.preprocess.DimensionalityTransformer import DimensionalityTransformer
from isistan.smartweb.preprocess.CombineTransformer import CombineTransformer
from isistan.smartweb.core.FreebaseInformationSource import FreebaseInformationSource
from isistan.smartweb.core.BabelInformationSource import BabelInformationSource
from isistan.smartweb.core.StandfordNER import StandfordNER

from isistan.smartweb.preprocess.variablesGlobales import variablesGlobales

import logging


__author__ = 'ignacio'


class SearchEngine(object):
    #
    # Search engine abstract class


    logging.basicConfig(filename='ner.log',
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s: %(message)s")

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def publish(self, service):
        pass

    @abc.abstractmethod
    def publish_services(self, service_list):
        pass

    @abc.abstractmethod
    def unpublish(self, service):
        pass

    @abc.abstractmethod
    def number_of_services(self):
        pass

    @abc.abstractmethod
    def find(self, query):
        pass


class SmartSearchEngine(SearchEngine):
    #
    # Smart Search engine base abstract class

    def __init__(self):
        self._document_expansion = False
        self._load_corpus_from_file = False
        self._save_corpus = False
        self._document_transformer = None
        self._query_transformer = None
        self._use_bm25tf = False
        self._use_bm25idf = False
        self._bm25_k = 1.2
        self._use_wordnet = False
        self._dimensionality_reduction = False

    def _get_document_filename(self, document):
        document_filename = document.split('/')
        return document_filename[len(document_filename)-1].split('.')[0]

    def _create_document_transformer(self, document_list):
        if len(document_list) > 0:
            document = document_list[0].split('.')
            extension = document[len(document)-1].lower()
            if extension == 'wadl':
                return WADLTransformer()
            elif extension == 'wsdl':
                return WSDLTransformer()
            elif self._use_wordnet:
                return WSDLSimpleTransformer()
        print 'Invalid document dataset'
        logging.debug('Invalid document dataset')
        return None

    @abc.abstractmethod
    def _after_publish(self, documents):
        pass

    @abc.abstractmethod
    def _preprocess(self, bag_of_words):
        pass

    def publish_services(self, service_list):
        transformer = self._create_document_transformer(service_list)
        documents = []
        current_document = 1


        var = variablesGlobales()
        if self._dimensionality_reduction:
            if self._load_corpus_from_file:
                self._document_transformer.get_transformer1().fit(service_list, transformer)
            else:
                self._document_transformer.get_transformer1().fit(service_list)

        for document in service_list:
            if (current_document == 47):
                print 'Loading document ' + str(current_document) + ' of ' + str(len(service_list))
                logging.debug('Loading document ' + str(current_document) + ' of ' + str(len(service_list)))

                if self._load_corpus_from_file:
                    if self._document_expansion:
                        bag = WordBag().load_from_file(join(self._corpus_path, self._get_document_filename(document)))
                        bag_of_words = self._document_transformer.transform(bag)
                    else:
                        bag_of_words = WordBag().load_from_file(join(self._corpus_path, self._get_document_filename(document)))
                else:
                    if self._document_expansion:
                        bag_of_words = self._document_transformer.transform(transformer.transform(document))
                    else:
                        bag_of_words = transformer.transform(document)
                if self._save_corpus:
                    bag_of_words.save_to_file(join(self._corpus_path, self._get_document_filename(document)))
                documents.append(self._preprocess(bag_of_words))
                self._service_array.append(document)
            self._document_transformer.get_variablesGlobales().increment_current_document()
            current_document += 1

        var = self._document_transformer.get_variablesGlobales()
        var.exports_rows()
        self._after_publish(documents)
        self._document_transformer.print_count_queries()

    def load_configuration(self, configuration_file):
        config = ConfigParser.ConfigParser()
        config.read(configuration_file)

        if config.get('RegistryConfigurations', 'load_corpus_from_file').lower() == 'true':
            self._load_corpus_from_file = True
            self._corpus_path = config.get('RegistryConfigurations', 'corpus_path')

        if config.get('RegistryConfigurations', 'save_corpus').lower() == 'true':
            self._save_corpus = True
            self._corpus_path = config.get('RegistryConfigurations', 'corpus_path')

        if config.get('RegistryConfigurations', 'ner_expansion').lower() == 'true':
            kdb_api_key = config.get('RegistryConfigurations', 'kdb_api_key')

            ner = StandfordNER()

            kdb_source_opt = config.get('RegistryConfigurations', 'kdb_source').lower()
            if kdb_source_opt == 'freebase':
                knowledge_source = FreebaseInformationSource(kdb_api_key)
            else:
                knowledge_source = BabelInformationSource(kdb_api_key)


            self._document_transformer = NERTransformer(knowledge_source, ner)
            var = variablesGlobales()
            self._document_transformer.setVarGlobales(var)
            self._document_expansion = True

        if config.get('RegistryConfigurations', 'wordnet_expansion').lower() == 'true':
            self._document_transformer = WordNetTransformer()
            self._use_wordnet = True
            self._document_expansion = True

        if config.get('RegistryConfigurations', 'dimensionality_reduction').lower() == 'true':
            if self._document_transformer:
                self._document_transformer = CombineTransformer(DimensionalityTransformer(), self._document_transformer)
            else:
                self._document_transformer = DimensionalityTransformer()
                self._dimensionality_reduction = True
                self._document_expansion = True

        if config.get('RegistryConfigurations', 'wordnet_query_expansion').lower() == 'true':
            self._query_transformer = WordNetTransformer()
        else:
            self._query_transformer = DummyTransformer()

        if config.has_option('RegistryConfigurations', 'use_bm25idf'):
            if config.get('RegistryConfigurations', 'use_bm25idf').lower() == 'true':
                self._use_bm25idf = True

        if config.has_option('RegistryConfigurations', 'use_bm25tf'):
            if config.get('RegistryConfigurations', 'use_bm25tf').lower() == 'true':
                self._bm25_k = config.getfloat('RegistryConfigurations', 'bm25_k')
                self._use_bm25tf = True
