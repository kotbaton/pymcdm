# Copyright (c) 2020-2024 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..validators import bounds_validator, esp_bounds_validator, matrix_bounds_validator
from ..io import TableDesc


class SPOTIS(MCDA_method):
    """ Stable Preference Ordering Towards Ideal Solution (SPOTIS) method.

        The SPOTIS method is based on an approach in which it evaluates
        given decision alternatives using the distance from the best
        ideal solution. [#spotis1]_.

        Read more in the User Guide.

        References
        ----------
        .. [#spotis1] Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The SPOTIS rank reversal free method for multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION) (pp. 1-8). IEEE.

        Examples
        --------
        >>> from pymcdm.methods import SPOTIS
        >>> import numpy as np
        >>> matrix = np.array([[10.5, -3.1, 1.7],
        ...                    [-4.7, 0, 3.4],
        ...                    [8.1, 0.3, 1.3],
        ...                    [3.2, 7.3, -5.3]])
        >>> bounds = np.array([[-5, 12],
        ...                    [-6, 10],
        ...                    [-8, 5]], dtype=float)
        >>> weights = np.array([0.2, 0.3, 0.5])
        >>> types = np.array([1, -1, 1])
        >>> body = SPOTIS(bounds)
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.1989, 0.3705, 0.3063, 0.7491]
    """
    _reverse_ranking = False
    _tables = [
        TableDesc(caption='Ideal/Expected Solution Point (ISP/ESP)',
                  label='esp_isp', symbol='$S^{*}$/$S^{+}$', rows='C', cols=None),
        TableDesc(caption='Normalized distances from ISP',
                  label='nmatrix', symbol='$d_{ij}(A_i, S^{*}_j)$', rows='A', cols='C'),
        TableDesc(caption='Weighted average distance from ISP',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def __init__(self, bounds, esp=None):
        """ Create SPOTIS method object.

        Parameters
        ----------
            bounds : ndarray
                Decision problem bounds / criteria bounds. Should be two dimensional array with [min, max] value for in criterion in rows.

            esp : ndarray or None
                Expected Solution Point for alternatives evaluation. Should be array with ideal (expected) value for each criterion. If None, ESP will be calculated based on bounds and criteria types. Default is None.
        """
        self.bounds = np.asarray(bounds, dtype='float')
        bounds_validator(self.bounds)
        self.esp = esp
        if esp is not None:
            self.esp = np.asarray(esp, dtype='float')
            esp_bounds_validator(self.esp, self.bounds)

    def _method(self, matrix, weights, types):
        bounds = self.bounds
        esp = self.esp
        if esp is None:
            # Determine ESP based on criteria bounds. In this case ESP == ISP.
            esp = bounds[np.arange(bounds.shape[0]),
                         ((types+1)//2).astype('int')]

        # Normalized distances matrix (d_{ij})
        nmatrix = np.abs((matrix - esp)/
                         (bounds[:,0] - bounds[:,1]))
        # Distances to ISP (smaller means better alt)
        raw_scores = np.sum(nmatrix * weights, axis=1)
        return esp, nmatrix, raw_scores

    def _additional_validation(self, matrix, weights, types):
        matrix_bounds_validator(matrix, self.bounds)

    @staticmethod
    def make_bounds(matrix):
        """ Returns bounds matrix for each criterion, e.g. extract min and max for each criterion values.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix.
                    Alternatives are in rows and Criteria are in columns.

            Returns
            -------
                bounds : ndarray
                    Min and max values (bounds) for each criterion.

            Examples
            --------
            >>> import numpy as np
            >>> from pymcdm.methods import SPOTIS
            >>> matrix = np.array([[ 96, 145, 200],
                                   [100, 145, 200],
                                   [120, 170,  80],
                                   [140, 180, 140],
                                   [100, 110,  30]])
            >>> types = np.ones(3)
            >>> weights = np.ones(3)/3
            >>> body = SPOTIS()
            >>> preferences = body(matrix, weights, types, bounds=bounds)
            >>> np.round(preferences, 4)
            array([0.5   , 0.4697, 0.4344, 0.1176, 0.9697])
            """
        return np.hstack((
            np.min(matrix, axis=0).reshape(-1, 1),
            np.max(matrix, axis=0).reshape(-1, 1)
        ))
