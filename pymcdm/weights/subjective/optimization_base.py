# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from scipy.optimize import minimize, linprog
from .subjective_weights_base import SubjectiveWeightsBase


class OptimizationWeightsBase(SubjectiveWeightsBase):
    """
    Base class for subjective weighting methods that determine weights by solving
    a constrained optimization problem (e.g. BWM, BCM, COBRAC, FUCOM).

    Provides a common ``_solve_optimization`` helper with configurable solver
    defaults and automatic failure detection.

    Parameters
    ----------
    **kwargs
        Forwarded to :class:`SubjectiveWeightsBase` (cooperative inheritance).

    Class Attributes
    ----------------
    solver_method : str
        Default scipy solver method (``'SLSQP'``).
    solver_options : dict
        Default solver options.
    """

    solver_method = "SLSQP"
    solver_options = {"ftol": 1e-12, "maxiter": 2000}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _solve_optimization(self, objective, x0, bounds, constraints,
                            method=None, options=None):
        """
        Run ``scipy.optimize.minimize`` with common defaults and error handling.

        Parameters
        ----------
        objective : callable
            Objective function to minimise.
        x0 : np.ndarray
            Initial guess.
        bounds : sequence of (min, max)
            Variable bounds.
        constraints : list of dict
            Constraint dicts accepted by scipy.
        method : str, optional
            Override ``solver_method``.
        options : dict, optional
            Override ``solver_options``.

        Returns
        -------
        scipy.optimize.OptimizeResult
            The optimisation result.

        Raises
        ------
        ValueError
            If the solver reports failure.
        """
        result = minimize(
            objective,
            x0,
            method=method or self.solver_method,
            bounds=bounds,
            constraints=constraints,
            options=options or self.solver_options,
        )
        if not result.success:
            raise ValueError(
                f"{self.__class__.__name__} optimization failed: {result.message}"
            )
        return result

    def _solve_lp(self, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
        """
        Run ``scipy.optimize.linprog`` (HiGHS solver) with common error handling.

        The problem is ``min c @ x`` subject to ``A_ub @ x <= b_ub``,
        ``A_eq @ x == b_eq`` and ``bounds``. Linear models (e.g. OPA) should
        use this helper instead of ``_solve_optimization`` to obtain the exact
        global optimum.

        Parameters
        ----------
        c : np.ndarray
            Coefficients of the linear objective function to minimise.
        A_ub, b_ub : np.ndarray, optional
            Inequality constraints.
        A_eq, b_eq : np.ndarray, optional
            Equality constraints.
        bounds : sequence of (min, max), optional
            Variable bounds. Default is ``(0, None)`` for every variable.

        Returns
        -------
        scipy.optimize.OptimizeResult
            The optimisation result.

        Raises
        ------
        ValueError
            If the solver reports failure.
        """
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                         bounds=bounds, method='highs')
        if not result.success:
            raise ValueError(
                f"{self.__class__.__name__} linear programming failed: {result.message}"
            )
        return result

    _ratio_tolerance = 1e-10

    def _minimize_ratio_deviation(self, ratios, n):
        """
        Find weights minimizing the largest deviation of weight ratios from target values.

        The model is ``min xi`` subject to ``|w_num / w_den - a| <= xi`` for every
        ``(num, den, a)`` in ``ratios``, ``sum(w) = 1`` and ``w > 0`` (e.g. BWM, FUCOM).
        For a fixed xi the constraints ``(a - xi) w_den <= w_num <= (a + xi) w_den`` are
        linear, so the smallest feasible xi is found by bisection, each step being a linear
        feasibility problem. This yields the global optimum of the nonconvex model, which
        a local nonlinear solver may miss.

        Parameters
        ----------
        ratios : sequence of (int, int, float)
            Index of the numerator weight, index of the denominator weight and the
            target value of their ratio.
        n : int
            Number of weights.

        Returns
        -------
        tuple[np.ndarray, float]
            Normalized weights and the largest deviation of their ratios from the targets.
        """
        num, den, a = self._split_ratios(ratios)

        def deviation(w):
            return float(np.max(np.abs(w[num] / w[den] - a))) if len(a) else 0.0

        def feasible(xi):
            try:
                result = self._solve_lp(np.zeros(n), A_ub=self._ratio_constraints(num, den, a, xi, n),
                                        b_ub=np.zeros(2 * len(a)), A_eq=np.ones((1, n)), b_eq=[1.0],
                                        bounds=[(1e-12, 1.0)] * n)
            except ValueError:
                return None
            return result.x

        weights = feasible(0.0)
        if weights is None:
            # Equal weights are feasible for xi equal to their deviation
            weights = np.full(n, 1.0 / n)
            lower, upper = 0.0, deviation(weights)
            while upper - lower > self._ratio_tolerance * max(1.0, upper):
                middle = (lower + upper) / 2
                candidate = feasible(middle)
                if candidate is None:
                    lower = middle
                else:
                    upper, weights = middle, candidate

        weights = self._normalize_weights(weights)
        # Deviation of the returned weights; the bisection bound may differ by the solver tolerance
        return weights, deviation(weights)

    @staticmethod
    def _split_ratios(ratios):
        """ Split ``(num, den, a)`` triples into index and value arrays. """
        num = np.array([r[0] for r in ratios], dtype=int)
        den = np.array([r[1] for r in ratios], dtype=int)
        a = np.array([r[2] for r in ratios], dtype=float)
        return num, den, a

    @staticmethod
    def _ratio_constraints(num, den, a, xi, n):
        """
        Inequality matrix of ``(a - xi) w_den <= w_num <= (a + xi) w_den`` (right-hand side 0).
        """
        A_ub = np.zeros((2 * len(a), n))
        rows = np.arange(len(a))
        # w_num - (a + xi) w_den <= 0  and  -w_num + (a - xi) w_den <= 0
        A_ub[rows, num] += 1.0
        A_ub[rows, den] -= a + xi
        A_ub[len(a) + rows, num] -= 1.0
        A_ub[len(a) + rows, den] += a - xi
        return A_ub

    def _ratio_weight_bounds(self, ratios, n, xi):
        """
        Smallest and largest value of each weight over all weight vectors whose ratios deviate
        from the targets by at most ``xi`` (e.g. models (5) and (6) in Rezaei (2016) for BWM).

        Parameters
        ----------
        ratios : sequence of (int, int, float)
            Index of the numerator weight, index of the denominator weight and the
            target value of their ratio.
        n : int
            Number of weights.
        xi : float
            Allowed deviation, usually the optimal value of ``_minimize_ratio_deviation``.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            Lower and upper bounds of the weights.
        """
        num, den, a = self._split_ratios(ratios)
        # Small relative slack keeps the optimal solution feasible despite rounding of xi
        xi = xi + self._ratio_tolerance * max(1.0, xi)
        A_ub = self._ratio_constraints(num, den, a, xi, n)
        lower, upper = np.empty(n), np.empty(n)
        for j in range(n):
            c = np.zeros(n)
            for sign, bound in ((1.0, lower), (-1.0, upper)):
                c[j] = sign
                result = self._solve_lp(c, A_ub=A_ub, b_ub=np.zeros(len(A_ub)), A_eq=np.ones((1, n)),
                                        b_eq=[1.0], bounds=[(0.0, 1.0)] * n)
                bound[j] = result.x[j]
        return lower, upper

    def _minimize_linear_deviation(self, ratios, n):
        """
        Find weights minimizing the largest absolute value of ``w_num - a w_den``.

        The model is ``min xi`` subject to ``|w_num - a w_den| <= xi`` for every ``(num, den, a)``
        in ``ratios``, ``sum(w) = 1`` and ``w >= 0`` (e.g. the linear BWM model). It is a
        linear programming problem.

        Parameters
        ----------
        ratios : sequence of (int, int, float)
            Index of the numerator weight, index of the denominator weight and the
            target value of their ratio.
        n : int
            Number of weights.

        Returns
        -------
        tuple[np.ndarray, float]
            Weights and the optimal value of xi.
        """
        num, den, a = self._split_ratios(ratios)
        rows = np.arange(len(a))
        # Variables: w_1, ..., w_n, xi
        A_ub = np.zeros((2 * len(a), n + 1))
        A_ub[rows, num] += 1.0
        A_ub[rows, den] -= a
        A_ub[len(a) + rows, num] -= 1.0
        A_ub[len(a) + rows, den] += a
        A_ub[:, n] = -1.0
        A_eq = np.zeros((1, n + 1))
        A_eq[0, :n] = 1.0
        c = np.zeros(n + 1)
        c[n] = 1.0
        result = self._solve_lp(c, A_ub=A_ub, b_ub=np.zeros(len(A_ub)), A_eq=A_eq, b_eq=[1.0],
                                bounds=[(0.0, 1.0)] * n + [(0.0, None)])
        weights = np.clip(result.x[:n], 0.0, None)
        weights = weights / weights.sum()
        return weights, float(np.max(np.abs(weights[num] - a * weights[den]))) if len(a) else 0.0

    @staticmethod
    def _normalize_weights(w: np.ndarray) -> np.ndarray:
        """
        Normalise a weight vector so that it sums to 1.

        Parameters
        ----------
        w : np.ndarray
            Raw weight vector (all elements must be non-negative).

        Returns
        -------
        np.ndarray
            Normalised weight vector.
        """
        s = np.sum(w)
        if s <= 0:
            raise ValueError("Sum of weights must be positive.")
        return w / s
