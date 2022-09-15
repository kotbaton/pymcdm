# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method


class MOORA(MCDA_method):
    """ Multi-Objective Optimization on the basis of Ratio Analysis (MOORA) method.

        The MOORA method is based on an approach using multi-objective optimization to evaluate alternatives.

        References
        ----------
        .. [1] Brauers, W. K., & Zavadskas, E. K. (2006). The MOORA method and its application to privatization in a
             transition economy. Control and cybernetics, 35(2), 445-469.


        Examples
        --------
        >>> from pymcdm.methods import MOORA
        >>> import numpy as np
        >>> body = MOORA()
        >>> matrix = np.array([[1.5, 3, 5, 3.3],
        ...                    [2, 7, 5, 3.35],
        ...                    [3, 1, 5, 3.07],
        ...                    [2.2, 4, 5, 3.5],
        ...                    [2, 5, 3, 3.09],
        ...                    [3.2, 2, 3, 3.48],
        ...                    [2.775, 3, 5, 3.27]])
        >>> weights = np.array([0.3, 0.2, 0.1, 0.4])
        >>> types = np.array([-1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.1801, 0.2345, 0.0625, 0.1757, 0.1683, 0.0742, 0.1197]
    """

    def __init__(self):
        pass

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
        MOORA._validate_input_data(matrix, weights, types)
        if np.all(types == 1.0):
            raise ValueError('types array contains only profit criteria. MOORA method requires at least one cost '
                             'criteria.')
        return MOORA._moora(matrix, weights, types)

    @staticmethod
    def _moora(matrix, weights, cryteria_types):
        nmatrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))

        # Difficult normalized decision making matrix
        wmatrix = nmatrix * weights
        # Calculate the composite score
        cscore = np.sum(wmatrix[:, cryteria_types == 1], axis=1) - np.sum(wmatrix[:, cryteria_types == -1], axis=1)
        return cscore