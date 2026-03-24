# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .ordered_criteria_base import OrderedCriteriaWeightsBase


class PIPRECIA(OrderedCriteriaWeightsBase):
    """
    A subclass of OrderedCriteriaWeightsBase implementing the PIPRECIA (PIvot Pairwise RElative
    Criteria Importance Assessment) method [#piprecia1]_.

    PIPRECIA extends the SWARA method by allowing the decision-maker to indicate that a
    criterion at position ``j+1`` is more important than at position ``j``. Values > 1 mean
    the next criterion is more important, = 1 means equal, and < 1 means less important.
    All values must satisfy ``0 < s_v[j] < 2``.

    Parameters
    ----------
    s : np.ndarray | list | tuple
        Criteria indices in decreasing order of expected importance.
    s_v : np.ndarray | list | tuple
        Relative significance values. Length must be ``len(s) - 1``.
        Each ``s_v[j]`` compares criterion at position ``j+1`` to criterion at position ``j``.

    Examples
    --------
    >>> from pymcdm.weights.subjective import PIPRECIA
    >>> s = [0, 1, 2, 3, 4, 5]
    >>> s_v = [1.0, 1.0, 0.75, 1.0, 0.8]
    >>> piprecia = PIPRECIA(s=s, s_v=s_v)
    >>> weights = piprecia()
    >>> print(weights)
    [0.19 0.19 0.19 0.15 0.15 0.13]

    References
    ----------
    .. [#piprecia1] Stanujkić, D., Zavadskas, E. K., Karabašević, D., Smarandache, F.,
                    & Turskis, Z. (2017). The use of the PIvot Pairwise RElative Criteria
                    Importance Assessment method for determining the weights of criteria.
                    Romanian Journal of Economic Forecasting, 20(4), 116-133.
    """

    def __init__(self,
                 s: np.ndarray | list | tuple,
                 s_v: np.ndarray | list | tuple):
        super().__init__(order=s)

        self.s_v = np.asarray(s_v, dtype=float)

        if len(self.s_v) != self.n - 1:
            raise ValueError(
                f's_v should have length {self.n - 1} (len(s) - 1), '
                f'but has length {len(self.s_v)}.'
            )

        if np.any(self.s_v <= 0):
            raise ValueError('All values in s_v must be > 0.')

        if np.any(self.s_v >= 2):
            raise ValueError(
                'All values in s_v must be < 2 to ensure a positive coefficient '
                'k_j = 2 - s_v[j] > 0 (see Eq. 7 in Stanujkić et al. 2017).')

    # backward-compatible alias
    @property
    def s(self):
        return self.order

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using the PIPRECIA algorithm.

        Returns
        -------
        np.ndarray
            Vector of criteria weights indexed by original criteria order.
        """
        # Calculate coefficient k_j (Eq. 7)
        k = np.ones(self.n)
        k[1:] = 2 - self.s_v

        # Calculate recalculated weight q_j (Eq. 8)
        q = np.ones(self.n)
        for j in range(1, self.n):
            q[j] = q[j - 1] / k[j]

        # Normalize and reindex (Eq. 9)
        w_ordered = q / np.sum(q)
        return self._reindex_from_order(w_ordered)
