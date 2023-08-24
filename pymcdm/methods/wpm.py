# Copyright (c) 2023 Bartłomiej Kizielewicz

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class WPM(MCDA_method):
    """ Weighted Product Model (WPM) [1].

        WPM is based on an approach that evaluates alternatives by weighted product.

        Parameters
        ----------
           normalization_function : callable
               Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
               where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
               cost or profit criterion.

        References
        ----------
        .. [1] Fishburn, P. C., Murphy, A. H., & Isaacs, H. H. (1968). Sensitivity of decisions to probability
        estimation errors: A reexamination. Operations Research, 16(2), 254-267.

        Examples
        --------
        >>> from pymcdm.methods import WPM
        >>> import numpy as np
        >>> body = WPM()
        >>> matrix = np.array([[96, 83, 75, 7],
        ...                    [63, 5, 56, 9],
        ...                    [72, 30, 32, 48],
        ...                    [11, 4, 27, 9],
        ...                    [77, 21, 17, 11]])
        >>> weights = np.array([8/13, 5/13, 6/13, 7/13])
        >>> types = np.array([1, 1, -1, -1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.065, 0.017, 0.019, 0.007, 0.052]
   """
    _captions = [
        'Normalized decision matrix.',
        'Weighted normalized decision matrix.',
        'Final preference values.'
    ]

    def __init__(self, normalization_function=normalizations.sum_normalization):
        self.normalization = normalization_function


    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        # Every row of nmatrix is compounded by weights
        weighted_matrix = nmatrix ** weights

        p = np.prod(weighted_matrix, axis=1)
        return (nmatrix, weighted_matrix, p)
