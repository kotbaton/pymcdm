# Copyright (c) 2023 Bartłomiej Kizielewicz
# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class WASPAS(MCDA_method):
    """ Weighted Aggregated Sum Product ASSessment (WASPAS) [1].

        The WASPAS method is a unique combination of two well-known MCDM approaches, i.e. Weighted Sum Model (WSM) and
        Weighted Product Model (WPM).

        Parameters
        ----------
           normalization_function : callable
               Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
               where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
               cost or profit criterion.

        References
        ----------
        .. [1] Zavadskas, E. K., Turskis, Z., Antucheviciene, J., & Zakarevicius, A. (2012). Optimization of weighted
        aggregated sum product assessment. Elektronika ir elektrotechnika, 122(6), 3-6.

        Examples
        --------
        >>> from pymcdm.methods import WASPAS
        >>> import numpy as np
        >>> body = WASPAS()
        >>> matrix = np.array([[30, 23, 5, 0.745, 0.745, 1500, 5000],
        ...                    [18, 13, 15, 0.745, 0.745, 1300, 6000],
        ...                    [15, 12, 10, 0.500, 0.500, 950, 7000],
        ...                    [25, 20, 13, 0.745, 0.745, 1200, 4000],
        ...                    [14, 18, 14, 0.255, 0.745, 950, 3500],
        ...                    [17, 15, 9, 0.745, 0.500, 1250, 5250],
        ...                    [23, 18, 20, 0.500, 0.745, 1100, 3000],
        ...                    [16, 8, 14, 0.255, 0.500, 1500, 3000]])
        >>> weights = np.array([0.1181, 0.1181, 0.0445, 0.1181, 0.2861, 0.2861, 0.0445])
        >>> types = np.array([1, 1, 1, 1, 1, -1, -1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.8329, 0.7884, 0.6987, 0.8831, 0.7971, 0.7036, 0.8728, 0.5749]
   """

    def __init__(self, normalization_function=normalizations.linear_normalization):
        self.normalization = normalization_function

    def __call__(self, matrix, weights, types, l=0.5, *args, **kwargs):
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

                l: value
                    Dominance parameter: if the value used is 0 the model obtained is a WPM model, if the value used is
                    1 the model obtained is a WSM model.

                *args: is necessary for methods which reqiure some additional data.

                **kwargs: is necessary for methods which reqiure some additional data.

            Returns
            -------
                ndarray
                    Preference values for alternatives. Better alternatives have higher values.
        """
        WASPAS._validate_input_data(matrix, weights, types)
        if self.normalization is not None:
            nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        else:
            nmatrix = helpers.normalize_matrix(matrix, normalizations.linear_normalization, types)
        return WASPAS._waspas(nmatrix, weights, l)

    @staticmethod
    def _waspas(nmatrix, weights, l):

        q_sum = np.sum(nmatrix * weights, axis=1)
        q_prod = np.prod(nmatrix ** weights, axis=1)

        return l * q_sum + (1 - l) * q_prod
