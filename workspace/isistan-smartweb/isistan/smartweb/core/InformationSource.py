import abc

__author__ = 'ignacio'


class InformationSource(object):
    #
    # Information source abstract class

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_description(self, query):
        pass

    @abc.abstractmethod
    def get_type(self, query):
        pass

    @abc.abstractmethod
    def get_aka(self, query):
        pass
