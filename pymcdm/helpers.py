# Copyright (c) 2021 Andrii Shekhovtsov
# Copyright (c) 2022 Bartłomiej Kizielewicz

import numpy as np
from collections import Counter

__all__ = [
    'rankdata',
    'rrankdata',
    'correlation_matrix',
    'normalize_matrix',
    'leave_one_out_rr'
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


def leave_one_out_rr(method, matrix, weights, types,
                     corr_function,
                     ideal_corr_value=1,
                     only_rr=True):
    """ Function which implements the procedure similar to leave one out cross
        validation. This function calculates N rankings from N decision
        matrices created by removing one of N alternatives from original one.
        This function returns the array of rankings build in following way:
        [original_ranking, w/o A1, w/o A2, ..., w/o AN, original_ranking].

        This function will insert in the ranking value 0 instead of removed
        alternative position. E.g. original ranking is [1, 2, 3, 4], ranking
        without A1 will looks like [0, 1, 2, 3].

        This function main purpose is to prepare data for rankings_flow
        visualization function.

        Parameters
        ----------
            method : MCDA_method
                MCDA method which should be used to calculate rankings.

            matrix : ndarray
                Decision matrix / alternatives data.
                Alternatives are in rows and Criteria are in columns.

            weights : ndarray
                Criteria weights. Sum of the weights should be 1. (e.g. sum(weights) == 1)

            types : ndarray
                Array with definitions of criteria types:
                1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.

            corr_function : Callable
                Correlation function to calculate correlation value between
                rankings.

            ideal_corr_value : float
                Correlation value for ideal ranking. Default is 1. Use it if
                correlation function you use has different value for two same
                rankings (e.g. 0).

            only_rr : bool
                Include in returned collections only rankings in which 
                rank reversal occurs. If rank reversal do not occured the list
                of two original rankings will be returned. Default is True.

        Returns
        -------
            rankings : ndarray
                Matrix of rankings obtained when removing different
                alternatives. Instead of removed alternatives 0 is placed.

            correlations : list
                List of correlation values calculated for rankings in
                `rankings` matrix.

            labels : list
                Names of the created rankings. It will looks like ['None', 
                'w/o A_1', 'w/o A_2', ... 'None'], where 'w/o A_i' means that
                this ranking was build without alternative A_i.

        Examples
        --------
        >>> import numpy as np
        >>> import pymcdm as pm
        >>> matrix = np.array([
        ...     [1, 9, 3, 4, 2],
        ...     [3, 2, 1, 6, 1],
        ...     [4, 6, 3, 2, 1],
        ...     [1, 2, 3, 4, 7],
        ...     [3, 2, 4, 5, 1]
        ... ])
        >>> topsis = pm.methods.TOPSIS()
        >>> weights = np.ones(5)/5
        >>> types = np.ones(5)
        >>> rankings, cors, labels = leave_one_out_rr(
        ...         topsis,
        ...         matrix,
        ...         weights,
        ...         types, 
        ...         pm.correlations.weighted_spearman,
        ...         only_rr=False)
        >>> print(labels, cors, rankings)

    """
    true_pref = method(matrix, weights, types)
    true_rank = method.rank(true_pref)

    rr_ranks = [(None, true_rank)]
    corr_values = [ideal_corr_value]

    for i in range(matrix.shape[0]):
        indices = list(range(i)) + list(range(i + 1, matrix.shape[0]))

        matrix1 = matrix[indices]

        pref = true_pref[indices]
        pref1 = method(matrix1, weights, types)

        rank = method.rank(pref)
        rank1 = method.rank(pref1)

        cr = corr_function(rank, rank1)
        rank1 = list(rank1)
        rank1.insert(i, 0)

        if only_rr:
            if cr != ideal_corr_value:
                rr_ranks.append((i, rank1))
                corr_values.append(cr)
        else:
            rr_ranks.append((i, rank1))
            corr_values.append(cr)

    rr_ranks.append((None, true_rank))
    removed_alts, rankings = zip(*rr_ranks)
    labels = [f'w/o $A_{{{i + 1}}}$' if i is not None else 'None'
              for i in removed_alts]
    corr_values.append(ideal_corr_value)

    return np.array(rankings), corr_values, labels
