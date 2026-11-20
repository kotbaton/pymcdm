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
