import sys
import os.path
import csv

__author__ = 'ignacio'


class WordBag(object):

    def __init__(self, word_list = None):
        self._words = word_list

    def get_words_list(self):
        return self._words

    def get_words_str(self):
        return ' '.join(self._words)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, 'rb') as words_file:
            try:
                words = csv.reader(words_file).next()
            except StopIteration:
                words = ''
        return WordBag(words)

    def save_to_file(self, filepath):
        with open(filepath, 'wb') as words_file:
            writer = csv.writer(words_file)
            writer.writerow(self._words)
