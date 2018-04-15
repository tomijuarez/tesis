import abc

__author__ = 'ignacio'


class Preprocessor(object):
    #
    # Abstract preprocessor

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def process_term(self, term):
        pass
