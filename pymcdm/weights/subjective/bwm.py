# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .optimization_base import OptimizationWeightsBase


class BWM(OptimizationWeightsBase):
    """
    A subclass of OptimizationWeightsBase implementing the BWM (Best-Worst Method) [#bwm1]_.

    BWM determines criteria weights by solving the original nonlinear optimization model.
    The decision-maker provides two comparison vectors: best-to-others and others-to-worst.
    Weights are obtained by minimizing the maximum absolute deviation.

    Parameters
    ----------
    a_b : np.ndarray | list | tuple
        Best-to-others comparison vector. The best criterion should have value 1.
    a_w : np.ndarray | list | tuple
        Others-to-worst comparison vector. The worst criterion should have value 1.

    Examples
    --------
    >>> from pymcdm.weights.subjective import BWM
    >>> bwm = BWM(a_b=[1, 3, 5, 7], a_w=[7, 5, 3, 1])
    >>> weights = bwm()
    >>> print(weights)

    References
    ----------
    .. [#bwm1] Rezaei, J. (2015). Best-worst multi-criteria decision-making method.
               Omega, 53, 49-57.
    """

    def __init__(self,
                 a_b: np.ndarray | list | tuple,
                 a_w: np.ndarray | list | tuple):
        super().__init__()

        self._xi = None

        self.a_b = np.asarray(a_b, dtype=float)
        self.a_w = np.asarray(a_w, dtype=float)

        if self.a_b.ndim != 1 or self.a_w.ndim != 1:
            raise ValueError('a_b and a_w must be one-dimensional arrays.')

        if len(self.a_b) != len(self.a_w):
            raise ValueError(
                f'a_b and a_w must have the same length, but have lengths '
                f'{len(self.a_b)} and {len(self.a_w)}.'
            )

        if np.any(self.a_b <= 0) or np.any(self.a_w <= 0):
            raise ValueError('All comparison values must be positive.')

        if np.sum(np.isclose(self.a_b, 1.0)) < 1:
            raise ValueError('a_b must contain at least one value equal to 1 (the best criterion).')

        if np.sum(np.isclose(self.a_w, 1.0)) < 1:
            raise ValueError('a_w must contain at least one value equal to 1 (the worst criterion).')

    def _calculate_weights(self) -> np.ndarray:
        """
        Solve the original nonlinear BWM optimization problem from [#bwm1]_.

        Returns
        -------
        np.ndarray
            Vector of criteria weights.
        """
        a_b = self.a_b
        a_w = self.a_w
        n = len(a_b)

        best_idx = int(np.where(np.isclose(a_b, 1.0))[0][0])
        worst_idx = int(np.where(np.isclose(a_w, 1.0))[0][0])

        recip = 1.0 / a_b
        w0 = recip / np.sum(recip)

        def residuals(w):
            values = []
            for j in range(n):
                values.append(abs(w[best_idx] / w[j] - a_b[j]))
                values.append(abs(w[j] / w[worst_idx] - a_w[j]))
            return np.asarray(values, dtype=float)

        xi0 = float(np.max(residuals(w0)))
        x0 = np.concatenate([w0, [xi0]])

        constraints = [{'type': 'eq', 'fun': lambda x: float(np.sum(x[:n]) - 1.0)}]

        for j in range(n):
            def make_c1(j=j): return lambda x: float(x[-1] - (x[best_idx] / x[j] - a_b[j]))
            def make_c2(j=j): return lambda x: float(x[-1] - (a_b[j] - x[best_idx] / x[j]))
            def make_c3(j=j): return lambda x: float(x[-1] - (x[j] / x[worst_idx] - a_w[j]))
            def make_c4(j=j): return lambda x: float(x[-1] - (a_w[j] - x[j] / x[worst_idx]))
            constraints.extend([
                {'type': 'ineq', 'fun': make_c1(j)},
                {'type': 'ineq', 'fun': make_c2(j)},
                {'type': 'ineq', 'fun': make_c3(j)},
                {'type': 'ineq', 'fun': make_c4(j)},
            ])

        bounds = [(1e-6, 1.0)] * n + [(0.0, None)]

        result = self._solve_optimization(lambda x: float(x[-1]), x0, bounds, constraints)

        weights = self._normalize_weights(result.x[:n])
        self._xi = float(result.x[-1])
        return weights

    def get_xi(self) -> float:
        """
        Return the optimal value of xi (consistency indicator).

        Returns
        -------
        float
            The optimal xi value. Smaller values indicate better consistency.
        """
        if self._weights is None:
            self()

        if self._xi is not None:
            return self._xi

        n = len(self.a_b)
        best_idx = int(np.where(np.isclose(self.a_b, 1.0))[0][0])
        worst_idx = int(np.where(np.isclose(self.a_w, 1.0))[0][0])

        xi = 0.0
        for j in range(n):
            xi = max(xi, abs(self._weights[best_idx] / self._weights[j] - self.a_b[j]))
            xi = max(xi, abs(self._weights[j] / self._weights[worst_idx] - self.a_w[j]))
        return float(xi)
