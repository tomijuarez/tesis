import random
import numpy as np

from sklearn.cluster.k_means_ import *
from sklearn.utils import check_array
from sklearn.utils import check_random_state
from sklearn.utils.validation import check_is_fitted


__author__ = 'ignacio'


def _divide_matrix(X, labels):
    X_first = []
    X_second = []
    for x in range(0, len(labels)):
        if labels[x] == 0:
            X_first.append(X[x])
        elif labels[x] == 1:
            X_second.append(X[x])
    X1 = np.array(X_first)
    X2 = np.array(X_second)
    return (X1, X2)

def _next_cluster(clusters):
    return random.randint(0, len(clusters)-1)

class BisectingKMeans(KMeans):
    #
    # Registry implementation using clusters

    def __init__(self, n_clusters=8, init='k-means++', n_init=10, max_iter=300,
                 tol=1e-4, precompute_distances='auto',
                 verbose=0, random_state=None, copy_x=True, n_jobs=1):
        self.n_clusters = n_clusters
        self.init = init
        self.max_iter = max_iter
        self.tol = tol
        self.precompute_distances = precompute_distances
        self.n_init = n_init
        self.verbose = verbose
        self.random_state = random_state
        self.copy_x = copy_x
        self.n_jobs = n_jobs
        self._cluster_centers_ = []

    def _check_fit_data(self, X):
        """Verify that the number of samples given is larger than k"""
        X = check_array(X, accept_sparse='csr', dtype=np.float64)
        if X.shape[0] < self.n_clusters:
            raise ValueError("n_samples=%d should be >= n_clusters=%d" % (
                X.shape[0], self.n_clusters))
        return X

    def _check_test_data(self, X):
        X = check_array(X, accept_sparse='csr', dtype=FLOAT_DTYPES,
                        warn_on_dtype=True)
        n_samples, n_features = X.shape
        expected_n_features = self.cluster_centers_.shape[1]
        if not n_features == expected_n_features:
            raise ValueError("Incorrect number of features. "
                             "Got %d features, expected %d" % (
                                 n_features, expected_n_features))
        return X

    def fit(self, X, y=None):
        """Compute k-means clustering.
        Parameters
        ----------
        X : array-like or sparse matrix, shape=(n_samples, n_features)
        """
        X = self._check_fit_data(X)
        initial_X = X
        self._clusters = [X]
        current_clusters = 1
        self.cluster_centers_ = []
        while current_clusters <= self.n_clusters:
            random_state = check_random_state(self.random_state)
            cluster_index = _next_cluster(self._clusters)
            X = self._clusters[cluster_index]
            cluster_centers, labels, self.inertia_, self.n_iter_ = \
                k_means(
                        X, n_clusters=2, init=self.init,
                        n_init=self.n_init, max_iter=self.max_iter,
                        verbose=self.verbose, return_n_iter=True,
                        precompute_distances=self.precompute_distances,
                        tol=self.tol, random_state=random_state, copy_x=self.copy_x,
                        n_jobs=self.n_jobs)
            X1, X2 = _divide_matrix(X, labels)
            self.cluster_centers_.extend(cluster_centers)
            del self.cluster_centers_[cluster_index]
            del self._clusters[cluster_index]
            self._clusters.append(X1)
            self._clusters.append(X2)
            current_clusters += 1
        self.labels_ = []
        self.cluster_centers_ = np.array(self.cluster_centers_)
        for x in range(0, len(initial_X)):
            self.labels_.append(self.predict(initial_X[x].reshape(-1, self.cluster_centers_.shape[1]))[0])
