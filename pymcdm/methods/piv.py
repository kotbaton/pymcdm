# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class PIV(MCDA_method):
    """ Proximity Indexed Value (PIV) method [#piv1]_.

        PIV sums the weighted deviations of every alternative from the best value of each criterion in the vector
        normalized decision matrix. The linear deviations, instead of the distances of TOPSIS, are meant to reduce
        rank reversal. Lower values of the overall proximity value correspond to better alternatives.

        Read more in the User Guide.

        References
        ----------
        .. [#piv1] Mufazzal, S., & Muzakkir, S. M. (2018). A new multi-criterion decision making (MCDM) method based
               on proximity indexed value for minimizing rank reversals. Computers & Industrial Engineering, 119,
               427-438.

        Examples
        --------
        >>> from pymcdm.methods import PIV
        >>> import numpy as np
        >>> matrix = np.array([[60, 2.5, 2540, 500, 990],
        ...                    [6.35, 6.667, 1016, 3000, 1041],
        ...                    [6.8, 10, 1727, 1500, 1676],
        ...                    [10, 5, 1000, 2000, 965],
        ...                    [2.5, 9.8, 560, 500, 915],
        ...                    [4.5, 12.5, 1016, 350, 508],
        ...                    [3, 10, 1778, 1000, 920]])
        >>> weights = np.array([0.1761, 0.2042, 0.2668, 0.1243, 0.2286])
        >>> types = np.ones(5)
        >>> body = PIV()
        >>> np.round(body(matrix, weights, types), 2).tolist()
        [0.22, 0.36, 0.27, 0.4, 0.46, 0.44, 0.36]
        >>> body.rank(body(matrix, weights, types)).tolist()
        [1.0, 4.0, 2.0, 5.0, 7.0, 6.0, 3.0]
    """
    _reverse_ranking = False
    _tables = [
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted proximity index',
                  label='wpi', symbol='$u_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Overall proximity value',
                  label='pref', symbol='$d_i$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        # Vector normalization (Eq. 1) and weighted normalized matrix (Eq. 2)
        wnmatrix = weights * matrix / np.sqrt(np.sum(matrix ** 2, axis=0))

        # Weighted proximity index: deviation from the best value of each criterion (Eq. 3)
        wpi = np.where(types == 1, np.max(wnmatrix, axis=0) - wnmatrix, wnmatrix - np.min(wnmatrix, axis=0))

        # Overall proximity value (Eq. 4)
        pref = np.sum(wpi, axis=1)

        return wnmatrix, wpi, pref

    def _additional_validation(self, matrix, weights, types):
        if np.any(np.all(matrix == 0, axis=0)):
            raise ValueError('Every criterion should have at least one non-zero value for the vector normalization.')
