import os
import sys
import ConfigParser
import lucene

from gensim import corpora, models, similarities
 
from java.io import File
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from isistan.smartweb.core.SearchEngine import SearchEngine
from isistan.smartweb.preprocess.StringPreprocessor import StringPreprocessor
from isistan.smartweb.preprocess.WSDLTransformer import WSDLTransformer
from isistan.smartweb.preprocess.StringTransformer import StringTransformer
from isistan.smartweb.preprocess.NERTransformer import NERTransformer
from isistan.smartweb.core.StandfordNER import StandfordNER
from isistan.smartweb.core.SpacyNER import SpacyNER
from isistan.smartweb.core.FreebaseInformationSource import FreebaseInformationSource

__author__ = 'ignacio'


class BM25SearchEngine(SearchEngine):
    #
    # BM25 engine implementation in python

    def __init__(self):
        self._document_expansion = False
        self._semantic_transformer = None
        lucene.initVM()
        self._preprocessor = StringPreprocessor()

    def load_configuration(self, configuration_file):
        config = ConfigParser.ConfigParser()
        config.read(configuration_file)

        if str(config.get('RegistryConfigurations', 'document_expansion')).lower() == 'true':
            freebase_api_key = str(config.get('RegistryConfigurations', 'freebase_api_key'))
            ner = StandfordNER()
            #ner = SpacyNER()
            freebase_source = FreebaseInformationSource(freebase_api_key)
            self._semantic_transformer = NERTransformer(freebase_source, ner)
            self._document_expansion = True

    def unpublish(self, service):
        pass

    def publish_services(self, service_list):
        transformer = WSDLTransformer()
        current_document = 1;
        indexDir = SimpleFSDirectory(File("index/"))
        writerConfig = IndexWriterConfig(Version.LUCENE_CURRENT, EnglishAnalyzer(Version.LUCENE_CURRENT))
        writerConfig.setSimilarity(BM25Similarity())
        index_writer = IndexWriter(indexDir, writerConfig)
        for wsdl in service_list:
            if self._document_expansion:
                #bag_of_words = ' '.join(self._preprocessor(self._semantic_transformer.transform(transformer.transform(wsdl))))
                bag_of_words = ' '.join(self._semantic_transformer.transform(transformer.transform(wsdl)))
            else:
                #bag_of_words = ' '.join(self._preprocessor(transformer.transform(wsdl)))
                bag_of_words = ' '.join(transformer.transform(wsdl))
            doc = Document()
            doc.add(Field("content", bag_of_words, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("path", wsdl, Field.Store.YES, Field.Index.NO))
            index_writer.addDocument(doc)
            current_document += 1
        index_writer.close()

    def publish(self, service):
        pass

    def find(self, query):
        transformer = StringTransformer()
        analyzer = EnglishAnalyzer(Version.LUCENE_CURRENT)
        reader = IndexReader.open(SimpleFSDirectory(File("index/")))
        searcher = IndexSearcher(reader)
        searcher.setSimilarity(BM25Similarity())
        processed_query = ' '.join(self._preprocessor(transformer.transform(query)))
        query = QueryParser(Version.LUCENE_CURRENT, "content", analyzer).parse(processed_query)
        hits = searcher.get_description(query, 10)
        result_list = []
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            result_list.append(doc.get("path").encode("utf-8"))
        return result_list

    def number_of_services(self):
        pass
