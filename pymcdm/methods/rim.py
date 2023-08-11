# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

from pymcdm import helpers
from pymcdm import normalizations

from .mcda_method import MCDA_method


def _dmin(x, c, d):
    """ Helper for the RIM normalization function."""
    return min(abs(x - c), abs(x - d))


def _f(x, a, b, c, d):
    """ RIM normalization function.

    Parameters
    ----------
    x: float
        Value which should be normalized. x ∈ [a, b]
    a, b: float
        Range that belongs to a universe of discourse.
    c, d: float
        The reference ideal.

    Returns
    -------
        float
            Normalized value
    """
    if c <= x <= d:
        return 1
    elif (a <= x < c) and (a != c):
        return 1 - (_dmin(x, c, d) / abs(a - c))
    elif (d < x <= b) and (d != b):
        return 1 - (_dmin(x, c, d) / abs(d - b))


class RIM(MCDA_method):
    """ Reference Ideal Method

    RIM is an MCDA method which uses criteria bounds and reference ideal to evaluate alternatives.

    References
    ----------
    .. [1] Cables, E., Lamata, M. T., & Verdegay, J. L. (2016). RIM-reference ideal method in multicriteria decision making. Information Sciences, 337, 1-10.

    Examples
    --------
    >>> import numpy as np
    >>> from pymcdm.methods import RIM
    >>> matrix = np.array([
    ...     [30,  0, 2, 3, 3, 2],
    ...     [40,  9, 1, 3, 2, 2],
    ...     [25,  0, 3, 1, 3, 2],
    ...     [27,  0, 5, 3, 3, 1],
    ...     [45, 15, 2, 2, 3, 4]
    ... ])
    >>> weights = np.array([0.2262, 0.2143, 0.1786, 0.1429, 0.1190, 0.1190])
    >>> types = np.array([1, 1, -1, 1, 1, 1])
    >>> range_t = np.array([
    ...      [23, 60],
    ...      [0, 15],
    ...      [0, 10],
    ...      [1, 3],
    ...      [1, 3],
    ...      [1, 5]
    ...  ])
    >>>  ref_s = [
    ...      [30, 35],
    ...      [10, 15],
    ...      [0, 0],
    ...      [3, 3],
    ...      [3, 3],
    ...      [4, 5]
    ...  ]
    >>>  pr = RIM(range_t, ref_s)
    >>>  pref = pr(matrix, weights, types)
    >>>  rank = pr.rank(pref)
    >>>  print(pref)
    ...  [0.5866 0.7558 0.3716 0.4666 0.7401]
    >>>  print(rank)
    ...  [3. 1. 5. 4. 2.]
    """

    def __init__(self, bounds, ref_ideal=None):
        """ Create RIM method object.

        Parameters
        ----------
            bounds : ndarray
                Decision problem bounds / criteria bounds. Should be two dimensional array with [min, max] value for in criterion in rows.

            ref_ideal : ndarray or None
                Reference ideal for alternatives evaluation. Should be two dimensional array with interval ideal value for each criterion. If None, reference ideal will be calculated based on bounds and criteria types.
        """
        bounds = np.array(bounds)
        if ref_ideal is not None:
            ref_ideal = np.array(ref_ideal)
            if ref_ideal.shape[1] != 2:
                raise ValueError('Shape of the ref_ideal should be (M, 2), where M is a number of critria. Single values should be provided duplicated, e.g. 0 should be added as [0, 0].')

            if ref_ideal.shape != bounds.shape:
                raise ValueError('Bounds and ref_ideal should have equal shapes.')

        if np.any(bounds[:, 0] >= bounds[:, 1]):
            eq = np.arange(bounds.shape[0])[bounds[:, 0] >= bounds[:, 1]]
            raise ValueError(f'Lower bound of criteria {eq} is bigger or equal to upper bound.')

        self.bounds = bounds
        self.ref_ideal = ref_ideal

    def __call__(self, matrix, weights, types, *args, **kwargs):
        """ Rank alternatives from decision matrix `matrix`, with criteria weights `weights` and criteria types `types`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : ndarray
                    Criteria weights. Sum of the weights should be 1. (e.g. sum(weights) == 1)

                types : ndarray
                    Array with definitions of criteria types:
                    1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.

                *args: is necessary for methods which reqiure some additional data.

                **kwargs: is necessary for methods which reqiure some additional data.

            Returns
            -------
                ndarray
                    Preference values for alternatives. Better alternatives have higher values.
        """
        RIM._validate_input_data(matrix, weights, types)
        # Build ref ideal from the bounds if None
        ref_ideal = self.ref_ideal
        if ref_ideal is None:
            ref_ideal = self.get_ideal_from_bounds(self.bounds, types)
        return RIM._rim(matrix, weights, self.bounds, ref_ideal)

    def get_ideal_from_bounds(self, bounds, types):
        ind = [0 if t == -1 else 1 for t in types]
        ref_ideal = bounds[range(len(ind)), ind]
        return np.array([ref_ideal, ref_ideal]).T

    @staticmethod
    def _rim(matrix, weights, range_t, ref_ideal_s):
        nmatrix = matrix.astype('float')

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                nmatrix[i, j] = _f(matrix[i, j], *range_t[j], *ref_ideal_s[j])

        wnmatrix = nmatrix * weights

        i_plus = np.sqrt(np.sum((wnmatrix - weights) ** 2, axis=1))
        i_minus = np.sqrt(np.sum(wnmatrix ** 2, axis=1))

        return i_minus / (i_plus + i_minus)
