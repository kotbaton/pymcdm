# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from .r_topsis import RTOPSIS
from ..validators import bounds_validator, matrix_bounds_validator
from ..io import TableDesc


class RVIKOR(MCDA_method):
    """ R-VIKOR method [#rvikor1]_.

        R-VIKOR removes the dependence of VIKOR on the set of alternatives by normalizing every criterion on its
        historical (or admissible) minimum and maximum instead of on the values in the decision matrix, and by fixing
        the positive and negative ideal solutions at the ends of that domain, as R-TOPSIS does for TOPSIS. The score
        of an alternative therefore does not change when other alternatives are added, removed or replaced, and the
        method is defined also when classical VIKOR divides by zero.

        Read more in the User Guide.

        Parameters
        ----------
            bounds : ndarray
                Domain of every criterion: [historical minimum, historical maximum] for each criterion in rows.
                Values in the decision matrix must lie within the domain, unless `clip` is True. The domain can be
                obtained with :meth:`RTOPSIS.make_bounds` or :meth:`RTOPSIS.expand_bounds`.
            v : float
                Weight of the strategy of the maximum group utility, in [0, 1]. Default is 0.5.
            clip : bool
                If True, values outside the domain are clipped to its ends before normalization. Default is False.

        References
        ----------
        .. [#rvikor1] Yang, W., & Wu, Y. (2020). A new improvement method to avoid rank reversal in VIKOR. IEEE Access,
               8, 21261-21271.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import RVIKOR
        >>> matrix = np.array([[78, 56, 34, 6],
        ...                    [4, 45, 3, 97],
        ...                    [18, 2, 50, 63],
        ...                    [9, 14, 11, 92],
        ...                    [85, 9, 100, 29]])
        >>> weights = np.ones(4) / 4
        >>> types = np.ones(4)
        >>> bounds = np.array([[0, 100]] * 4)
        >>> body = RVIKOR(bounds)
        >>> preferences = body(matrix, weights, types)
        >>> np.round(preferences, 5).tolist()
        [0.7525, 0.79875, 0.82375, 0.7975, 0.67625]
        >>> body.rank(preferences).tolist()
        [2.0, 4.0, 5.0, 3.0, 1.0]
    """
    _reverse_ranking = False
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Group utility',
                  label='S', symbol='$S_i$', rows='A', cols=None),
        TableDesc(caption='Individual regret',
                  label='R', symbol='$R_i$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='NQ', symbol='$NQ_i$', rows='A', cols=None),
    ]

    def __init__(self, bounds, v=0.5, clip=False):
        self.bounds = np.asarray(bounds, dtype='float')
        bounds_validator(self.bounds)
        if not 0 <= v <= 1:
            raise ValueError(f'v should be in [0, 1], but is {v}.')
        self.v = v
        self.clip = clip

    def _method(self, matrix, weights, types):
        if self.clip:
            matrix = np.clip(matrix, self.bounds[:, 0], self.bounds[:, 1])
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]

        # Normalization on the domain: 1 is the historical best, 0 the historical worst value (Eqs. 9-10)
        nmatrix = np.where(types == 1, (matrix - lower) / (upper - lower), (upper - matrix) / (upper - lower))

        # Fixed ideal solutions N+ = 1 and N- = 0 (Eqs. 11-12)
        regret = weights * (1 - nmatrix)
        S = np.sum(regret, axis=1)
        R = np.max(regret, axis=1)

        # S+ = 1, S- = 0, R+ = max(w), R- = 0 (Eqs. 16-18)
        NQ = self.v * S + (1 - self.v) * R / np.max(weights)

        return nmatrix, S, R, NQ

    def _additional_validation(self, matrix, weights, types):
        if self.bounds.shape[0] != matrix.shape[1]:
            raise ValueError(f'Number of domains ({self.bounds.shape[0]}) should be equal '
                             f'to the number of criteria ({matrix.shape[1]}).')
        if not self.clip:
            matrix_bounds_validator(matrix, self.bounds)

    make_bounds = staticmethod(RTOPSIS.make_bounds)
    expand_bounds = staticmethod(RTOPSIS.expand_bounds)
