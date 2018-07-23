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
        for elem in self._analyzed_sentences:
            #logging.debug(str(elem['value']) + ' - ' + str(elem['sentence']))
            if elem['value'] > maxValue:
                maxValue = elem['value']
                result = elem
        #logging.debug('sentencia elegida: ')
        #logging.debug(result['sentence'])
        return result