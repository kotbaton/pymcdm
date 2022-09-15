# Copyright (c) 2020 Andrii Shekhovtsov
# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from itertools import permutations

__all__ = [
    'spearman',
    'pearson',
    'weighted_spearman',
    'rank_similarity_coef',
    'kendall_tau',
    'goodman_kruskal_gamma',
    'correlation_matrix'
]


def _cov(x, y):
    return np.cov(x, y, bias=True)[0][1]


def spearman(x, y):
    """Calculate Spearman correlation between two rankings vectors.

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


def pearson(x, y):
    """Calculate Pearson correlation between two raw vectors.

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


def weighted_spearman(x, y):
    """Calculate Weighted Spearman correlation between two rankings vectors.

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


def rank_similarity_coef(x, y):
    """Calculate Rank Similarity Coefficient (WS) between two rankings vectors.

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


def kendall_tau(x, y):
    """Calculate Kendall Tau correlation between two rankings vectors.

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


def goodman_kruskal_gamma(x, y):
    """Calculate Goodman's and Kruskal's Gamma correlation between two rankings vectors.

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


def correlation_matrix(rankings, method, columns=False):
    """Creates a correlation matrix for given vectors from the numpy array.

    Parameters
    ----------
        rankings : ndarray
            Vectors for which the correlation matrix is to be calculated.

        method : callable
            Function to calculate the correlation matrix.

        columns: bool
            If the column value is set to true then the correlation matrix will be calculated for the columns.
            Otherwise the matrix will be calculated for the rows.

    Returns
    -------
        ndarray
            Correlation between two rankings vectors.
    """
    rankings = np.array(rankings)
    if columns:
        rankings = rankings.T
    n = rankings.shape[0]
    corr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            corr[i, j] = method(rankings[i], rankings[j])
    return corr
