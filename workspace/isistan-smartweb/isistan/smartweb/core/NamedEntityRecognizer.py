import abc

__author__ = 'ignacio'


class NamedEntityRecognizer(object):

    #
    # Information source abstract class

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_entities(self, text):
        pass