from Transformer import Transformer
from isistan.smartweb.persistence.WordBag import WordBag

import collections

from nltk.corpus import wordnet
from os.path import join

__author__ = 'ignacio'


class CombineTransformer(Transformer):

    def __init__(self, transformer1, transformer2):
        self._transformer1 = transformer1
        self._transformer2 = transformer2

    def set_transformer1(transformer1):
        self._transformer1 = transformer1

    def set_transformer2(transformer2):
        self._transformer2 = transformer2

    def get_transformer1():
        return self._transformer1

    def get_transformer2():
        return self._transformer2

    def transform(self, wordbag):
        return self._transformer1.transform(self._transformer2.transform(wordbag))