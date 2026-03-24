# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .ordered_criteria_base import OrderedCriteriaWeightsBase


class SWARA(OrderedCriteriaWeightsBase):
    """
    A subclass of OrderedCriteriaWeightsBase implementing the SWARA (Step-wise Weight Assessment
    Ratio Analysis) method [#swara1]_.

    The SWARA method determines criteria weights based on successive pairwise comparisons.
    Criteria are ranked from most to least important, then for each criterion (starting from
    the second) the decision-maker states how much more important the previous criterion is.

    Parameters
    ----------
    s : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance.
    s_v : np.ndarray | list | tuple
        Comparative importance of successive criteria. Length must be ``len(s) - 1``.
        Each ``s_v[j]`` states how much more important criterion at position ``j`` is
        compared to criterion at position ``j+1``. Values must be >= 0.

    Examples
    --------
    >>> from pymcdm.weights.subjective import SWARA
    >>> s = [0, 1, 2, 3, 4, 5]
    >>> s_v = [0.15, 0.04, 0.29, 0.02, 0.04]
    >>> swara = SWARA(s=s, s_v=s_v)
    >>> weights = swara()
    >>> print(weights)
    [0.22 0.19 0.18 0.14 0.14 0.13]

    References
    ----------
    .. [#swara1] Keršulienė, V., Zavadskas, E. K., & Turskis, Z. (2010). Selection of rational
                 dispute resolution method by applying new step-wise weight assessment ratio
                 analysis (SWARA). Journal of Business Economics and Management, 11(2), 243-258.
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

        if np.any(self.s_v < 0):
            raise ValueError('All values in s_v must be >= 0.')

    # backward-compatible alias
    @property
    def s(self):
        return self.order

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using the SWARA algorithm.

        Returns
        -------
        np.ndarray
            Vector of criteria weights indexed by original criteria order.
        """
        # Calculate coefficient k_j
        k = np.ones(self.n)
        k[1:] = self.s_v + 1

        # Calculate recalculated weight q_j
        q = np.ones(self.n)
        for j in range(1, self.n):
            q[j] = q[j - 1] / k[j]

        # Normalize and reindex
        w_ordered = q / np.sum(q)
        return self._reindex_from_order(w_ordered)
