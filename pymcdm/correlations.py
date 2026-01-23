# Copyright (c) 2020-2026 Andrii Shekhovtsov
# Copyright (c) 2021-2026 Bartłomiej Kizielewicz

from functools import wraps
from itertools import permutations
import numpy as np
from warnings import warn

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
    """ Calculate Spearman correlation between two rankings vectors [#spearman1]_.

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

        Notes
        -----
            If either input vector has zero variance, the Spearman correlation is undefined.
            In such cases, a UserWarning is emitted.
            This function can also be used via its alias: rs().

        References
        ----------
        .. [#spearman1] Spearman's rank correlation coefficient, Wikipedia.
               Available at: https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient
    """
    sx = np.std(x)
    sy = np.std(y)
    if sx == 0 or sy == 0:
        warn('Spearman correlation is undefined when one of the vectors has zero variance.', UserWarning)
    return (_cov(x, y)) / (sx * sy)


def rs(x, y):
    """Alias to pymcdm.correlations.spearman() function."""
    return spearman(x, y)


@_correlation_decorator
def pearson(x, y):
    """ Calculate Pearson correlation between two raw vectors [#pearson1]_.

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

        Notes
        -----
            If either input vector has zero variance, the Pearson correlation is undefined.
            In such cases, a UserWarning is emitted.
            This function can also be used via its alias: r().

        References
        ----------
        .. [#pearson1] "Pearson correlation coefficient", Wikipedia,
               Available at: https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    """
    sx = np.std(x)
    sy = np.std(y)
    if sx == 0 or sy == 0:
        warn('Pearson correlation is undefined when one of the vectors has zero variance.', UserWarning)
    return (_cov(x, y)) / (sx * sy)


def r(x, y):
    """Alias to pymcdm.correlations.pearson() function."""
    return pearson(x, y)


@_correlation_decorator
def weighted_spearman(x, y):
    """ Calculate Weighted Spearman correlation between two rankings vectors [#weighted_spearman1]_.

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

        Notes
        -----
            This function can also be used via its alias: rw().

        References
        ----------
        .. [#weighted_spearman1] Pinto da Costa, J., & Soares, C. (2005). A weighted rank measure of correlation.
               Australian & New Zealand Journal of Statistics, 47(4), 515-529.
    """
    N = len(x)
    n = 6 * np.sum((x-y)**2 * ((N - x + 1) + (N - y + 1)))
    d = N**4 + N**3 - N**2 - N
    return 1 - (n/d)


def rw(x, y):
    """Alias to pymcdm.correlations.weighted_spearman() function."""
    return weighted_spearman(x, y)


@_correlation_decorator
def rank_similarity_coef(x, y):
    """ Calculate Rank Similarity Coefficient (WS) between two ranking vectors [#rank_similarity_coef1]_.

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

        Notes
        -----
            This function can also be used via its alias: ws().

        References
        ----------
        .. [#rank_similarity_coef1] Sałabun, W., & Urbaniak, K. (2020, June). A new coefficient of rankings similarity in
               decision-making problems. In International conference on computational science (pp. 632-645).
               Cham: Springer International Publishing.
    """
    N = len(x)
    n = np.fabs(x - y)
    d = np.max((np.fabs(1 - x), np.fabs(N - x)), axis=0)
    return 1 - np.sum(2.0**(-1.0 * x) * n/d)


def ws(x, y):
    """Alias to pymcdm.correlations.rank_similarity_coef() function."""
    return rank_similarity_coef(x, y)


@_correlation_decorator
def kendall_tau(x, y):
    """ Calculate Kendall Tau correlation between two rankings vectors [#kendall_tau1]_.

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

        References
        ----------
        .. [#kendall_tau1] Kendall tau rank correlation coefficient, Wikipedia.
               Available at: https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient
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
        ranking vectors [#goodman_kruskal_gamma1]_.

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

        Notes
        -----
            If there are no comparable pairs (i.e., the denominator is zero), Gamma is undefined.
            In such cases, a UserWarning is emitted.

        References
        ----------
        .. [#goodman_kruskal_gamma1] Goodman and Kruskal's gamma, Wikipedia.
               Available at: https://en.wikipedia.org/wiki/Goodman_and_Kruskal%27s_gamma
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
    if den == 0:
        warn("Goodman's and Kruskal's Gamma is undefined when there are no comparable pairs (denominator is zero).", UserWarning)
    return num / float(den)


@_correlation_decorator
def wsc(w0, w1):
    """ Weights similarity coefficient for measuring the similarity between
        the criteria weights [#wsc1]_.

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

        References
        ----------
        .. [#wsc1] Shekhovtsov, A. (2023). Evaluating the performance of subjective weighting methods for multi-criteria
               decision-making using a novel weights similarity coefficient.
               Procedia Computer Science, 225, 4785-4794.
    """
    return 1 - (np.sum(np.abs(w0 - w1)) / 2 * (1 - np.min(w0)))


@_correlation_decorator
def wsc2(w0, w1):
    """ Weights similarity coefficient for measuring the similarity between
        the criteria weights. This is symmetrical version,
        i.e. wsc2(a, b) == wsc2(b, a) [#wsc21]_.

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

        References
        ----------
        .. [#wsc21] Shekhovtsov, A. (2023). Evaluating the performance of subjective weighting methods for multi-criteria
               decision-making using a novel weights similarity coefficient.
               Procedia Computer Science, 225, 4785-4794.
    """
    return 1 - (np.sum(np.abs(w0 - w1)) / 2 )
