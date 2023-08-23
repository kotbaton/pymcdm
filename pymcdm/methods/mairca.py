# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class MAIRCA(MCDA_method):
    """ Multi-Attributive RealIdeal Comparative Analysis (MARICA) method.

        The MAIRCA method is based on an assumption in which it determines the gap between ideal and empirical rates.\

        Read more in the :ref:`User Guide <MAIRCA>`.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [1] Pamučar, D., Vasin, L., & Lukovac, L. (2014, October). Selection of railway level crossings for investing
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
    _captions = [
        'Normalized decision matrix.',
        'Theoretical ranking matrix.',
        'Real rating matrix.',
        'Total gap matrix.',
        'Final preference values.'
    ]

    def __init__(self, normalization_function=normalizations.minmax_normalization):
        self.normalization = normalization_function

    def _method(self, martrix, weights, types):
        n, _ = martrix.shape

        # Creating theoretical ranking matrix
        Tp = 1 / n * weights

        # Creating real rating matrix
        nmatrix = helpers.normalize_matrix(martrix, self.normalization, types)
        Tr = nmatrix * Tp

        # Calculation of Total Gap Matrix
        G = Tp - Tr

        # Calculation the final values of criteria functions
        score = np.sum(G, axis=1)
        return (nmatrix, Tp, Tr, G, score)
