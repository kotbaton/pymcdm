# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .ordered_criteria_base import OrderedCriteriaWeightsBase
from .optimization_base import OptimizationWeightsBase


class FUCOM(OrderedCriteriaWeightsBase, OptimizationWeightsBase):
    """
    A subclass implementing the FUCOM (Full Consistency Method) [#fucom1]_.

    FUCOM determines criteria weights by solving a constrained nonlinear optimization problem
    that ensures full consistency of pairwise comparisons. The decision-maker ranks criteria by
    importance and specifies comparative priorities between consecutive criteria.

    Parameters
    ----------
    o : np.ndarray | list | tuple
        Ranking of criteria indices in decreasing order of importance, i.e.
        ``o[0]`` is the index of the most important criterion.
    i : np.ndarray | list | tuple or None, optional
        Comparative priority values φ_{k/(k+1)} provided directly (Step 2a).
        Length must equal ``len(o) - 1``. All values must be >= 1.
        Mutually exclusive with ``v``.
    v : np.ndarray | list | tuple or None, optional
        Significance scores on a positive scale, one per criterion in the ranked order ``o``
        (Step 2b). ``v[0]`` must be 1.0. Values must be non-decreasing.
        Mutually exclusive with ``i``.

    Attributes
    ----------
    phi : np.ndarray
        Comparative priority vector Φ = [φ_{1/2}, φ_{2/3}, ..., φ_{(n-1)/n}].
    dfc : float
        Deviation from Full Consistency (χ). Value of 0.0 means perfect consistency.

    Examples
    --------
    >>> from pymcdm.weights.subjective import FUCOM
    >>> fucom = FUCOM(o=[0, 1, 2, 3], i=[1.08, 1.25, 1.45])
    >>> weights = fucom()
    >>> print(np.round(weights, 4))
    [0.3147 0.2914 0.2331 0.1608]
    >>> print(fucom.dfc)  # 0.0

    References
    ----------
    .. [#fucom1] Pamučar, D., Stević, Ž., & Sremac, S. (2018). A new model for
       determining weight coefficients of criteria in MCDM models: Full Consistency
       Method (FUCOM). Symmetry, 10(9), 393.
    """

    def __init__(self,
                 o: np.ndarray | list | tuple,
                 i: np.ndarray | list | tuple | None = None,
                 v: np.ndarray | list | tuple | None = None):
        if i is None and v is None:
            raise ValueError(
                "Provide either comparative priorities 'i' (Step 2a) "
                "or significance scores 'v' (Step 2b)."
            )
        if i is not None and v is not None:
            raise ValueError(
                "'i' and 'v' are mutually exclusive. Provide only one."
            )

        # Initialise both bases via cooperative MRO
        super().__init__(order=o)

        # backward-compatible alias
        self.o = self.order

        if v is not None:
            v_arr = np.asarray(v, dtype=float)
            if len(v_arr) != self.n:
                raise ValueError(
                    f"'v' must have the same length as 'o' ({self.n}), "
                    f"but has length {len(v_arr)}."
                )
            if not np.isclose(v_arr[0], 1.0):
                raise ValueError("The first element of 'v' must be 1.0.")
            if np.any(np.diff(v_arr) < 0):
                raise ValueError("'v' must be non-decreasing.")
            self.phi = v_arr[1:] / v_arr[:-1]
        else:
            self.phi = np.asarray(i, dtype=float)

        if len(self.phi) != self.n - 1:
            raise ValueError(
                f"Comparative priority vector must have length {self.n - 1} "
                f"(len(o) - 1), but has length {len(self.phi)}."
            )
        if np.any(self.phi < 1.0):
            raise ValueError("All comparative priorities phi must be >= 1.0.")

        self.dfc: float = float("nan")

    def _calculate_weights(self) -> np.ndarray:
        """
        Solve the FUCOM nonlinear optimisation model (5) from [#fucom1]_.

        Returns
        -------
        np.ndarray
            Weight vector indexed by original criteria indices.
        """
        n = self.n

        if n == 1:
            self.dfc = 0.0
            return self._reindex_from_order(np.array([1.0]))

        phi = self.phi
        num_vars = n + 1  # w_0, ..., w_{n-1}, chi

        constraints = []

        # Condition (3): |w_{(k)}/w_{(k+1)} - phi_k| <= chi
        for k in range(n - 1):
            p = phi[k]
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, k=k, p=p: x[-1] - (x[k] / x[k + 1] - p)
            })
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, k=k, p=p: x[-1] + (x[k] / x[k + 1] - p)
            })

        # Condition (4): |w_{(k)}/w_{(k+2)} - phi_k*phi_{k+1}| <= chi
        for k in range(n - 2):
            prod = phi[k] * phi[k + 1]
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, k=k, prod=prod: x[-1] - (x[k] / x[k + 2] - prod)
            })
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, k=k, prod=prod: x[-1] + (x[k] / x[k + 2] - prod)
            })

        # sum(w) = 1
        constraints.append({
            'type': 'eq',
            'fun': lambda x: np.sum(x[:n]) - 1.0
        })

        bounds = [(1e-9, None)] * n + [(0.0, None)]

        x0 = np.ones(num_vars)
        x0[:n] = 1.0 / n
        x0[-1] = 0.01

        result = self._solve_optimization(
            lambda x: x[-1], x0, bounds, constraints,
            options={'ftol': 1e-12, 'maxiter': 2000, 'disp': False}
        )

        w_ordered = np.maximum(result.x[:n], 0.0)
        w_ordered /= w_ordered.sum()

        self.dfc = float(max(result.x[-1], 0.0))

        return self._reindex_from_order(w_ordered)
