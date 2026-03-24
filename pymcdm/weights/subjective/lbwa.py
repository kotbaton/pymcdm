# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .subjective_weights_base import SubjectiveWeightsBase


class LBWA(SubjectiveWeightsBase):
    """
    A subclass of SubjectiveWeightsBase implementing the LBWA (Level Based Weight Assessment) method [#lbwa1]_.

    LBWA groups criteria into levels of significance, where level 1 contains the most important
    criteria. Within each level, criteria are further differentiated by integer comparison
    values (I_pi). An elasticity coefficient allows additional fine-tuning of weights.

    Parameters
    ----------
    i : list of lists
        Criteria indices grouped by level of significance. The first sublist
        is the most important level (S1), the second is S2, etc. Levels may
        be empty (``[]``) to represent gaps in significance.
    l : np.ndarray | list | tuple
        Flat list of integer comparison values I_pi for each criterion, in
        the same order as they appear when iterating through ``i``. The most
        important criterion must receive value 0.
    r0 : int | float | None, optional
        Elasticity coefficient. Must satisfy r0 > r. If None, defaults to r + 1.

    Examples
    --------
    >>> from pymcdm.weights.subjective import LBWA
    >>> import numpy as np
    >>> i = [[1, 4, 6, 5, 0, 2], [7, 3]]
    >>> l = [0, 2, 3, 4, 4, 5, 1, 2]
    >>> lbwa = LBWA(i=i, l=l, r0=7)
    >>> weights = lbwa()
    >>> print(np.round(weights, 3))
    [0.121 0.191 0.111 0.084 0.148 0.121 0.134 0.089]

    References
    ----------
    .. [#lbwa1] Zizovic, M., & Pamucar, D. (2019). New model for determining
       criteria weights: Level Based Weight Assessment (LBWA) model.
       Decision Making: Applications in Management and Engineering, 2(2), 126-137.
    """

    def __init__(self,
                 i: list,
                 l: np.ndarray | list | tuple,
                 r0: int | float | None = None):
        super().__init__()
        self.criteria_order = i
        self.internal_structure = np.asarray(l, dtype=float)
        self.r0 = r0

        # Validate total number of l values
        total_criteria = sum(len(group) for group in self.criteria_order)
        if len(self.internal_structure) != total_criteria:
            raise ValueError(
                f'l should have length {total_criteria} (total number of '
                f'criteria), but has length {len(self.internal_structure)}.'
            )

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using the LBWA algorithm (Zizovic & Pamucar 2019).

        Returns
        -------
        np.ndarray
            Vector of criteria weights indexed by original criteria order.
        """
        # Step 3 / Eq. (2): r = maximum group size across all non-empty levels
        non_empty = [group for group in self.criteria_order if len(group) > 0]
        if not non_empty:
            raise ValueError("criteria_order contains no criteria.")
        r = max(len(group) for group in non_empty)

        # Step 4: elasticity coefficient r0 > r
        r0 = self.r0 if self.r0 is not None else r + 1
        if r0 <= r:
            raise ValueError(
                f'Elasticity coefficient r0 ({r0}) must be greater than '
                f'r ({r}). The authors recommend r0 = r + 1 as a starting value.'
            )

        # Validate that all I_pi values are within [0, r]
        if np.any(self.internal_structure < 0) or np.any(self.internal_structure > r):
            raise ValueError(
                f'All values in l must be in the range [0, r] = [0, {r}].'
            )

        # Step 5 / Eq. (3): influence function f(C_pi) = r0 / (i * r0 + I_pi)
        all_criteria = []
        idx = 0
        for level_idx, group in enumerate(self.criteria_order):
            i = level_idx + 1  # 1-indexed level number
            for criterion in group:
                I_pi = self.internal_structure[idx]
                f = r0 / (i * r0 + I_pi)
                all_criteria.append((criterion, f))
                idx += 1

        # Steps 6 / Eq. (4) and (5): normalise
        total_f = sum(f for _, f in all_criteria)
        n_criteria = max(c for c, _ in all_criteria) + 1
        w = np.zeros(n_criteria)
        for criterion, f in all_criteria:
            w[criterion] = f / total_f

        return w
