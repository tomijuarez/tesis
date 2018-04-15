from StringPreprocessor import StringPreprocessor

__author__ = 'ignacio'


class StringPreprocessorAdapter(StringPreprocessor):
    #
    # String query preprocessor

    def __init__(self, stoplist='english'):
        super(StringPreprocessorAdapter, self).__init__(stoplist)

    def __call__(self, *args):
        terms = []
        data = args[0].split(' ')
        return ' '.join(super(StringPreprocessorAdapter, self).__call__(data))
