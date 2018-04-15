import ConfigParser

from sklearn.neighbors import BallTree

from isistan.smartweb.preprocess.text import TfidfVectorizer
from isistan.smartweb.core.SearchEngine import SmartSearchEngine
from isistan.smartweb.preprocess.StringPreprocessorAdapter import StringPreprocessorAdapter
from isistan.smartweb.preprocess.StringTransformer import StringTransformer

__author__ = 'ignacio'


class BallTreeSearchEngine(SmartSearchEngine):
    #
    # Registry implementation using ball-tree

    def __init__(self):
        super(BallTreeSearchEngine, self).__init__()
        self._service_array = []
        self._balltree_index = None
        self._tfidf_matrix = None

    def load_configuration(self, configuration_file):
        super(BallTreeSearchEngine, self).load_configuration(configuration_file)
        
        config = ConfigParser.ConfigParser()
        config.read(configuration_file)
        
        self._metric = config.get('RegistryConfigurations', 'metric').lower()
        self._leaf_size = config.getint('RegistryConfigurations', 'leaf_size')

        self._vectorizer = TfidfVectorizer(sublinear_tf=False,
                                           analyzer='word', lowercase=False, use_bm25idf=self._use_bm25idf,
                                           bm25_tf=self._use_bm25tf, k = self._bm25_k,
                                           preprocessor=StringPreprocessorAdapter())

    def unpublish(self, service):
        pass

    def _preprocess(self, bag_of_words):
        return bag_of_words.get_words_str()

    def _after_publish(self, documents):
        self._tfidf_matrix = self._vectorizer.fit_transform(documents)
        self._balltree_index = BallTree(self._tfidf_matrix.toarray(), leaf_size=self._leaf_size, metric=self._metric)

    def publish(self, service):
        pass

    def find(self, query):
        query = StringTransformer().transform(query)
        query_array = self._vectorizer.transform([self._query_transformer.transform(query).get_words_str()]).toarray()
        result = self._balltree_index.query(query_array, k=len(self._service_array), return_distance=False)
        result_list = []
        for index in result[0]:
            result_list.append(self._service_array[index])
        return result_list

    def number_of_services(self):
        pass
