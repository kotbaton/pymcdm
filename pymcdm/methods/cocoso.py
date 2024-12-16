# Copyright (c) 2021 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from ..validators import param_validator
from .mcda_method import MCDA_method
from ..io import TableDesc


class COCOSO(MCDA_method):
    """ COmbined COmpromise SOlution (COCOSO) method.

        The COCOSO method is based on an integrated model of simple additive weighting and exponentially weighted
        product [#cocoso1]_.

        Read more in the User Guide.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is
                a cost or profit criterion.

        References
        ----------
        .. [#cocoso1] Yazdani, M., Zarate, P., Zavadskas, E. K., & Turskis, Z. (2019). A Combined Compromise Solution (CoCoSo)
               method for multi-criteria decision-making problems. Management Decision.

        Examples
        --------
        >>> from pymcdm.methods import COCOSO
        >>> import numpy as np
        >>> body = COCOSO()
        >>> matrix = np.array([[60, 0.4, 2540, 500, 990],
        ...                    [6.35, 0.15, 1016, 3000, 1041],
        ...                    [6.8, 0.1, 1727.2, 1500, 1676],
        ...                    [10, 0.2, 1000, 2000, 965],
        ...                    [2.5, 0.1, 560, 500, 915],
        ...                    [4.5, 0.08, 1016, 350, 508],
        ...                    [3, 0.1, 1778, 1000, 920]])
        >>> weights = np.array([0.036, 0.192, 0.326, 0.326, 0.12])
        >>> types = np.array([1, -1, 1, 1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [2.041, 2.788, 2.882, 2.416, 1.299, 1.443, 2.519]
    """
    _captions = [
        'Normalized decision matrix.',
        'Vector of $S_i$ values.',
        'Vector of $P_i$ values.',
        'Appraisal score strategy $k_{ia}$.',
        'Appraisal score strategy $k_{ib}$.',
        'Appraisal score strategy $k_{ic}$.',
        'Final preference value.',
    ]
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Vector of $S_i$ values',
                  label='s_values', symbol='$S_{i}$', rows='A', cols=None),
        TableDesc(caption='Vector of $P_i$ values',
                  label='p_values', symbol='$P_{i}$', rows='A', cols=None),
        TableDesc(caption='Appraisal score strategy $k_{ia}$',
                  label='appr_score_a', symbol='$k_{ia}$', rows='A', cols=None),
        TableDesc(caption='Appraisal score strategy $k_{ib}$',
                  label='appr_score_b', symbol='$k_{ib}$', rows='A', cols=None),
        TableDesc(caption='Appraisal score strategy $k_{ic}$',
                  label='appr_score_c', symbol='$k_{ic}$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$k_i$', rows='A', cols=None)
    ]

    def __init__(self,
                 normalization_function=normalizations.minmax_normalization,
                 l=0.5):
        self.normalization = normalization_function
        param_validator(l, 'l')
        self.l = l

    def _method(self, matrix, weights, types):
        l = self.l
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        # Vectors of S and P
        S = np.sum(nmatrix * weights, axis=1)
        P = np.sum(nmatrix ** weights, axis=1)

        # Calculate score strategies
        ksi_a = (P + S) / np.sum(P + S, axis=0)
        ksi_b = S / np.min(S) + P / np.min(P)
        ksi_c = (l * S + (1 - l) * P) / (l * np.max(S) + (1 - l) * np.max(P))

        # Compute the prefomance score
        ksi = np.power(ksi_a * ksi_b * ksi_c, 1/3) + 1/3 * (ksi_a + ksi_b + ksi_c)

        return nmatrix, S, P, ksi_a, ksi_b, ksi_c, ksi
