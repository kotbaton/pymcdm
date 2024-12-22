# Copyright (c) 2023-2024 Andrii Shekhovtsov

import numpy as np

from .mcda_method import MCDA_method
from ..validators import bounds_validator, matrix_bounds_validator, ref_ideal_bounds_validator
from ..io import TableDesc


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
    """ Reference Ideal Method [#rim1]_.

    RIM is an MCDA method which uses criteria bounds and reference ideal to evaluate alternatives.

    References
    ----------
    .. [#rim1] Cables, E., Lamata, M. T., & Verdegay, J. L. (2016). RIM-reference ideal method in multicriteria decision making. Information Sciences, 337, 1-10.

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
    _tables = [
        TableDesc(caption='Reference ideal',
                  label='ref_ideal', symbol='$s_j$', rows='C', cols=['$s_{j}^{(min)}$', '$s_{j}^{(max)}$']),
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$y_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatirx', symbol='$y^{\\prime}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Positive variation to the normalized reference ideal',
                  label='pos_var', symbol='$I_i^+$', rows='A', cols=None),
        TableDesc(caption='Negative variation to the normalized reference ideal',
                  label='neg_var', symbol='$I_i^-$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def __init__(self, bounds: np.ndarray | list | tuple, ref_ideal: np.ndarray | list | tuple or None=None):
        """ Create RIM method object.

        Parameters
        ----------
            bounds : ndarray
                Decision problem bounds / criteria bounds. Should be two dimensional array with [min, max] value for in criterion in rows.

            ref_ideal : ndarray or None
                Reference ideal for alternatives evaluation. Should be two dimensional array with interval ideal value for each criterion. If None, reference ideal will be calculated based on bounds and criteria types.
        """
        bounds = np.asarray(bounds)
        bounds_validator(bounds)

        if ref_ideal is not None:
            ref_ideal = np.asarray(ref_ideal)
            ref_ideal_bounds_validator(ref_ideal, bounds)

        self.bounds = bounds
        self.ref_ideal = ref_ideal

    def _additional_validation(self, matrix, weights, types):
        matrix_bounds_validator(matrix, self.bounds)

    def get_ideal_from_bounds(self, bounds, types):
        ind = [0 if t == -1 else 1 for t in types]
        ref_ideal = bounds[range(len(ind)), ind]
        return np.array([ref_ideal, ref_ideal]).T

    def _method(self, matrix, weights, types):
        ref_ideal_s = self.ref_ideal
        range_t = self.bounds
        if ref_ideal_s is None:
            ref_ideal_s = self.get_ideal_from_bounds(self.bounds, types)

        nmatrix = matrix.astype('float')

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                nmatrix[i, j] = _f(matrix[i, j], *range_t[j], *ref_ideal_s[j])

        wnmatrix = nmatrix * weights

        i_plus = np.sqrt(np.sum((wnmatrix - weights) ** 2, axis=1))
        i_minus = np.sqrt(np.sum(wnmatrix ** 2, axis=1))

        p = i_minus / (i_plus + i_minus)

        return ref_ideal_s, nmatrix, wnmatrix, i_plus, i_minus, p
