# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .optimization_base import OptimizationWeightsBase


class COBRAC(OptimizationWeightsBase):
    """
    A subclass of OptimizationWeightsBase implementing the COBRAC weighting method [#cobrac1]_.

    COBRAC (COmparisons Between RAnked Criteria) obtains weights from pairwise comparisons
    of ranked criteria. For each ordered pair (i, j), the decision-maker specifies a share
    ``xi`` in (0, 1) representing the local importance ratio between the two criteria.

    Parameters
    ----------
    n_criteria : int
        Total number of criteria in the model.
    pairs : array-like of shape (m, 2)
        Sequence of index pairs ``(i, j)`` describing local comparisons. Index ``i`` denotes
        the more important criterion and ``j`` the less important one. Zero-based.
    xis : array-like of shape (m,)
        Share parameters in (0, 1), one per pair. For pair ``(i, j)``:\
        ``w[i] : w[j] = xi : (1 - xi)``.

    Examples
    --------
    >>> from pymcdm.weights.subjective import COBRAC
    >>> cobrac = COBRAC(n_criteria=3, pairs=[(0, 1), (1, 2)], xis=[0.7, 0.6])
    >>> weights = cobrac()

    References
    ----------
    .. [#cobrac1] Pamucar, D., Simic, V., Gorcun, O. F., & Kucukonder, H. (2024).
                  Selection of the best Big Data platform using COBRAC-ARTASI
                  methodology with adaptive standardized intervals. Expert Systems
                  with Applications, 239, 122312.
    """

    def __init__(self, n_criteria: int, pairs, xis):
        super().__init__()

        self._delta: float | None = None

        if n_criteria <= 0:
            raise ValueError('n_criteria must be a positive integer.')
        self.n_criteria = int(n_criteria)

        pairs = np.asarray(pairs, dtype=int)
        xis = np.asarray(xis, dtype=float)

        if pairs.ndim != 2 or pairs.shape[1] != 2:
            raise ValueError('pairs must be an array-like of shape (m, 2).')
        if pairs.shape[0] == 0:
            raise ValueError('At least one comparison pair must be provided.')
        if pairs.shape[0] != xis.shape[0]:
            raise ValueError('pairs and xis must have the same length.')
        if np.any(pairs < 0) or np.any(pairs >= self.n_criteria):
            raise ValueError('Criterion indices in pairs must be in range [0, n_criteria).')
        if np.any(xis <= 0.0) or np.any(xis >= 1.0):
            raise ValueError('All xi values must be in the open interval (0, 1).')

        self.pairs = pairs
        self.xis = xis
        self._ratios = self.xis / (1.0 - self.xis)

    def _calculate_weights(self) -> np.ndarray:
        """
        Solve the COBRAC nonlinear optimization problem from [#cobrac1]_.

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        n = self.n_criteria

        w0 = np.full(n, 1.0 / n, dtype=float)

        def max_deviation(w):
            vals = [abs(w[i] / w[j] - r) for (i, j), r in zip(self.pairs, self._ratios, strict=False)]
            return max(vals) if vals else 0.0

        delta0 = max_deviation(w0)
        x0 = np.concatenate([w0, [delta0]])

        constraints = [{'type': 'eq', 'fun': lambda x: float(np.sum(x[:n]) - 1.0)}]

        for (i, j), r_ij in zip(self.pairs, self._ratios, strict=False):
            def make_c1(i=i, j=j, r=r_ij):
                return lambda x: float(x[-1] - (x[i] / x[j] - r))
            def make_c2(i=i, j=j, r=r_ij):
                return lambda x: float(x[-1] - (r - x[i] / x[j]))
            constraints.append({'type': 'ineq', 'fun': make_c1()})
            constraints.append({'type': 'ineq', 'fun': make_c2()})

        bounds = [(1e-8, 1.0)] * n + [(0.0, None)]

        result = self._solve_optimization(
            lambda x: float(x[-1]), x0, bounds, constraints,
            options={'ftol': 1e-12, 'maxiter': 5000}
        )

        w = self._normalize_weights(result.x[:n])
        self._delta = float(result.x[-1])
        return w

    def get_delta(self) -> float:
        """
        Return the optimal deviation parameter ``delta``.

        Returns
        -------
        float
            Smaller values indicate better global consistency.
        """
        if self._weights is None:
            self()

        if self._delta is None:
            w = self._weights
            vals = [abs(w[i] / w[j] - r) for (i, j), r in zip(self.pairs, self._ratios, strict=False)]
            self._delta = max(vals) if vals else 0.0
        return float(self._delta)
