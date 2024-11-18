# Copyright (c) 2021 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method
from ..io import TableDesc


class MABAC(MCDA_method):
    """ Multi-Attributive Border Approximation Area Comparison (MABAC) method.

        The MABAC method is based on determining the distance measure between each possible alternative and the Boundary
        Approximation Area (BAA) [#mabac1]_.

        Parameters
        ----------
           normalization_function : callable
               Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
               where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
               cost or profit criterion.

        References
        ----------
        .. [#mabac1] Pamučar, D., & Ćirović, G. (2015). The selection of transport and handling resources in logistics
               centers using Multi-Attributive Border Approximation area Comparison (MABAC). Expert systems with
               applications, 42(6), 3016-3028.

        Examples
        --------
        >>> from pymcdm.methods import MABAC
        >>> import numpy as np
        >>> body = MABAC()
        >>> matrix = np.array([[22600, 3800, 2, 5, 1.06, 3.00, 3.5, 2.8, 24.5, 6.5],
        ...                    [19500, 4200, 3, 2, 0.95, 3.00, 3.4, 2.2, 24, 7.0],
        ...                    [21700, 4000, 1, 3, 1.25, 3.20, 3.3, 2.5, 24.5, 7.3],
        ...                    [20600, 3800, 2, 5, 1.05, 3.25, 3.2, 2.0, 22.5, 11.0],
        ...                    [22500, 3800, 4, 3, 1.35, 3.20, 3.7, 2.1, 23, 6.3],
        ...                    [23250, 4210, 3, 5, 1.45, 3.60, 3.5, 2.8, 23.5, 7.0],
        ...                    [20300, 3850, 2, 5, 0.90, 3.25, 3.0, 2.6, 21.5, 6.0]])
        >>> weights = np.array([0.146, 0.144, 0.119, 0.121, 0.115, 0.101, 0.088, 0.068, 0.050, 0.048])
        >>> types = np.array([-1, 1, 1, 1, -1, -1, 1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.0826, 0.2183, -0.0488, 0.0246, -0.0704, 0.0465, 0.0464]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$n_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Border approximation area matrix',
                  label='baam', symbol='$g_{j}$', rows='C', cols=None),
        TableDesc(caption='Distances from border approximation matrix',
                  label='dbaam', symbol='$q_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$S_i$', rows='A', cols=None)
    ]

    def __init__(self, normalization_function=normalizations.minmax_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        n, m = nmatrix.shape
        # Calculation of the elements from the weighted matrix
        weighted_matrix = (nmatrix + 1) * weights

        # Determining the border approximation area matrix
        G = np.prod(weighted_matrix, axis=0) ** (1 / n)

        # Calculation of the distance border approximation area
        Q = weighted_matrix - G

        score = np.sum(Q, axis=1)
        return nmatrix, weighted_matrix, G, Q, score
