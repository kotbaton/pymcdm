# Copyright (c) 2020 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class TOPSIS(MCDA_method):
    """ Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS).

        The TOPSIS method is based on an approach in which it evaluates alternatives to a positive ideal solution and a
        negative ideal solution [1].

        Parameters
        ----------
           normalization_function : callable
               Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
               where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
               cost or profit criterion.

        References
        ----------
        .. [1] Hwang, C. L., & Yoon, K. (1981). Methods for multiple attribute decision making. In Multiple attribute
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
        TOPSIS._validate_input_data(matrix, weights, types)
        if self.normalization is not None:
            nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        else:
            nmatrix = helpers.normalize_matrix(matrix, normalizations.minmax_normalization, types)
        return TOPSIS._topsis(nmatrix, weights)

    @staticmethod
    def _topsis(nmatrix, weights):
        # Every row of nmatrix is multiplayed by weights
        weighted_matrix = nmatrix * weights

        # Vectors of PIS and NIS
        pis = np.max(weighted_matrix, axis=0)
        nis = np.min(weighted_matrix, axis=0)

        # PIS and NIS are substracted from every row of weighted matrix
        Dp = np.sqrt(np.sum((weighted_matrix - pis) ** 2, axis=1))
        Dm = np.sqrt(np.sum((weighted_matrix - nis) ** 2, axis=1))

        return Dm / (Dm + Dp)

