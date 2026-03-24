# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .ordered_criteria_base import OrderedCriteriaWeightsBase


class SWAN(OrderedCriteriaWeightsBase):
    """
    A subclass of OrderedCriteriaWeightsBase implementing SWAN (Sequential Weighting
    with Anchored Network) [#swan1]_.

    SWAN extends SWARA by adding a small number of anchor comparisons — direct ratio
    assessments between non-adjacent criteria — that break the chain structure and reduce
    error propagation. Weights are recovered by ordinary least squares on the log-scale,
    yielding an analytical closed-form solution.

    For m = 0 anchors, the method reduces exactly to SWARA.

    Parameters
    ----------
    s : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance (identical to SWARA).
    s_v : np.ndarray | list | tuple
        Adjacent comparative importance values. Length must be ``len(s) - 1``.
        Each ``s_v[k]`` states how much more important position ``k`` is than position
        ``k+1``. Values must be >= 0.
    bridges : list of tuples, optional
        Bridge comparisons as ``(p, q, r)`` triples where ``p`` and ``q`` are
        0-based **positions** in the ranking (not criterion indices) with ``p < q``,
        and ``r > 0`` is the directly stated ratio w_{(p)} / w_{(q)}.
        If None or empty, the method reduces to SWARA.

    Attributes
    ----------
    gri : float
        Global Residual Index after weight computation.
    bci : float or None
        Bridge Consistency Index (defined only when bridges are present).

    Examples
    --------
    >>> from pymcdm.weights.subjective import SWAN
    >>> s = [0, 1, 2, 3, 4, 5]
    >>> s_v = [0.15, 0.04, 0.29, 0.02, 0.04]
    >>> bridges = [(0, 5, 1.7)]  # position 0 is 1.7× more important than position 5
    >>> sb = SWAN(s=s, s_v=s_v, bridges=bridges)
    >>> weights = sb()
    >>> print(sb.bci)

    References
    ----------
    .. [#swan1] SWAN method — manuscript in preparation.
    """

    def __init__(self,
                 s: np.ndarray | list | tuple,
                 s_v: np.ndarray | list | tuple,
                 bridges: list | None = None):
        super().__init__(order=s)

        self.s_v = np.asarray(s_v, dtype=float)
        self.gri: float = 0.0
        self.bci: float | None = None

        if len(self.s_v) != self.n - 1:
            raise ValueError(
                f's_v should have length {self.n - 1} (len(s) - 1), '
                f'but has length {len(self.s_v)}.'
            )
        if np.any(self.s_v < 0):
            raise ValueError('All values in s_v must be >= 0.')

        # Parse and validate bridges
        if bridges is None or len(bridges) == 0:
            self._bridges = []
        else:
            self._bridges = []
            for item in bridges:
                p, q, r = int(item[0]), int(item[1]), float(item[2])
                if p >= q:
                    raise ValueError(
                        f'Bridge ({p}, {q}): first position must be < second position.'
                    )
                if p < 0 or q >= self.n:
                    raise ValueError(
                        f'Bridge positions must be in [0, {self.n - 1}], '
                        f'got ({p}, {q}).'
                    )
                if r <= 0:
                    raise ValueError(
                        f'Bridge ratio must be > 0, got {r} for pair ({p}, {q}).'
                    )
                self._bridges.append((p, q, r))

    @property
    def s(self):
        """Backward-compatible alias for the ranking order."""
        return self.order

    @property
    def m(self):
        """Number of bridge comparisons."""
        return len(self._bridges)

    def _build_system(self):
        """
        Build the linear system Av = b on the log-scale.

        Returns
        -------
        A : np.ndarray, shape (n-1+m, n-1)
        b : np.ndarray, shape (n-1+m,)
        """
        n = self.n
        m = self.m
        n_eq = n - 1 + m
        n_var = n - 1  # v_2, ..., v_n (v_1 = 0)

        A = np.zeros((n_eq, n_var))
        b = np.zeros(n_eq)

        # Adjacent equations: v_k - v_{k+1} = a_k
        a = np.log(self.s_v + 1.0)
        for k in range(n - 1):
            # Equation: v_{k+1} - v_{k+2} = a_{k+1}  (1-indexed positions)
            # In 0-indexed positions: v_{pos k} - v_{pos k+1} = a_k
            # Variables are v_1, ..., v_{n-1} (0-indexed as columns 0..n-2)
            # where column j corresponds to v_{j+1} (position j+1, since v_0 = 0)
            if k == 0:
                # v_0 - v_1 = a_0  =>  -v_1 = a_0 (since v_0 = 0)
                # column 0 = v_1
                A[k, 0] = -1.0
            else:
                # v_k - v_{k+1} = a_k
                # column k-1 = v_k, column k = v_{k+1}
                A[k, k - 1] = 1.0
                A[k, k] = -1.0
            b[k] = a[k]

        # Bridge equations: v_{p} - v_{q} = c_l
        for l, (p, q, r) in enumerate(self._bridges):
            row = n - 1 + l
            c_l = np.log(r)

            # v_p - v_q = c_l
            # If p = 0: 0 - v_q = c_l => column q-1 has -1, b = c_l
            # If p > 0: column p-1 has +1, column q-1 has -1
            if p > 0:
                A[row, p - 1] = 1.0
            A[row, q - 1] = -1.0
            b[row] = c_l

        return A, b

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using log-scale OLS reconstruction.

        Returns
        -------
        np.ndarray
            Vector of criteria weights indexed by original criteria order.
        """
        n = self.n

        if self.m == 0:
            # Pure SWARA: chain multiplication (exact, no LS needed)
            k = np.ones(n)
            k[1:] = self.s_v + 1
            q = np.ones(n)
            for j in range(1, n):
                q[j] = q[j - 1] / k[j]
            w_ordered = q / np.sum(q)
            self.gri = 0.0
            self.bci = None
            return self._reindex_from_order(w_ordered)

        # Build and solve the overdetermined system
        A, b = self._build_system()
        v_hat = np.linalg.lstsq(A, b, rcond=None)[0]

        # Prepend v_0 = 0
        v_full = np.concatenate([[0.0], v_hat])

        # Compute residuals
        residuals = A @ v_hat - b
        total_eq = len(residuals)
        self.gri = float(np.sqrt(np.sum(residuals ** 2) / total_eq))

        bridge_residuals = residuals[n - 1:]
        self.bci = float(np.sqrt(np.sum(bridge_residuals ** 2) / self.m))

        # Recover weights via softmax
        v_shifted = v_full - np.max(v_full)  # numerical stability
        exp_v = np.exp(v_shifted)
        w_ordered = exp_v / np.sum(exp_v)

        return self._reindex_from_order(w_ordered)

    def get_covariance(self, sigma: float = 1.0) -> np.ndarray:
        """
        Compute the covariance matrix of log-weight estimates under iid noise.

        Assumes all observations (adjacent and bridge) have equal noise variance σ².

        Parameters
        ----------
        sigma : float
            Standard deviation of noise on log-ratio observations.

        Returns
        -------
        np.ndarray, shape (n-1, n-1)
            Covariance matrix of (v̂_2, …, v̂_n).
        """
        A, _ = self._build_system()
        ATA = A.T @ A
        return sigma ** 2 * np.linalg.inv(ATA)

    # ------------------------------------------------------------------
    # Bridge topology generators (static helpers)
    # ------------------------------------------------------------------

    @staticmethod
    def make_bridges_global(n: int) -> list:
        """
        T1: Single global bridge (position 0 vs position n-1).

        Parameters
        ----------
        n : int
            Number of criteria.

        Returns
        -------
        list of (int, int)
            Bridge pairs as (p, q) position tuples. Ratios must be added by user.
        """
        return [(0, n - 1)]

    @staticmethod
    def make_bridges_dyadic(n: int, budget: int | None = None) -> list:
        """
        T2: Dyadic bridges via recursive bisection.

        Parameters
        ----------
        n : int
            Number of criteria.
        budget : int, optional
            Maximum number of bridges. Defaults to ⌊log₂ n⌋.

        Returns
        -------
        list of (int, int)
            Bridge pairs as (p, q) position tuples.
        """
        if budget is None:
            budget = max(1, int(np.floor(np.log2(n))))
        pairs = []
        queue = [(0, n - 1)]
        while queue and len(pairs) < budget:
            a, b = queue.pop(0)
            if b - a < 2:
                continue
            pairs.append((a, b))
            mid = (a + b) // 2
            if mid > a and mid < b:
                queue.append((a, mid))
                queue.append((mid, b))
        # If we haven't filled budget yet from bisection, the (0, n-1) is first
        if not pairs:
            pairs = [(0, n - 1)]
        return pairs[:budget]

    @staticmethod
    def make_bridges_uniform(n: int, m: int) -> list:
        """
        T3: Uniform bridges from position 0 to evenly spaced positions.

        Parameters
        ----------
        n : int
            Number of criteria.
        m : int
            Number of bridges.

        Returns
        -------
        list of (int, int)
            Bridge pairs as (p, q) position tuples.
        """
        pairs = []
        for k in range(1, m + 1):
            q = round(n * k / (m + 1)) - 1
            q = max(1, min(q, n - 1))
            if (0, q) not in pairs:
                pairs.append((0, q))
        return pairs
