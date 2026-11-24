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
    >>> print(np.round(weights, 4))
    [0.5833 0.25   0.1667]

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
        if np.any(pairs[:, 0] == pairs[:, 1]):
            raise ValueError('A criterion cannot be compared with itself.')

        # Every criterion has to be connected with the others by comparisons, otherwise its weight is undefined
        connected = {0}
        changed = True
        while changed:
            changed = False
            for i, j in pairs:
                if (i in connected) != (j in connected):
                    connected.update((int(i), int(j)))
                    changed = True
        if len(connected) != self.n_criteria:
            missing = sorted(set(range(self.n_criteria)) - connected)
            raise ValueError(f'The comparisons should connect all criteria, but criteria {missing} are not connected '
                             'with criterion 0.')

        self.pairs = pairs
        self.xis = xis
        self._ratios = self.xis / (1.0 - self.xis)

    def _calculate_weights(self) -> np.ndarray:
        """
        Solve the COBRAC nonlinear optimization problem (model (4) in [#cobrac1]_).

        For a fixed delta the constraints are linear in the weights, so the model is solved to its
        global optimum by bisection on delta, each step being a linear feasibility problem.

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        ratios = [(i, j, r) for (i, j), r in zip(self.pairs, self._ratios, strict=True)]
        w, self._delta = self._minimize_ratio_deviation(ratios, self.n_criteria)
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
