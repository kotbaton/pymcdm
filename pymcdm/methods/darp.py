# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class DARP(MCDA_method):
    """ Distances to Aspiration Reference Points (DARP) method [#darp1]_.

        Every alternative is compared with an aspiration reference point, which can be common for all alternatives
        or individual for each of them (e.g. national targets of countries). The criteria are normalized between
        the worst performance of the alternatives and the aspiration level, and the values at or beyond the
        aspiration level are set to 1, so a surplus on one criterion does not compensate shortages on the others.

        Read more in the User Guide.

        Parameters
        ----------
            reference : ndarray | None
                Aspiration reference points. None (default) means the best performance of the alternatives on every
                criterion (internal common reference point). A one-dimensional array of length `n_criteria` is
                a common reference point, and a two-dimensional array of shape `(n_alternatives, n_criteria)` gives
                an individual reference point for every alternative (row) of the decision matrix.

        References
        ----------
        .. [#darp1] Roszkowska, E., Filipowicz-Chomko, M., & Wachowicz, T. (2020). Using individual and common
               reference points to measure the performance of alternatives in multiple criteria evaluation.
               Operations Research and Decisions, 30(3), 77-96.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import DARP
        >>> matrix = np.array([[3.16, 7.4, 40.8],
        ...                    [2.58, 8.9, 45.9],
        ...                    [0.75, 12.7, 32.8],
        ...                    [0.86, 3.1, 28.7],
        ...                    [3.4, 7.7, 51.3]])
        >>> weights = np.ones(3) / 3
        >>> types = np.array([1, -1, 1])
        >>> body = DARP(reference=[3, 10, 40])
        >>> np.round(body(matrix, weights, types), 3).tolist()
        [1.0, 0.892, 0.104, 0.203, 1.0]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol=r'$\bar{x}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Distances from the aspiration reference points',
                  label='d', symbol='$d_{i0}$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$DARP_i$', rows='A', cols=None),
    ]

    def __init__(self, reference=None):
        self.reference = None if reference is None else np.asarray(reference, dtype=float)
        if self.reference is not None and self.reference.ndim not in (1, 2):
            raise ValueError('reference should be a one- or two-dimensional array.')

    def _method(self, matrix, weights, types):
        best = np.where(types == 1, np.max(matrix, axis=0), np.min(matrix, axis=0))
        worst = np.where(types == 1, np.min(matrix, axis=0), np.max(matrix, axis=0))
        reference = best if self.reference is None else self.reference
        reference = np.broadcast_to(reference, matrix.shape)

        # Normalization between the worst performance and the aspiration level (Eq. 4); the aspiration level is
        # reached when it is not better than the worst performance or when the performance is not worse than it
        not_better = np.where(types == 1, reference <= worst, reference >= worst)
        span = np.where(not_better, 1, reference - worst)
        nmatrix = np.where(not_better, 1, np.minimum((matrix - worst) / span, 1))

        # Weighted distances from the weighted reference points [w_1, ..., w_m] (Eqs. 5-8)
        d = np.sqrt(np.sum((weights * (nmatrix - 1)) ** 2, axis=1))

        # Final measure (Eq. 10)
        pref = 1 - d / np.sqrt(np.sum(weights ** 2))

        return nmatrix, d, pref

    def _additional_validation(self, matrix, weights, types):
        if self.reference is None:
            return
        expected = matrix.shape[1:] if self.reference.ndim == 1 else matrix.shape
        if self.reference.shape != expected:
            raise ValueError(f'Shape of the reference points {self.reference.shape} should be {expected}.')
