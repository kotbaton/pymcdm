# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class MAIRCA(MCDA_method):
    """ Multi-Attributive RealIdeal Comparative Analysis (MARICA) method.

        The MAIRCA method is based on an assumption in which it determines the gap between ideal and empirical rates.\

        Read more in the :ref:`User Guide <MAIRCA>`.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [1] Pamučar, D., Vasin, L., & Lukovac, L. (2014, October). Selection of railway level crossings for investing
               in security equipment using hybrid DEMATEL-MARICA model. In XVI international scientific-expert
               conference on railway, railcon (pp. 89-92).

        Examples
        --------
        >>> from pymcdm.methods import MAIRCA
        >>> import numpy as np
        >>> body = MAIRCA()
        >>> matrix = np.array([[70, 245, 16.4, 19],
        ...                    [52, 246, 7.3, 22],
        ...                    [53, 295, 10.3, 25],
        ...                    [63, 256, 12, 8],
        ...                    [64, 233, 5.3, 17]])
        >>> weights = np.array([0.04744, 0.02464, 0.51357, 0.41435])
        >>> types = np.array([1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.0332, 0.1122, 0.0654, 0.1304, 0.1498]
    """
    reverse_ranking = False

    def __init__(self, normalization_function=normalizations.minmax_normalization):
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
        MAIRCA._validate_input_data(matrix, weights, types)
        return MAIRCA._mairca(matrix, weights, types, self.normalization)

    @staticmethod
    def _mairca(martrix, weights, types, normalization):
        n, _ = martrix.shape

        # Creating theoretical ranking matrix
        Tp = 1 / n * weights

        # Creating real rating matrix
        nmatrix = helpers.normalize_matrix(martrix, normalization, types)
        Tr = nmatrix * Tp

        # Calculation of Total Gap Matrix
        G = Tp - Tr

        # Calculation the final values of criteria functions
        return np.sum(G, axis=1)
