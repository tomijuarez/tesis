from Transformer import Transformer

from nltk.corpus import wordnet

__author__ = 'ignacio'


class WordNetTransformer(Transformer):

    def transform(self, wordbag):
        word_list = list(wordbag.get_words_list())
        for word in word_list:
            synsets = wordnet.synsets(word)
            if len(synsets) > 0:
                lemmas = synsets[0].lemmas()
                if len(lemmas) == 1 and lemmas[0].name() == word and len(synsets) > 1:
                    lemmas = synsets[1].lemmas()
                wordbag.get_words_list().extend([lemma.name().replace('_', ' ') for lemma in lemmas])
        return wordbag