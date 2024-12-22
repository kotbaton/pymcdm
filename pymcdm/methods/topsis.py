# Copyright (c) 2020-2024 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method
from ..io import TableDesc


class TOPSIS(MCDA_method):
    """ Technique for Order of Preference by Similarity to
        Ideal Solution (TOPSIS).

        The TOPSIS method is based on an approach in which it evaluates alternatives to a positive ideal solution and a
        negative ideal solution [#topsis1]_.

        Parameters
        ----------
           normalization_function : Callable
               Function which should be used to normalize `matrix` columns.
               It should match signature `foo(x, cost)`, where `x` is a vector
               which should be normalized and `cost` is a bool variable which
               says if `x` is a cost or profit criterion.

        References
        ----------
        .. [#topsis1] Hwang, C. L., & Yoon, K. (1981). Methods for multiple attribute decision making. In Multiple attribute
           decision making (pp. 58-191). Springer, Berlin, Heidelberg.

        Examples
        --------
        >>> from pymcdm.methods import TOPSIS
        >>> import numpy as np
        >>> body = TOPSIS()
        >>> matrix = np.array([[1, 2, 5],
        ...                     3000, 3750, 4500]]).T
        >>> weights = np.array([0.5, 0.5])
        >>> types = np.array([-1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.500, 0.617, 0.500]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Negative Ideal Solution',
                  label='nis', symbol='$v^{-}_{j}$', rows='C', cols=None),
        TableDesc(caption='Positive Ideal Solution',
                  label='pis', symbol='$v^{+}_{j}$', rows='C', cols=None),
        TableDesc(caption='Distance from NIS',
                  label='dnis', symbol='$D_i^-$', rows='A', cols=None),
        TableDesc(caption='Distance from PIS',
                  label='dpis', symbol='$D_i^+$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$P_i$', rows='A', cols=None)
    ]

    def __init__(self, normalization_function=normalizations.minmax_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)

        # Every row of nmatrix is multiplayed by weights
        weighted_matrix = nmatrix * weights

        # Vectors of PIS and NIS
        pis = np.max(weighted_matrix, axis=0)
        nis = np.min(weighted_matrix, axis=0)

        # PIS and NIS are substracted from every row of weighted matrix
        Dp = np.sqrt(np.sum((weighted_matrix - pis) ** 2, axis=1))
        Dm = np.sqrt(np.sum((weighted_matrix - nis) ** 2, axis=1))

        p = Dm / (Dm + Dp)

        return nmatrix, weighted_matrix, nis, pis, Dm, Dp, p
