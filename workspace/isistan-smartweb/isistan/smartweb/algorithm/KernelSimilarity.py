from gensim import similarities, interfaces, utils, matutils
import numpy
import scipy

class KernelSimilarity(similarities.MatrixSimilarity):
    """
    Compute similarity against a corpus of documents by storing the index matrix
    in memory. The similarity measure used is cosine between two vectors.
    Use this if your input corpus contains dense vectors (such as documents in LSI
    space) and fits into RAM.
    The matrix is internally stored as a *dense* numpy array. Unless the entire matrix
    fits into main memory, use `Similarity` instead.
    See also `Similarity` and `SparseMatrixSimilarity` in this module.
    """

    def __init__(self, corpus, num_best=None, dtype=numpy.float32, num_features=None, chunksize=256, corpus_len=None, kernel_function= None):
        """
        `num_features` is the number of features in the corpus (will be determined
        automatically by scanning the corpus if not specified). See `Similarity`
        class for description of the other parameters.
        """
        self.kernel = kernel_function
        super(KernelSimilarity, self).__init__(corpus, num_best, dtype, num_features, chunksize, corpus_len)

    def get_similarities(self, query):
        """
        Return similarity of sparse vector `query` to all documents in the corpus,
        as a numpy array.
        If `query` is a collection of documents, return a 2D array of similarities
        of each document in `query` to all documents in the corpus (=batch query,
        faster than processing each document in turn).
        **Do not use this function directly; use the self[query] syntax instead.**
        """
        is_corpus, query = utils.is_corpus(query)
        if is_corpus:
            query = numpy.asarray(
                [matutils.sparse2full(vec, self.num_features) for vec in query],
                dtype=self.index.dtype)
        else:
            if scipy.sparse.issparse(query):
                query = query.toarray()  # convert sparse to dense
            elif isinstance(query, numpy.ndarray):
                pass
            else:
                # default case: query is a single vector in sparse gensim format
                query = matutils.sparse2full(query, self.num_features)
            query = numpy.asarray(query, dtype=self.index.dtype)

        result = (self.kernel(self.index, query.T) / ((self.kernel(self.index, self.index.T).diagonal() * self.kernel(query, query.T)) ** 0.5))
        return result  # XXX: removed casting the result from array to list; does anyone care?
