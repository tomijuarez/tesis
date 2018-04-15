from Preprocessor import Preprocessor
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

__author__ = 'ignacio'


class PorterPreprocessor(Preprocessor):

    def __init__(self, stoplist):
        self._stemmer = PorterStemmer()
        self._stoplist = stopwords.words(stoplist)

    def process_term(self, term):
        stem_term = None
        term = term.lower()
        stops = set(self._stoplist)
        if term is not None and term not in stops:
            stem_term = self._stemmer.stem(term)
        return stem_term
