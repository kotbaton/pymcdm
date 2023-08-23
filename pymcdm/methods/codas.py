# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


def _psi(x, tau=0.02):
    if np.abs(x) >= tau:
        return 1
    return 0


class CODAS(MCDA_method):
    """ COmbinative Distance-based ASsessment (CODAS) method.

        The CODAS method is based on an approach based on Euclidean distance and Taxicab from the negative ideal solution [#codas1]_.

        Read more in the User Guide.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [#codas1] Keshavarz Ghorabaee, M., Zavadskas, E. K., Turskis, Z., & Antucheviciene, J. (2016). A new combinative
               distance-based assessment (CODAS) method for multi-criteria decision-making. Economic Computation &
               Economic Cybernetics Studies & Research, 50(3).

        Examples
        --------
        >>> from pymcdm.methods import CODAS
        >>> import numpy as np
        >>> body = CODAS()
        >>> matrix = np.array([[45, 3600, 45, 0.9],
        ...                    [25, 3800, 60, 0.8],
        ...                    [23, 3100, 35, 0.9],
        ...                    [14, 3400, 50, 0.7],
        ...                    [15, 3300, 40, 0.8],
        ...                    [28, 3000, 30, 0.6]])
        >>> weights = np.array([0.2857, 0.3036, 0.2321, 0.1786])
        >>> types = np.array([1, -1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [1.3914, 0.3411, -0.2170, -0.5381, -0.7292, -0.2481]
    """
    _captions = [
        'Normalized decision matrix.',
        'Weighted normalized decision matrix.',
        'Negative-ideal solution.',
        'Euclidean distances from the negative-ideal solution.',
        'Manhattan distances from the negative-ideal solution.',
        'Relative assessement matrix.',
        'Final preference values.'
    ]

    def __init__(self, normalization_function=normalizations.linear_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        # Every row of nmatrix is multiplayed by weights
        weighted_matrix = nmatrix * weights
        n, m = weighted_matrix.shape

        # Vector of NIS
        nis = np.min(weighted_matrix, axis=0)

        # Euclidean and Taxicab distances from negative-ideal solution
        E = np.sqrt(np.sum((weighted_matrix - nis) ** 2, axis=1))
        T = np.sum(np.abs(weighted_matrix - nis), axis=1)

        # Construct the relative assessment matrix
        h = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                h[i, j] = (E[i] - E[j]) + (_psi(E[i] - E[j]) * (T[i] - T[j]))

        H = np.sum(h, axis=1)

        return (nmatrix, weighted_matrix, nis, E, T, h, H)
