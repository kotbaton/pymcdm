# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .grouped_ranks_base import GroupedRanksBase


class SIMOS(GroupedRanksBase):
    """
    A subclass of GroupedRanksBase implementing the original Simos procedure for
    weight determination [#simos1]_.

    The decision-maker ranks criteria from least to most important using cards, inserting
    white cards between groups to indicate the magnitude of difference. Positions are
    assigned sequentially, and each rank group's weight is the average of its positions,
    normalized by the total sum of criterion positions.

    .. note::
        This is the *original* procedure (Section 2.2 of Figueira & Roy, 2002).
        For the corrected version see :class:`SRF`.

    Parameters
    ----------
    r : list | tuple
        Criteria indices from least to most important. Use inner lists for ties
        (e.g. ``[[0, 1], 2, 3]``).
    w_c : np.ndarray | list | tuple
        Number of white cards between consecutive rank positions.
        Length must be ``number_of_positions - 1``. All values >= 0.

    Examples
    --------
    >>> from pymcdm.weights.subjective import SIMOS
    >>> r = [[2, 6, 11], [3], [1, 5, 8, 9], [4], [0, 7], [10]]
    >>> w_c = [0, 1, 0, 0, 0]
    >>> simos = SIMOS(r=r, w_c=w_c)
    >>> weights = simos()

    References
    ----------
    .. [#simos1] Figueira, J., & Roy, B. (2002). Determining the weights of criteria in the
                 ELECTRE type methods with a revised Simos' procedure. European Journal of
                 Operational Research, 139(2), 317-326.
    """

    def __init__(self,
                 r:   list | tuple,
                 w_c: np.ndarray | list | tuple):
        super().__init__(ranks=r, gaps=w_c)

    # backward-compatible aliases
    @property
    def r(self):
        return self.ranks

    @property
    def w_c(self):
        return self.gaps

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using the original Simos procedure.

        Returns
        -------
        np.ndarray
            Normalized criteria weights (sum ≈ 1), indexed by original criterion order.
        """
        position = 1
        rank_positions = []

        for i, group in enumerate(self.positions):
            group_pos = list(range(position, position + len(group)))
            position += len(group)
            rank_positions.append(group_pos)

            if i < len(self.positions) - 1:
                position += int(self.gaps[i])

        # Non-normalized weight = average position within each rank group
        rank_avg = np.array([sum(pos) / len(pos) for pos in rank_positions])

        # Denominator: sum of criterion positions only (white cards excluded)
        total = sum(p for pos_list in rank_positions for p in pos_list)

        return self._expand_rank_values(rank_avg / total)
