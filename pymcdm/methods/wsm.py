# Copyright (c) 2023 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method
from ..io import TableDesc


class WSM(MCDA_method):
    """ Weighted Sum Model (WSM) [#wsm1]_.

        WSM is based on an approach that evaluates alternatives by weighted sum.

        Parameters
        ----------
           normalization_function : callable
               Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
               where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
               cost or profit criterion.

        References
        ----------
        .. [#wsm1] Fishburn, P. C., Murphy, A. H., & Isaacs, H. H. (1968). Sensitivity of decisions to probability
            estimation errors: A reexamination. Operations Research, 16(2), 254-267.

        Examples
        --------
        >>> from pymcdm.methods import WSM
        >>> import numpy as np
        >>> body = WSM()
        >>> matrix = np.array([[96, 83, 75, 7],
        ...                    [63, 5, 56, 9],
        ...                    [72, 30, 32, 48],
        ...                    [11, 4, 27, 9],
        ...                    [77, 21, 17, 11]])
        >>> weights = np.array([8/13, 5/13, 6/13, 7/13])
        >>> types = np.array([1, 1, -1, -1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.609, 0.313, 0.334, 0.265, 0.479]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def __init__(self, normalization_function=normalizations.sum_normalization):
        self.normalization = normalization_function


    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        # Every row of nmatrix is multiplayed by weights
        weighted_matrix = nmatrix * weights

        p = np.sum(weighted_matrix, axis=1)
        return nmatrix, weighted_matrix, p
