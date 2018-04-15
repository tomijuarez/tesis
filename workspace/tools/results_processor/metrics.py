import numpy as np

__author__ = 'ignacio'


def recall(row, number_of_relevants):
    if number_of_relevants > 0:
    	return row.count(1) / float(number_of_relevants)
    return 0

def average_recall(data, array_of_relevants):
    """
        param data: binary matrix of results
        param array_of_relevants: numbers of relevants per data row
    """
    number_of_rows = len(data)
    avg = 0
    for i in range(len(data)):
        avg += recall(data[i], array_of_relevants[i])
    return avg / float(number_of_rows)

def precision(row, from_n, to_n):
    precision_array = []
    for at in range(from_n, to_n):
        precision_array.append(row[0:at].count(1) / float(at))
    return precision_array

def count_hits(row, from_n, to_n):
    rprecision_array = []
    for at in range(from_n, to_n):
        precision_array.append(row[0:at].count(1))
    return precision_array

def average_precision_q(data, from_n, to_n):
    """
        param data: binary matrix of results
        param from_n: precision at n start
        param to_n: precision at n end (not included)
    """
    avg_array = [0] * (to_n - from_n)
    number_of_rows = len(data)
    for row in data:
        row_precision = precision(row, from_n + 1, to_n + 1)
        avg_array = [x + y for x, y in zip(avg_array, row_precision)]
    return [x / (number_of_rows * i) for x, i in zip(avg_array, range(from_n + 1, to_n + 1))]

def average_precision(data, from_n, to_n):
    """
        param data: binary matrix of results
        param from_n: precision at n start
        param to_n: precision at n end (not included)
    """
    avg_array = [0] * (to_n - from_n)
    number_of_rows = len(data)
    for row in data:
        row_precision = precision(row, from_n + 1, to_n + 1)
        avg_array = [x + y for x, y in zip(avg_array, row_precision)]
    return [x / number_of_rows for x in avg_array]

def average_ndcg(data):
    number_of_rows = len(data)
    avg = 0
    for row in data:
        avg += ndcg_at_k(row, len(data[0]))
    return avg / float(number_of_rows)

def ndcg(data):
    return ndcg_at_k(data, len(data))

def dcg_at_k(r, k, method=0):
    """Score is discounted cumulative gain (dcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
    >>> dcg_at_k(r, 1)
    3.0
    >>> dcg_at_k(r, 1, method=1)
    3.0
    >>> dcg_at_k(r, 2)
    5.0
    >>> dcg_at_k(r, 2, method=1)
    4.2618595071429155
    >>> dcg_at_k(r, 10)
    9.6051177391888114
    >>> dcg_at_k(r, 11)
    9.6051177391888114
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Discounted cumulative gain
    """
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.


def ndcg_at_k(r, k, method=0):
    """Score is normalized discounted cumulative gain (ndcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
    >>> ndcg_at_k(r, 1)
    1.0
    >>> r = [2, 1, 2, 0]
    >>> ndcg_at_k(r, 4)
    0.9203032077642922
    >>> ndcg_at_k(r, 4, method=1)
    0.96519546960144276
    >>> ndcg_at_k([0], 1)
    0.0
    >>> ndcg_at_k([1], 2)
    1.0
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Normalized discounted cumulative gain
    """
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max
