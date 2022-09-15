# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method


def _ocra_normalization(x, cost=False):
    if cost:
        return (np.max(x) - x) / np.min(x)
    return (x - np.min(x)) / np.min(x)


class OCRA(MCDA_method):
    """ Operational Competitiveness Rating (OCRA) method.

        The main idea of the OCRA method is toperform   independent evaluation ofalternatives  with  respect  to
        beneficial  andnon beneficial  criteria,  and  finally  tocombine these two sets of ratings to obtainthe
        operational competitiveness ratings [1].

        Parameters
        ----------
          normalization_function : callable
              Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
              where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
              cost or profit criterion.

        References
        ----------
        .. [1] Madić, M., Petković, D., & Radovanović, M. (2015). Selection of non-conventional machining processes using
             the OCRA method. Serbian Journal of Management, 10(1), 61-73.


        Examples
        --------
        >>> from pymcdm.methods import OCRA
        >>> import numpy as np
        >>> body = OCRA()
        >>> matrix = np.array([[7.7, 256, 7.2, 7.3, 7.3],
        ...                    [8.1, 250, 7.9, 7.8, 7.7],
        ...                    [8.7, 352, 8.6, 7.9, 8.0],
        ...                    [8.1, 262, 7.0, 8.1, 7.2],
        ...                    [6.5, 271, 6.3, 6.4, 6.1],
        ...                    [6.8, 228, 7.1, 7.2, 6.5]])
        >>> weights = np.array([0.239, 0.225, 0.197, 0.186, 0.153])
        >>> types = np.array([1, -1, 1, 1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.143, 0.210, 0.164, 0.167, 0, 0.112]
    """

    def __init__(self, normalization_function=_ocra_normalization):
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
        OCRA._validate_input_data(matrix, weights, types)
        return OCRA._ocra(matrix, weights, types, self.normalization)

    @staticmethod
    def _ocra(martrix, weights, types, normalization):
        n, m = martrix.shape

        # Calculate preference ratings for cost and profit criteria
        I = np.zeros(n)
        O = np.zeros(n)
        for j in range(m):
            if types[j] == -1:
                I += weights[j] * normalization(martrix[:, j], cost=True)
            else:
                O += weights[j] * normalization(martrix[:, j], cost=False)

        # Calculate linear preference ratings for cost and profit criteria
        I -= np.min(I)
        O -= np.min(O)

        # Calculate overall preference rating
        return (I + O) - np.min(I + O)
