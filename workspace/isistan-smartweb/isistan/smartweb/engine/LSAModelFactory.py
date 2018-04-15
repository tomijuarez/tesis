from ModelFactory import ModelFactory
from gensim.models import LsiModel

__author__ = 'ignacio'


class LSAModelFactory(ModelFactory):
    #
    # Creates an Latent Semantic Analysis model

    def create(self, corpus, dictionary, number_of_topics):
        return LsiModel(corpus, id2word=dictionary,
                        num_topics=number_of_topics)