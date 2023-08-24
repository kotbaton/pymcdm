# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .. import helpers
from .mcda_method import MCDA_method


def _marcos_normalization(x, cost=False):
    if cost:
        return x[-2] / x
    return x / x[-2]


class MARCOS(MCDA_method):
    """ Measurement of Alternatives and Ranking according to COmpromise Solution (MARCOS) method.

        The MARCOS method is based on the approach of evaluating alternatives according to reference values (ideal and
        anti-ideal) using a utility function [1].

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [1] Stević, Ž., Pamučar, D., Puška, A., & Chatterjee, P. (2020). Sustainable supplier selection in
               healthcare industries using a new MCDM method: Measurement of alternatives and ranking according to
               COmpromise solution (MARCOS). Computers & Industrial Engineering, 140, 106231.


        Examples
        --------
        >>> from pymcdm.methods import MARCOS
        >>> import numpy as np
        >>> body = MARCOS()
        >>> matrix = np.array([[660, 1000, 1600, 18, 1200],
        ...                    [800, 1000, 1600, 24, 900],
        ...                    [980, 1000, 2500, 24, 900],
        ...                    [920, 1500, 1600, 24, 900],
        ...                    [1380, 1500, 1500, 24, 1150],
        ...                    [1230, 1000, 1600, 24, 1150],
        ...                    [680, 1500, 1600, 18, 1100],
        ...                    [960, 2000, 1600, 12, 1150]])
        >>> weights = np.array([0.1061, 0.3476, 0.3330, 0.1185, 0.0949])
        >>> types = np.array([-1, 1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.5649, 0.5543, 0.6410, 0.6174, 0.6016, 0.5453, 0.6282, 0.6543]
    """
    _captions = [
        'Extended decision matrix.',
        'Normalized extended decision matrix.',
        'Weighted normalized extended decision matrix.',
        'Utility degree in relation to anti-ideal solution.',
        'Utility degree in relation to ideal solution.',
        'Utility function in relation to anti-ideal solution.',
        'Utility function in relation to ideal solution.',
        'Final preference score.'
    ]

    def __init__(self, normalization_function=_marcos_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        n, m = matrix.shape

        # Extended initial decision matrix
        exmatrix = np.zeros((n + 2, m))
        exmatrix[:-2] = matrix

        max_maxes = matrix.max(axis=0)
        min_values = matrix.min(axis=0)

        for i in range(m):
            if types[i] == 1:
                exmatrix[-2, i] = max_maxes[i]
                exmatrix[-1, i] = min_values[i]
            else:
                exmatrix[-2, i] = min_values[i]
                exmatrix[-1, i] = max_maxes[i]

        # Normalization
        n_exmatrix = helpers.normalize_matrix(exmatrix,
                                              self.normalization, types)

        # Weighting
        weighted_matrix = n_exmatrix * weights

        # Utility degree
        S = weighted_matrix.sum(axis=1)
        k_neg = (S / S[-1])[:-2]
        k_pos = (S / S[-2])[:-2]

        # Utility functions
        f_k_pos = k_neg / (k_pos + k_neg)
        f_k_neg = k_pos / (k_pos + k_neg)
        f_k = (k_pos + k_neg) / (1 + (1 - f_k_pos) / f_k_pos + (1 - f_k_neg) / f_k_neg)

        return (exmatrix, n_exmatrix, weighted_matrix,
                k_neg, k_pos, f_k_neg, f_k_pos, f_k)
