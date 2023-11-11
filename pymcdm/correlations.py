# Copyright (c) 2020-2023 Andrii Shekhovtsov
# Copyright (c) 2021 Bartłomiej Kizielewicz

from functools import wraps
from itertools import permutations
import numpy as np

__all__ = [
    'spearman',
    'rs',
    'pearson',
    'r',
    'weighted_spearman',
    'rw',
    'rank_similarity_coef',
    'ws',
    'kendall_tau',
    'goodman_kruskal_gamma',
    'draws',
    'wsc',
    'wsc2'
]

def _correlation_decorator(func):
    @wraps(func)
    def wrapped(x, y):
        x = np.array(x)
        y = np.array(y)
        return func(x, y)
    return wrapped


def _cov(x, y):
    return np.cov(x, y, bias=True)[0][1]


@_correlation_decorator
def spearman(x, y):
    """ Calculate Spearman correlation between two rankings vectors.

        Parameters
        ----------
            x : ndarray
                First vector of ranks.

            y : ndarray
                Second vector of ranks.

        Returns
        -------
            float
                Correlation between two rankings vectors.
    """
    return (_cov(x, y)) / (np.std(x) * np.std(y))

rs = spearman


@_correlation_decorator
def pearson(x, y):
    """ Calculate Pearson correlation between two raw vectors.

        Parameters
        ----------
            x : ndarray
                First vector with raw values.

            y : ndarray
                Second vector with raw values.

        Returns
        -------
            float
                Correlation between two vectors.
    """
    return (_cov(x, y)) / (np.std(x) * np.std(y))

r = pearson


@_correlation_decorator
def weighted_spearman(x, y):
    """ Calculate Weighted Spearman correlation between two rankings vectors.

        Parameters
        ----------
            x : ndarray
                First vector of ranks.

            y : ndarray
                Second vector of ranks.

        Returns
        -------
            float
                Correlation between two rankings vectors.
    """
    N = len(x)
    n = 6 * np.sum((x-y)**2 * ((N - x + 1) + (N - y + 1)))
    d = N**4 + N**3 - N**2 - N
    return 1 - (n/d)

rw = weighted_spearman


@_correlation_decorator
def rank_similarity_coef(x, y):
    """ Calculate Rank Similarity Coefficient (WS) between two ranking vectors.

        Parameters
        ----------
            x : ndarray
                First vector of ranks.

            y : ndarray
                Second vector of ranks.

        Returns
        -------
            float
                Correlation between two rankings vectors.
    """
    N = len(x)
    n = np.fabs(x - y)
    d = np.max((np.fabs(1 - x), np.fabs(N - x)), axis=0)
    return 1 - np.sum(2.0**(-1.0 * x) * n/d)

ws = rank_similarity_coef


@_correlation_decorator
def kendall_tau(x, y):
    """ Calculate Kendall Tau correlation between two rankings vectors.

        Parameters
        ----------
            x : ndarray
                First vector of ranks.

            y : ndarray
                Second vector of ranks.

        Returns
        -------
            float
                Correlation between two rankings vectors.
    """
    n = len(x)
    res = 0
    for j in range(n):
        for i in range(j):
            res += np.sign(x[i] - x[j]) * np.sign(y[i] - y[j])
    return 2/(n*(n-1)) * res


@_correlation_decorator
def goodman_kruskal_gamma(x, y):
    """ Calculate Goodman's and Kruskal's Gamma correlation between two
        ranking vectors.

        Parameters
        ----------
            x : ndarray
                First vector of ranks.

            y : ndarray
                Second vector of ranks.

        Returns
        -------
            float
                Correlation between two rankings vectors.
    """
    num = 0
    den = 0
    for i, j in permutations(range(len(x)), 2):
        x_dir = x[i] - x[j]
        y_dir = y[i] - y[j]
        sign = np.sign(x_dir * y_dir)
        num += sign
        if sign:
            den += 1
    return num / float(den)


@_correlation_decorator
def draws(x, y):
    """ Calculate drastic WS distance between the ranking vectors.
        Rankings should be presented as indices, i.e. for the ranking
        A2 > A1 > A3 the ranking vector should be [2, 1, 3].

        Parameters
        ----------
            x : ndarray
                First vector of ranks.

            y : ndarray
                Second vector of ranks.

        Returns
        -------
            float
                Drastic distance between two rankings vectors.
    """
    return sum(2 ** -i * int(xi != yi)
               for i, (xi, yi) in enumerate(zip(x, y), 1)) / (1 - 2**(-len(x)))


@_correlation_decorator
def wsc(w0, w1):
    """ Weights similarity coefficient for measuring the similarity between
        the criteria weights.

        Parameters
        ----------
            w0 : ndarray
                First vector of weights.

            w1 : ndarray
                Second vector of weights.

        Returns
        -------
            float
                The similarity of the weights in range [0, 1], where 0 is
                different weights, and 1 is the same weights.
    """
    return 1 - (np.sum(np.abs(w0 - w1)) / 2 * (1 - np.min(w0)))


@_correlation_decorator
def wsc2(w0, w1):
    """ Weights similarity coefficient for measuring the similarity between
        the criteria weights. This is symmetrical version,
        i.e. wsc2(a, b) == wsc2(b, a).

        Parameters
        ----------
            w0 : ndarray
                First vector of weights.

            w1 : ndarray
                Second vector of weights.

        Returns
        -------
            float
                The similarity of the weights in range [0, 1], where 0 is
                different weights, and 1 is the same weights.
    """
    return 1 - (np.sum(np.abs(w0 - w1)) / 2 )
