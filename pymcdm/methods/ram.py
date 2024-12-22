# Copyright (c) 2023-2024 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method
from ..io import TableDesc


class RAM(MCDA_method):
    """ Root Assessment Method (RAM) [#ram1]_.

        Parameters
        ----------
           normalization_function : Callable
               Function which should be used to normalize `matrix` columns.
               It should match signature `foo(x, cost)`, where `x` is a vector
               which should be normalized and `cost` is a bool variable which
               says if `x` is a cost or profit criterion.

        References
        ----------
        .. [#ram1] Sotoudeh-Anvari, A. (2023). Root Assessment Method (RAM): A novel multi-criteria decision making method and its applications in sustainability challenges. Journal of Cleaner Production, 138695.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import RAM
        >>> matrix = np.array([
        ...     [0.068, 0.066, 0.150, 0.098, 0.156, 0.114, 0.098],
        ...     [0.078, 0.076, 0.108, 0.136, 0.082, 0.171, 0.105],
        ...     [0.157, 0.114, 0.128, 0.083, 0.108, 0.113, 0.131],
        ...     [0.106, 0.139, 0.058, 0.074, 0.132, 0.084, 0.120],
        ...     [0.103, 0.187, 0.125, 0.176, 0.074, 0.064, 0.057],
        ...     [0.105, 0.083, 0.150, 0.051, 0.134, 0.094, 0.113],
        ...     [0.137, 0.127, 0.056, 0.133, 0.122, 0.119, 0.114],
        ...     [0.100, 0.082, 0.086, 0.060, 0.062, 0.109, 0.093],
        ...     [0.053, 0.052, 0.043, 0.100, 0.050, 0.078, 0.063],
        ...     [0.094, 0.074, 0.097, 0.087, 0.080, 0.054, 0.106]
        ... ])
        >>> weights = np.array([0.132, 0.135, 0.138, 0.162, 0.09, 0.223, 0.12])
        >>> types = np.array([1, -1, -1, 1, 1, 1, 1])
        >>> ram = RAM()
        >>> output_method = ram(matrix, weights, types)
        >>> output_method = np.round(output_method, 4)
        >>> print(output_method)
        [1.4332 1.4392 1.4353 1.4322 1.4279 1.4301 1.4394 1.4308 1.4294 1.4288]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$y_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Sum of weighted normalized scores of beneficial criteria',
                  label='benefit_scores', symbol='$S_{+i}$', rows='A', cols=None),
        TableDesc(caption='Sum of weighted normalized scores of cost criteria',
                  label='cost_scores', symbol='$S_{-i}$', rows='A', cols=None),
        TableDesc(caption='Final preference values of each alternative',
                  label='pref', symbol='${RI}_{i}$', rows='A', cols=None),
    ]

    def __init__(self, normalization_function=normalizations.sum_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, None)

        # Every row of nmatrix is multiplayed by weights
        wnmatrix = nmatrix * weights

        # Vectors of PIS and NIS
        mask = (types == 1)
        Spi = wnmatrix[:, mask].sum(axis=1)
        Smi = wnmatrix[:, ~mask].sum(axis=1)

        ri = (2 + Spi) ** (1 / (2 + Smi))

        return nmatrix, wnmatrix, Spi, Smi, ri

