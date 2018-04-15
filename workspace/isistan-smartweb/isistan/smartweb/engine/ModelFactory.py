import abc

__author__ = 'ignacio'


class ModelFactory(object):
    #
    # Abstract model factory

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, corpus, dictionary, number_of_topics):
        pass
