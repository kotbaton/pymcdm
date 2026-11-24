# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .subjective_weights_base import SubjectiveWeightsBase


class VIMM(SubjectiveWeightsBase):
    """
    A subclass of SubjectiveWeightsBase implementing the VIMM (Vital-Immaterial-Mediocre)
    method [#vimm1]_.

    VIMM determines criteria weights through iterative pairwise comparisons, distance
    measuring, and scoring. The decision-maker classifies criteria as vital (most impactful),
    immaterial (least impactful), or mediocre. In each round, remaining criteria are compared
    against the current vital and immaterial references, and scores are accumulated.

    This class implements the first scenario (one-goal decision-making).

    Parameters
    ----------
    n_criteria : int
        Total number of criteria (>= 4).
    vital_index : int
        Index (0-based) of the initial vital criterion.
    immaterial_index : int
        Index (0-based) of the initial immaterial criterion.
    c_vital : list of np.ndarray | list | tuple
        Comparison vectors per round. ``c_vital[k]`` contains values when comparing
        the vital criterion of round ``k`` with remaining criteria. Values in [2, 9].
    c_immaterial : list of np.ndarray | list | tuple
        Comparison vectors per round. ``c_immaterial[k]`` contains values when comparing
        the immaterial criterion of round ``k`` with remaining criteria. Values in [2, 9].

    Examples
    --------
    >>> from pymcdm.weights.subjective import VIMM
    >>> c_vital = [[9, 7.5, 8, 6.5, 7], [8, 8.5, 7]]
    >>> c_immaterial = [[9, 8, 8.5, 6, 7.5], [8.5, 9, 8]]
    >>> vimm = VIMM(n_criteria=7, vital_index=0, immaterial_index=4,
    ...             c_vital=c_vital, c_immaterial=c_immaterial)
    >>> weights = vimm()
    >>> print(np.round(weights, 3))
    [0.286 0.243 0.186 0.192 0.014 0.027 0.05 ]

    References
    ----------
    .. [#vimm1] Zakeri, S., Ecer, F., Konstantas, D., & Cheikhrouhou, N. (2023).
                The vital-immaterial-mediocre multi-criteria decision-making method.
                Kybernetes, 52(3), 937-963.
    """

    VITAL_SCORE = 5.0
    IMMATERIAL_SCORE = 1.0

    def __init__(self,
                 n_criteria: int,
                 vital_index: int,
                 immaterial_index: int,
                 c_vital: list,
                 c_immaterial: list):
        super().__init__()

        self._total_scores = None

        self.n_criteria = n_criteria
        self.vital_index = vital_index
        self.immaterial_index = immaterial_index

        self.c_vital = [np.asarray(c, dtype=float) for c in c_vital]
        self.c_immaterial = [np.asarray(c, dtype=float) for c in c_immaterial]

        # With three criteria no comparison round is made (Phase 5 stops when one criterion remains), so the
        # importance of the remaining criterion would not be expressed at all
        if n_criteria < 4:
            raise ValueError('n_criteria must be at least 4, so that at least one comparison round is made.')

        if not (0 <= vital_index < n_criteria):
            raise ValueError(
                f'vital_index must be in range [0, {n_criteria - 1}], '
                f'got {vital_index}.'
            )

        if not (0 <= immaterial_index < n_criteria):
            raise ValueError(
                f'immaterial_index must be in range [0, {n_criteria - 1}], '
                f'got {immaterial_index}.'
            )

        if vital_index == immaterial_index:
            raise ValueError('vital_index and immaterial_index must be different.')

        if len(self.c_vital) != len(self.c_immaterial):
            raise ValueError(
                f'c_vital and c_immaterial must have the same number of rounds, '
                f'but have {len(self.c_vital)} and {len(self.c_immaterial)}.'
            )

        expected_rounds = (n_criteria - 2) // 2
        if len(self.c_vital) != expected_rounds:
            raise ValueError(
                f'Expected {expected_rounds} comparison rounds for {n_criteria} criteria, '
                f'but got {len(self.c_vital)}.'
            )

        remaining_count = n_criteria - 2
        for k in range(expected_rounds):
            if self.c_vital[k].ndim != 1 or self.c_immaterial[k].ndim != 1:
                raise ValueError(
                    f'Comparison vectors for round {k} must be one-dimensional.'
                )

            if len(self.c_vital[k]) != remaining_count:
                raise ValueError(
                    f'c_vital[{k}] must have {remaining_count} elements, '
                    f'got {len(self.c_vital[k])}.'
                )

            if len(self.c_immaterial[k]) != remaining_count:
                raise ValueError(
                    f'c_immaterial[{k}] must have {remaining_count} elements, '
                    f'got {len(self.c_immaterial[k])}.'
                )

            if np.any(self.c_vital[k] < 2) or np.any(self.c_vital[k] > 9):
                raise ValueError(
                    f'All comparison values in c_vital[{k}] must be in the interval [2, 9].'
                )

            if np.any(self.c_immaterial[k] < 2) or np.any(self.c_immaterial[k] > 9):
                raise ValueError(
                    f'All comparison values in c_immaterial[{k}] must be in the interval [2, 9].'
                )

            remaining_count -= 2

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate criteria weights using the VIMM first scenario algorithm.

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        n = self.n_criteria
        V = self.VITAL_SCORE
        I = self.IMMATERIAL_SCORE

        total_columns = (n + 1) // 2

        assignment_round = np.full(n, -1, dtype=int)
        is_vital = np.zeros(n, dtype=bool)
        computed_scores_sum = np.zeros(n)

        assignment_round[self.vital_index] = 0
        is_vital[self.vital_index] = True

        assignment_round[self.immaterial_index] = 0
        is_vital[self.immaterial_index] = False

        settled = {self.vital_index, self.immaterial_index}
        remaining = sorted(set(range(n)) - settled)

        for k in range(len(self.c_vital)):
            cv = self.c_vital[k]
            ci = self.c_immaterial[k]

            # Calculate distances
            d_plus = ci - I
            d_minus = 2.0 * V - cv

            # Normalize (Eqs. 1-2)
            d_plus_norm = d_plus / np.max(d_plus)
            d_minus_norm = np.min(d_minus) / d_minus

            # Compute scores (Eq. 3)
            scores = d_plus_norm + d_minus_norm

            for i, idx in enumerate(remaining):
                computed_scores_sum[idx] += scores[i]

            # Determine new vital and immaterial
            best_local = int(np.argmax(scores))
            worst_local = int(np.argmin(scores))
            if best_local == worst_local:
                raise ValueError(f"All remaining criteria have the same score in comparison {k + 1}, so a vital "
                                 "and an immaterial criterion cannot be selected.")

            new_vital_idx = remaining[best_local]
            new_immaterial_idx = remaining[worst_local]

            assignment_round[new_vital_idx] = k + 1
            is_vital[new_vital_idx] = True

            assignment_round[new_immaterial_idx] = k + 1
            is_vital[new_immaterial_idx] = False

            settled.update([new_vital_idx, new_immaterial_idx])
            remaining = sorted(set(range(n)) - settled)

            if len(remaining) == 1:
                last_idx = remaining[0]
                assignment_round[last_idx] = k + 1
                is_vital[last_idx] = True
                settled.add(last_idx)
                remaining = []

        # Compute final weights (Eqs. 4-5)
        total_scores = np.zeros(n)
        for j in range(n):
            r = assignment_round[j]
            if is_vital[j]:
                bonus = V * (total_columns - r)
            else:
                bonus = I

            total_scores[j] = computed_scores_sum[j] + bonus

        self._total_scores = total_scores
        weights = total_scores / np.sum(total_scores)
        return weights

    def get_scores(self) -> np.ndarray:
        """
        Return total (non-normalized) scores for each criterion.

        Returns
        -------
        np.ndarray
            Vector of total scores (Eq. 4) before normalization.
        """
        if self._weights is None:
            self()
        return self._total_scores.copy()
