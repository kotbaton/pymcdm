# Copyright (c) 2021 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method
from ..io import TableDesc


class MAIRCA(MCDA_method):
    """ Multi-Attributive RealIdeal Comparative Analysis (MARICA) method.

        The MAIRCA method is based on an assumption in which it determines the gap between ideal and empirical rates [#mairca1]_.

        Read more in the User Guide.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [#mairca1] Pamučar, D., Vasin, L., & Lukovac, L. (2014, October). Selection of railway level crossings for investing
               in security equipment using hybrid DEMATEL-MARICA model. In XVI international scientific-expert
               conference on railway, railcon (pp. 89-92).

        Examples
        --------
        >>> from pymcdm.methods import MAIRCA
        >>> import numpy as np
        >>> body = MAIRCA()
        >>> matrix = np.array([[70, 245, 16.4, 19],
        ...                    [52, 246, 7.3, 22],
        ...                    [53, 295, 10.3, 25],
        ...                    [63, 256, 12, 8],
        ...                    [64, 233, 5.3, 17]])
        >>> weights = np.array([0.04744, 0.02464, 0.51357, 0.41435])
        >>> types = np.array([1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.0332, 0.1122, 0.0654, 0.1304, 0.1498]
    """
    _reverse_ranking = False
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Theoretical ranking matrix',
                  label='tpmatrix', symbol='$t_{pij}$', rows='C', cols=None),
        TableDesc(caption='Real rating matrix',
                  label='trmatrix', symbol='$t_{rij}$', rows='A', cols='C'),
        TableDesc(caption='Total gap matrix',
                  label='gmatrix', symbol='$g_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$Q_{i}$', rows='A', cols=None),
    ]

    def __init__(self, normalization_function=normalizations.minmax_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        n, _ = matrix.shape

        # Creating theoretical ranking matrix
        Tp = 1 / n * weights

        # Creating real rating matrix
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        Tr = nmatrix * Tp

        # Calculation of Total Gap Matrix
        G = Tp - Tr

        # Calculation of the final values of criteria functions
        score = np.sum(G, axis=1)
        return nmatrix, Tp, Tr, G, score
