from ModelFactory import ModelFactory
from gensim.models import LdaModel

__author__ = 'ignacio'


class LDAModelFactory(ModelFactory):
    #
    # Creates an Latent Dirichlet Allocation model

    def create(self, corpus, dictionary, number_of_topics):
        return LdaModel(corpus, id2word=dictionary,
                        num_topics=number_of_topics)