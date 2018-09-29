import abc

__author__ = 'Tomas Juarez y Damian Dominguez'


class HeuristicAbs(object):
    #
    # Information source abstract class

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate(self, documentText, synsetContext, id):
        pass
    
    def getBetterSentence(self):
        result = None
        maxValue = -1

        #Si solo hay un contexto, se devuelve el contexto con valor nulo(-)
        if(len(self._analyzed_sentences) == 1):
            result = self._analyzed_sentences[0]
            result['value'] = '-'
            return result

        for elem in self._analyzed_sentences:
            if elem['value'] > maxValue:
                maxValue = elem['value']
                result = elem
        return result