from Transformer import Transformer
from isistan.smartweb.persistence.WordBag import WordBag

import collections

from nltk.corpus import wordnet
from os.path import join

__author__ = 'ignacio'


class DimensionalityTransformer(Transformer):

    def __init__(self):
        self._synonyms = collections.OrderedDict()

    def fit(self, service_list, transformer=None):
        for document in service_list:
            if transformer:
                word_bag = transformer.transform(document)
            else:
                word_bag = WordBag().load_from_file(join(self._corpus_path,
                                                    self._get_document_filename(document)))
            word_list = word_bag.get_words_list()
            self._fit(word_list)

    def _fit(self, word_list):
        for word in word_list:
            if word.lower() not in self._synonyms:
                synonyms = self._get_synonyms(word.lower())
                if len(synonyms) > 0:
                    for syn in synonyms:
                        self._synonyms[syn.replace('_', ' ')] = word.lower()

    def _get_synonyms(self, term):
        syn_set = set()
        synsets = wordnet.synsets(term)
        for term in synsets:
            syn_set.add(term.lemma_names()[0])
        return syn_set

    def transform(self, wordbag):
        word_list = list(wordbag.get_words_list())
        processed = set()
        word_str = wordbag.get_words_str().lower()
        for word in word_list:
            if word.lower() not in processed:
                if word.lower() in self._synonyms:
                    word_str = word_str.replace(word.lower(), self._synonyms[word.lower()])
                processed.add(word.lower())
        return WordBag(word_str.split(' '))
