# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class COCOSO(MCDA_method):
    """ COmbined COmpromise SOlution (COCOSO) method.

        The COCOSO method is based on an integrated model of simple additive weighting and exponentially weighted
        product [1].

        Read more in the :ref:`User Guide <COCOSO>`.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is
                a cost or profit criterion.

        References
        ----------
        .. [1] Yazdani, M., Zarate, P., Zavadskas, E. K., & Turskis, Z. (2019). A Combined Compromise Solution (CoCoSo)
               method for multi-criteria decision-making problems. Management Decision.

        Examples
        --------
        >>> from pymcdm.methods import COCOSO
        >>> import numpy as np
        >>> body = COCOSO()
        >>> matrix = np.array([[60, 0.4, 2540, 500, 990],
        ...                    [6.35, 0.15, 1016, 3000, 1041],
        ...                    [6.8, 0.1, 1727.2, 1500, 1676],
        ...                    [10, 0.2, 1000, 2000, 965],
        ...                    [2.5, 0.1, 560, 500, 915],
        ...                    [4.5, 0.08, 1016, 350, 508],
        ...                    [3, 0.1, 1778, 1000, 920]])
        >>> weights = np.array([0.036, 0.192, 0.326, 0.326, 0.12])
        >>> types = np.array([1, -1, 1, 1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [2.041, 2.788, 2.882, 2.416, 1.299, 1.443, 2.519]
    """

    def __init__(self, normalization_function=normalizations.minmax_normalization):
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
                The value of balanced compromise. It must be from the interval [0, 1].

            *args: is necessary for methods which reqiure some additional data.

            **kwargs: is necessary for methods which reqiure some additional data.

        Returns
        -------
            ndarray
                Preference values for alternatives. Better alternatives have higher values.
        """
        COCOSO._validate_input_data(matrix, weights, types)
        if self.normalization is not None:
            nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        else:
            nmatrix = helpers.normalize_matrix(matrix, normalizations.minmax_normalization, types)
        return COCOSO._cocoso(nmatrix, weights, l)

    @staticmethod
    def _cocoso(nmatrix, weights, l=0.5):
        # Vectors of S and P
        S = np.sum(nmatrix * weights, axis=1)
        P = np.sum(nmatrix ** weights, axis=1)

        # Calculate score strategies
        ksi_a = (P + S) / np.sum(P + S, axis=0)
        ksi_b = S / np.min(S) + P / np.min(P)
        ksi_c = (l * S + (1 - l) * P) / (l * np.max(S) + (1 - l) * np.max(P))

        # Compute the prefomance score
        ksi = np.power(ksi_a * ksi_b * ksi_c, 1/3) + 1/3 * (ksi_a + ksi_b + ksi_c)

        return ksi