# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .grouped_ranks_base import GroupedRanksBase


class SRF(GroupedRanksBase):
    """
    A subclass of GroupedRanksBase implementing the revised Simos procedure (SRF)
    for weight determination [#srf1]_.

    Three improvements over the original :class:`SIMOS` method: (1) the decision-maker
    explicitly states the ratio ``z`` between the most and least important criterion,
    (2) tied criteria receive identical weights, and (3) optimal rounding ensures weights
    sum to exactly 100.

    Parameters
    ----------
    r : list | tuple
        Criteria indices from least to most important. Use inner lists for ties
        (e.g. ``[[0, 1], 2, 3]``).
    w_c : np.ndarray | list | tuple
        Number of white cards between consecutive rank positions.
        Length must be ``number_of_positions - 1``. All values >= 0.
    z : float
        Ratio of the weight of the most important criterion to the least important. Must be >= 1.
    w : int, optional
        Decimal places for normalized output (0, 1, or 2). Default is 0.

    Examples
    --------
    >>> from pymcdm.weights.subjective import SRF
    >>> r = [[2, 6, 11], [3], [1, 5, 8, 9], [4], [0, 7], [10]]
    >>> w_c = [0, 1, 0, 0, 0]
    >>> srf = SRF(r=r, w_c=w_c, z=6.5, w=1)
    >>> weights = srf()
    >>> print(np.round(100 * weights, 1))
    [13.2  8.9  2.4  4.5 11.   8.9  2.4 13.2  8.9  8.9 15.3  2.4]

    References
    ----------
    .. [#srf1] Figueira, J., & Roy, B. (2002). Determining the weights of criteria in the
               ELECTRE type methods with a revised Simos' procedure. European Journal of
               Operational Research, 139(2), 317-326.
    """

    def __init__(self,
                 r:   list | tuple,
                 w_c: np.ndarray | list | tuple,
                 z:   float,
                 w:   int = 0):
        super().__init__(ranks=r, gaps=w_c)
        self.z = float(z)
        self.w = int(w)

        # z states how many times the most important criterion is more important than the least important one
        # (Figueira & Roy, 2002, Section 3.2.1)
        if self.z < 1:
            raise ValueError(f'z must be at least 1, but is {self.z}.')
        if self.w not in (0, 1, 2):
            raise ValueError('w must be 0, 1, or 2.')

    # backward-compatible aliases
    @property
    def r(self):
        return self.ranks

    @property
    def w_c(self):
        return self.gaps

    def _non_normalized_weights(self) -> np.ndarray:
        """
        Compute non-normalized weights k(r) per rank (Section 3.2.1).

        Returns
        -------
        np.ndarray
            Non-normalized weight for each rank group.
        """
        e_prime  = self.gaps
        e_r      = e_prime + 1
        e        = float(np.sum(e_r))
        u        = round((self.z - 1) / e, 6)

        cumulative = np.concatenate([[0.0], np.cumsum(e_r)])
        k_r = np.array(
            [round(1.0 + u * cumulative[r], 2) for r in range(len(self.positions))]
        )
        return k_r

    def _optimal_round(self, k_star: np.ndarray) -> np.ndarray:
        """
        Round normalized weights to ``self.w`` decimal places with sum = 100.

        Implements lexicographic minimization of rounding errors (Section 3.2.2).

        Parameters
        ----------
        k_star : np.ndarray
            Exact normalized weights summing to 100.

        Returns
        -------
        np.ndarray
            Rounded weights summing to exactly 100.
        """
        multiplier = 10 ** self.w
        step       = 10 ** (-self.w)

        k_floor   = np.floor(k_star * multiplier) / multiplier
        K_floor   = np.sum(k_floor)
        m         = round((100.0 - K_floor) * multiplier)

        n = len(k_star)

        d_plus  = (step - (k_star - k_floor)) / k_star
        d_minus = (k_star - k_floor)           / k_star

        M     = {i for i in range(n) if d_plus[i] < d_minus[i]}
        not_M = set(range(n)) - M
        m_hat = len(M)

        if m_hat <= m:
            not_M_sorted = sorted(not_M, key=lambda i: (d_plus[i], -i))
            to_promote   = set(not_M_sorted[: m - m_hat])
            F_plus       = M | to_promote
        else:
            # Ties keep the criteria with the higher subscripts in F+ (Figueira & Roy, 2002, Section 3.2.2)
            M_sorted    = sorted(M, key=lambda i: (d_minus[i], i))
            to_demote   = set(M_sorted[: m_hat - m])
            F_plus      = M - to_demote

        k_rounded = k_floor.copy()
        for i in F_plus:
            k_rounded[i] += step

        k_rounded = np.where(k_rounded <= 0, step, k_rounded)

        return k_rounded

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using the revised Simos procedure.

        Returns
        -------
        np.ndarray
            Normalized criteria weights (sum = 1), indexed by original criterion order.
        """
        # Non-normalized weights k(r) per rank
        k_r = self._non_normalized_weights()

        # Assign k'_i to each criterion
        k_prime = self._expand_rank_values(k_r)

        # k*_i = (100 / K0) * k'_i
        K0     = np.sum(k_prime)
        k_star = 100.0 * k_prime / K0

        # Optimal rounding
        k_rounded = self._optimal_round(k_star)

        return k_rounded / 100.0
