# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from .hellwig import _normalize
from ..io import TableDesc


class MIDIA(MCDA_method):
    """ Multi-criteria method Integrating Distances to Ideal and Anti-ideal points (MIDIA) [#midia1]_.

        An extension of Hellwig's method, which combines the closeness to the ideal solution and the distance from the
        anti-ideal solution, both related to the distance between these solutions.

        Read more in the User Guide.

        Parameters
        ----------
            alpha : float
                Coefficient of importance of the distance to the ideal solution, in [0, 1]; 1 gives the pure
                aggressive (ideal-based) strategy and 0 the pure conservative (anti-ideal-based) strategy. Default is
                0.5.
            normalization_function : callable | None
                Function used to normalize the columns of the matrix, as in :class:`HELLWIG`. None (default) means
                the standardization (z-score with the population standard deviation).

        References
        ----------
        .. [#midia1] Roszkowska, E., & Filipowicz-Chomko, M. (2024). A multi-criteria method integrating distances
               to ideal and anti-ideal points. Symmetry, 16(8), 1025.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import MIDIA
        >>> matrix = np.array([[16, 50, 98, 20, 64],
        ...                    [11, 50, 97, 23, 68],
        ...                    [17, 29, 90, 23, 70],
        ...                    [8, 55, 98, 22, 54],
        ...                    [11, 43, 91, 18, 56],
        ...                    [9, 58, 86, 10, 50],
        ...                    [18, 44, 82, 5, 49],
        ...                    [4, 25, 85, 14, 66],
        ...                    [6, 35, 80, 8, 59],
        ...                    [3, 38, 78, 5, 58]])
        >>> weights = np.ones(5) / 5
        >>> types = np.ones(5)
        >>> np.round(MIDIA(alpha=0.5)(matrix, weights, types), 3).tolist()
        [0.818, 0.793, 0.662, 0.641, 0.544, 0.458, 0.406, 0.356, 0.269, 0.217]
    """
    _tables = [
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol=r'$\tilde{x}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Closeness to the ideal solution',
                  label='DI', symbol='$DI_i$', rows='A', cols=None),
        TableDesc(caption='Distance from the anti-ideal solution',
                  label='DAI', symbol='$DAI_i$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol=r'$D(\alpha)_i$', rows='A', cols=None),
    ]

    def __init__(self, alpha=0.5, normalization_function=None):
        if not 0 <= alpha <= 1:
            raise ValueError(f'alpha should be in [0, 1], but is {alpha}.')
        self.alpha = alpha
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        # Weighted normalized matrix, ideal and anti-ideal solutions (Eqs. 3-10)
        wnmatrix = _normalize(matrix, self.normalization) * weights
        ideal = np.where(types == 1, np.max(wnmatrix, axis=0), np.min(wnmatrix, axis=0))
        anti_ideal = np.where(types == 1, np.min(wnmatrix, axis=0), np.max(wnmatrix, axis=0))

        # Distances (Eqs. 11-12) related to the distance between the ideal and anti-ideal solutions (Eqs. 13-14)
        d_ideal = np.sqrt(np.sum((wnmatrix - ideal) ** 2, axis=1))
        d_anti_ideal = np.sqrt(np.sum((wnmatrix - anti_ideal) ** 2, axis=1))
        d = np.sqrt(np.sum((ideal - anti_ideal) ** 2))
        DI = 1 - d_ideal / d
        DAI = d_anti_ideal / d

        # Final measure (Eq. 15)
        pref = self.alpha * DI + (1 - self.alpha) * DAI

        return wnmatrix, DI, DAI, pref

    def _additional_validation(self, matrix, weights, types):
        if np.any(np.max(matrix, axis=0) == np.min(matrix, axis=0)):
            raise ValueError('All criteria should have at least two different values.')
