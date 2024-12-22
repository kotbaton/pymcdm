# Copyright (c) 2021 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class MOORA(MCDA_method):
    """ Multi-Objective Optimization on the basis of Ratio Analysis (MOORA) method.

        The MOORA method is based on an approach using multi-objective optimization to evaluate alternatives [#moora1]_.

        References
        ----------
        .. [#moora1] Brauers, W. K., & Zavadskas, E. K. (2006). The MOORA method and its application to privatization in a
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
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$P_i$', rows='A', cols=None)
    ]

    def _method(self, matrix, weights, types):
        if np.all(types == 1.0):
            raise ValueError('types array contains only profit criteria.'
                             ' MOORA method requires at least one cost'
                             ' criterion.')

        nmatrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))

        # Difficult normalized decision-making matrix
        wmatrix = nmatrix * weights
        # Calculate the composite score
        cscore = np.sum(wmatrix[:, types == 1], axis=1) - np.sum(wmatrix[:, types == -1], axis=1)

        return nmatrix, wmatrix, cscore
