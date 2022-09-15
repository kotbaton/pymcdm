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

        The CODAS method is based on an approach based on Euclidean distance and Taxicab from the negative ideal solution
        [1].

        Read more in the :ref:`User Guide <CODAS>`.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [1] Keshavarz Ghorabaee, M., Zavadskas, E. K., Turskis, Z., & Antucheviciene, J. (2016). A new combinative
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

    def __init__(self, normalization_function=normalizations.linear_normalization):
        self.normalization = normalization_function

    def __call__(self, matrix, weights, types, *args, **kwargs):
        """Rank alternatives from decision matrix `matrix`, with criteria weights `weights` and criteria types `types`.

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
        CODAS._validate_input_data(matrix, weights, types)
        if self.normalization is not None:
            nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        else:
            nmatrix = helpers.normalize_matrix(matrix, normalizations.linear_normalization, types)
        return CODAS._codas(nmatrix, weights)

    @staticmethod
    def _codas(nmatrix, weights):
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

        return np.sum(h, axis=1)
