from sklearn.neural_network import BernoulliRBM
from sklearn.neighbors import NearestNeighbors

from isistan.smartweb.preprocess.text import TfidfVectorizer
from isistan.smartweb.core.SearchEngine import SmartSearchEngine
from isistan.smartweb.preprocess.StringPreprocessorAdapter import StringPreprocessorAdapter
from isistan.smartweb.preprocess.StringTransformer import StringTransformer

__author__ = 'ignacio'


class BernoulliRBMSearchEngine(SmartSearchEngine):
    #
    # Registry implementation using ball-tree

    def __init__(self):
        super(BernoulliRBMSearchEngine, self).__init__()
        self._service_array = []
        self._bernoulliRBM_index = None
        self._tfidf_matrix = None

    def load_configuration(self, configuration_file):
        super(BernoulliRBMSearchEngine, self).load_configuration(configuration_file)

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
        self._bernoulliRBM = BernoulliRBM(learning_rate=1)
        self._rbm_matrix = self._bernoulliRBM.fit_transform(self._tfidf_matrix)
        self._bernoulliRBM_index = NearestNeighbors(len(self._service_array), algorithm='brute', metric='euclidean')
        self._bernoulliRBM_index.fit(self._rbm_matrix)


    def publish(self, service):
        pass

    def find(self, query):
        query = StringTransformer().transform(query)
        query_array = self._vectorizer.transform([self._query_transformer.transform(query).get_words_str()])
        query_array = self._bernoulliRBM.transform(query_array.toarray())
        result = self._bernoulliRBM_index.kneighbors(query_array, return_distance=False)[0]
        result_list = []
        for index in result:
            result_list.append(self._service_array[index])
        return result_list

    def number_of_services(self):
        pass
