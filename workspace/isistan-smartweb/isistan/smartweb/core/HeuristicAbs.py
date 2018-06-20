import abc

__author__ = 'Tomas Juarez y Damian Dominguez'


class HeuristicAbs(object):
    #
    # Information source abstract class

    __metaclass__ = abc.ABCMeta

    synsetContext = ''
    documentText = ''
    analyzed_sentences = []

    @abc.abstractmethod
    def calculate(self):
        pass

    def setSysntexContext(self,synsetContext):
        self.synsetContext = synsetContext

    def setDocumentText(self, documentText):
        self.documentText = documentText
    
    @abc.abstractmethod
    def getBetterSentence(self):
        pass
