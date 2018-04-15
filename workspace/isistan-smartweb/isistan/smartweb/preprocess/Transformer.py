import abc

__author__ = 'ignacio'


class Transformer(object):
    #
    # Transforms data

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def transform(self, data):
        pass
