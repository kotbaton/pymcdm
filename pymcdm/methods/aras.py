# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class ARAS(MCDA_method):
    """ Additive Ratio ASsessment (ARAS) method.

        The ARAS method is based on a utility function value that determines the complex relative efficiency of a feasible
        alternative [1]. This relationship is directly proportional to the relative effect of the values and weights of the
        main criteria.

        Read more in the :ref:`User Guide <ARAS>`.


        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [1] Zavadskas, E. K., & Turskis, Z. (2010). A new additive ratio assessment (ARAS) method in multicriteria
               decision‐making. Technological and economic development of economy, 16(2), 159-172.

        Examples
        --------
        >>> from pymcdm.methods import ARAS
        >>> import numpy as np
        >>> body = ARAS()
        >>> matrix = np.array([[4.64, 3.00, 3.00, 3.00, 2.88, 3.63],
        ...                    [4.00, 4.00, 4.64, 3.56, 3.63, 5.00],
        ...                    [3.30, 4.31, 3.30, 4.00, 3.30, 4.00],
        ...                    [2.62, 5.00, 4.22, 4.31, 5.00, 5.00]])
        >>> weights = np.array([0.28, 0.25, 0.19, 0.15, 0.08, 0.04])
        >>> types = np.array([1, 1, 1, 1, 1, 1])
        >>> [round(preference, 2) for preference in body(matrix, weights, types)]
        [0.74, 0.86, 0.78, 0.86]
    """
    _captions = [
        'Extended decision matrix.',
        'Normalized extended decision matrix.',
        'Weighted normalized extended decision matrix.',
        'Values of optimality function.',
        'Final preference values (Utility degree).'
    ]

    def __init__(self, normalization_function=normalizations.sum_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        n, m = matrix.shape

        # Extended initial decision matrix
        exmatrix = np.zeros((n + 1, m))
        exmatrix[1:] = matrix

        for i in range(m):
            if types[i] == 1:
                exmatrix[0, i] = np.max(matrix[:, i])
            else:
                exmatrix[0, i] = np.min(matrix[:, i])

        # Every row of nmatrix is multiplayed by weights
        nmatrix = helpers.normalize_matrix(exmatrix, self.normalization, types)
        weighted_matrix = nmatrix * weights

        # Values of optimality function
        S = weighted_matrix.sum(axis=1)

        # Utility degree
        K = S[1:] / S[0]

        return (exmatrix, nmatrix, weighted_matrix, S, K)
