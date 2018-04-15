from PorterPreprocessor import PorterPreprocessor

__author__ = 'ignacio'


class StringPreprocessor(PorterPreprocessor):
    #
    # String query preprocessor

    def __init__(self, stoplist='english'):
        super(StringPreprocessor, self).__init__(stoplist)

    def __call__(self, *args):
        terms = []
        data = args[0]
        for term in data:
            processed_term = self.process_term(term)
            if processed_term is not None:
                terms.append(processed_term)
        return terms
