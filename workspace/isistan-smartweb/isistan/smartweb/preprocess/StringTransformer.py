import re
from Transformer import Transformer
from isistan.smartweb.persistence.WordBag import WordBag

__author__ = 'ignacio'


class StringTransformer(Transformer):

    def transform(self, data):
        """'Parses the data extracting words'"""
        return WordBag(re.sub(' +', ' ', re.sub("([a-z])([A-Z])", "\g<1> \g<2>",
                                        re.sub(' +', ' ',
                                               re.sub('[^a-zA-Z ]', ' ', data
                                                      )))).split(' '))
