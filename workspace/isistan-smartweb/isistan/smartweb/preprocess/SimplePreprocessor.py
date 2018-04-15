from Preprocessor import Preprocessor

from nltk.corpus import stopwords

__author__ = 'ignacio'


class SimplePreprocessor(Preprocessor):
    #
    # Freebase query preprocessor

    def __init__(self, stoplist='english'):
        self._stoplist = stopwords.words(stoplist)

    def process_term(self, term):
        stops = set(self._stoplist)
        if term is not None and term not in stops:
            term = term.lower()
            return term
        return None

    def __call__(self, *args):
        terms = []
        data = args[0]
        for term in data:
            processed_term = self.process_term(term)
            if processed_term is not None:
                terms.append(processed_term)
        return terms
