# Copyright (c) 2020 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method


class COPRAS(MCDA_method):
    """ COmplex PRoportional ASsessment (COPRAS) method.

        COPRAS is used to assess the maximizing and minimizing index values, and the effect of maximizing and minimizing
        indexes of attributes on the results assessment is considered separately [1].

        Read more in the :ref:`User Guide <COPRAS>`.

        References
        ----------
        .. [1] Zavadskas, E. K., Kaklauskas, A., & Sarka, V. (1994). The new method of multicriteria complex
               proportional assessment of projects. Technological and economic development of economy, 1(3), 131-139.

        Examples
        --------
        >>> from pymcdm.methods import COPRAS
        >>> import numpy as np
        >>> body = COPRAS()
        >>> matrix = np.array([[1543, 2000, 39000, 15, 13.76, 3.86, 5, 3, 5000],
        ...                    [1496, 3600, 43000, 14, 14, 2.5, 4, 4, 4000],
        ...                    [1584, 3100, 24500, 10, 13.1, 3.7, 2, 2, 3500],
        ...                    [1560, 2700, 36000, 12, 13.2, 3.2, 3, 3, 3500],
        ...                    [1572, 2500, 31500, 13, 13.3, 3.4, 3, 2, 3500],
        ...                    [1580, 2400, 20000, 12, 12.8, 3.9, 2, 2, 3000]])
        >>> weights = np.array([0.2027, 0.1757, 0.1622, 0.1351, 0.1081, 0.0946, 0.0676, 0.0405, 0.0135])
        >>> types = np.array([-1, -1, -1, 1, 1, -1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [1, 0.9167, 0.8675, 0.9084, 0.9315, 0.9486]
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
        COPRAS._validate_input_data(matrix, weights, types)
        if np.all(types == 1.0):
            raise ValueError('types array contains only profit criteria. COPRAS method requires at least one cost '
                             'criteria.')
        return COPRAS._copras(matrix, weights, types)

    @staticmethod
    def _copras(matrix, weights, criteria_types):
        nmatrix = matrix / np.sum(matrix, axis=0)

        # Difficult normalized decision making matrix
        wmatrix = nmatrix * weights

        Sp = np.sum(wmatrix[:, criteria_types == 1], axis=1)
        Sm = np.sum(wmatrix[:, criteria_types == -1], axis=1)

        Q = Sp + ((np.min(Sm) * np.sum(Sm)) / (Sm * np.sum(np.min(Sm) / Sm)))

        return Q / np.max(Q)
