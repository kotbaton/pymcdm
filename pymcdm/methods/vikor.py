# Copyright (c) 2020, 2024 Andrii Shekhovtsov

import numpy as np
from .. import helpers
from .mcda_method import MCDA_method
from ..validators import param_validator
from ..io import TableDesc


def _fake_normalization(x, cost=False):
    if cost:
        return np.max(x) - x
    else:
        return x


class VIKOR(MCDA_method):
    """ VIšekriterijumsko KOmpromisno Rangiranje (VIKOR) method.

        The VIKOR method is based on an approach that uses a compromise mechanism to evaluate alternatives using
        distance from the ideal [#vikor1]_.

        Parameters
        ----------
            normalization_function : None or callable
                Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
                where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
                cost or profit criterion.

        References
        ----------
        .. [#vikor1] Duckstein, L., & Opricovic, S. (1980). Multiobjective optimization in river basin development. Water
               resources research, 16(1), 14-20.

        Examples
        --------
        >>> from pymcdm.methods import VIKOR
        >>> import numpy as np
        >>> body = VIKOR()
        >>> matrix = np.array([[78, 56, 34, 6],
        ...                    [4, 45, 3, 97],
        ...                    [18, 2, 50, 63],
        ...                    [9, 14, 11, 92],
        ...                    [85, 9, 100, 29]])
        >>> weights = np.array([0.25, 0.25, 0.25, 0.25])
        >>> types = np.array([1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.5679, 0.7667, 1, 0.7493, 0]
    """
    _reverse_ranking = False
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Worst values of all criterion functions',
                  label='fminus', symbol='$f^{-}_{j}$', rows='C', cols=None),
        TableDesc(caption='Best values of all criterion functions',
                  label='fstar', symbol='$f^{*}_{j}$', rows='C', cols=None),
        TableDesc(caption='Vector of $S_i$ values',
                  label='s', symbol='$S_i$', rows='A', cols=None),
        TableDesc(caption='Vector of $R_i$ values',
                  label='r', symbol='$R_i$', rows='A', cols=None),
        TableDesc(caption='Vector of $Q_i$ values',
                  label='q', symbol='$Q_i$', rows='A', cols=None),
    ]

    def __init__(self, normalization_function=None, v=0.5):
        if normalization_function is None:
            self.normalization = _fake_normalization
        else:
            self.normalization = normalization_function

        param_validator(v, 'v')
        self.v = v

    def _method(self, matrix, weights, types):
        v = self.v
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)

        fstar = np.max(nmatrix, axis=0)
        fminus = np.min(nmatrix, axis=0)

        if np.any(fstar == fminus):
            eq = np.arange(fstar.shape[0])[fstar == fminus]
            raise ValueError(
                f'Criteria with indexes {eq} contains equal values for all alternatives. VIKOR method could not be '
                f'applied in this case. Consider removing this criteria from the decision matrix or use another '
                f'MCDA method.'
            )

        weighted_ff = weights * ((fstar - nmatrix) / (fstar - fminus))
        S = np.sum(weighted_ff, axis=1)
        R = np.max(weighted_ff, axis=1)

        Sstar = np.min(S)
        Sminus = np.max(S)
        Rstar = np.min(R)
        Rminus = np.max(R)

        Q = v * (S - Sstar) / (Sminus - Sstar) \
            + (1 - v) * (R - Rstar) / (Rminus - Rstar)

        return nmatrix, fminus, fstar, S, R, Q
