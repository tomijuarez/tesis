from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from Preprocessor import Preprocessor

__author__ = 'ignacio'


class SnowballPreprocessor(Preprocessor):

    def __init__(self):
        self._stemmer = SnowballStemmer('english')

    def process_term(self, term):
        stem_term = None
        term = term.lower()
        stops = set(stopwords.words('english'))
        if term is not None and term not in stops:
            stem_term = self._stemmer.stem(term)
        return stem_term
