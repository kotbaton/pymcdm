# Copyright (c) 2021 Andrii Shekhovtsov
# Copyright (c) 2022 Bartłomiej Kizielewicz

import numpy as np
from collections import Counter

__all__ = [
    'rankdata',
    'rrankdata',
    'correlation_matrix',
    'normalize_matrix'
]


def rankdata(a, reverse=False):
    """
    Assign ranks to data in vector `a`.

    Ranks begin at 1. Tied elements get average rank (see Examples below).

    Ranking starts from smaller values, e.g. the smaller element get
    the first position. The `reverse` argument reverse posisions, e.g.
    the largest element get first position.

    Parameters
    ----------
    a : iterable
        The array of values to be ranked.

    reverse : bool, optional
        If True, larger elements get first posisions in ranking.
        If False, smaller elements get first positions in ranking.

    Returns
    -------
    ndarray
        An array of rank scores for the input data.

    Examples
    --------
    >>> from pymcdm.helpers import rankdata
    >>> rankdata([0, 3, 2, 5])
    array([1, 3, 2, 4])
    >>> rankdata([0, 3, 2, 5], reverse=True)
    array([4, 2, 3, 1])
    >>> rankdata([0, 3, 2, 3])
    array([1. , 3.5, 2. , 3.5])
    >>> rankdata([0, 3, 2, 3], reverse=True)
    array([4. , 1.5, 3. , 1.5])
    """
    c = Counter(a)
    rv = {}
    i = 1
    for k in sorted(c.keys(), reverse=reverse):
        if c[k] == 1:
            rv[k] = i
            i += 1
        else:
            v = c[k]
            rv[k] = (2*i + v - 1)/2
            i += v
    return np.array([rv[k] for k in a], dtype='float')


def rrankdata(a):
    """Alias to `rankdata(a, reverse=True)`. See `rankdata` for details."""
    return rankdata(a, reverse=True)


def correlation_matrix(rankings, method, columns=False):
    """ Creates a correlation matrix for given vectors from the numpy array.

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
    if columns:
        rankings = rankings.T
    n = rankings.shape[0]
    corr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            corr[i, j] = method(rankings[i], rankings[j])
    return corr


def normalize_matrix(matrix, method, criteria_types):
    """ Normalize each column in `matrix`, using `normalization` function according `criteria_types`.

        Parameters
        ----------
            matrix : ndarray
                Decision matrix representation.
                The rows are considered as alternatives and the columns are considered as criteria.

            normalization : callable
                Function which should be used for normalize `matrix` columns.
                It should match signature `foo(x, cost)`, where `x` is a vector which would be normalized and `cost` is
                a bool variable which says if `x` is a cost or profit criteria.

            criteria_types : None or ndarray
                Describes criteria types.
                1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.
                If None all criteria are considered as profit

        Returns
        -------
            ndarray
                Normalized copy of the input matrix.

        Raises
        ------
            ValueError
                If `criteria_types` and `matrix` has different number of criteria.
    """
    if criteria_types is None:
        nmatrix = matrix.astype('float')
        for i in range(matrix.shape[1]):
            nmatrix[:, i] = method(matrix[:, i], cost=False)
        return nmatrix

    if matrix.shape[1] != len(criteria_types):
        raise ValueError(f'Matrix has {matrix.shape[1]} criteria and criteria_types has {len(criteria_types)}. This '
                         f'values must be equal.')

    nmatrix = matrix.astype('float')
    for i, type in enumerate(criteria_types):
        if type == 1:  # If profit
            nmatrix[:, i] = method(matrix[:, i], cost=False)
        else:
            nmatrix[:, i] = method(matrix[:, i], cost=True)
    return nmatrix
