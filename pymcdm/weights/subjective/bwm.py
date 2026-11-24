# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .optimization_base import OptimizationWeightsBase


class BWM(OptimizationWeightsBase):
    """
    A subclass of OptimizationWeightsBase implementing the BWM (Best-Worst Method) [#bwm1]_.

    BWM determines criteria weights from two comparison vectors provided by the decision-maker:
    best-to-others and others-to-worst. Weights are obtained by minimizing the maximum absolute
    deviation of the weight ratios from the comparisons. The original nonlinear model [#bwm1]_ is
    solved to its global optimum by bisection on the deviation with linear feasibility problems.
    For more than three not fully consistent criteria it may have multiple optimal solutions,
    whose ranges are given by ``get_weight_intervals`` [#bwm2]_. The linear model [#bwm2]_
    always has a unique solution.

    Parameters
    ----------
    a_b : np.ndarray | list | tuple
        Best-to-others comparison vector. The best criterion should have value 1.
    a_w : np.ndarray | list | tuple
        Others-to-worst comparison vector. The worst criterion should have value 1.
    model : str, optional
        Optimization model. 'nonlinear' minimizes the largest deviation of the weight ratios
        from the comparisons, as in the original BWM [#bwm1]_ (default). 'linear' minimizes the
        largest absolute value of ``w_B - a_Bj w_j`` and ``w_j - a_jW w_W``, as in the linear
        BWM [#bwm2]_. Can also be changed later by setting the `model` attribute, which clears
        cached weights.

    Examples
    --------
    >>> from pymcdm.weights.subjective import BWM
    >>> bwm = BWM(a_b=[1, 3, 5, 7], a_w=[7, 5, 3, 1])
    >>> weights = bwm()
    >>> print(np.round(weights, 4))
    [0.5333 0.2667 0.1333 0.0667]

    Multiple optimal solutions of the nonlinear model and the unique solution of the linear model:

    >>> bwm = BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 2, 3, 1])
    >>> lower, upper = bwm.get_weight_intervals()
    >>> print(np.round(lower, 4), np.round(upper, 4))
    [0.2145 0.4461 0.1085 0.1563 0.0548] [0.2289 0.4571 0.1176 0.1602 0.0561]
    >>> bwm.model = 'linear'
    >>> print(np.round(bwm(), 4), round(bwm.get_xi(), 4))
    [0.2295 0.4481 0.1148 0.153  0.0546] 0.0109

    References
    ----------
    .. [#bwm1] Rezaei, J. (2015). Best-worst multi-criteria decision-making method.
               Omega, 53, 49-57.
    .. [#bwm2] Rezaei, J. (2016). Best-worst multi-criteria decision-making method: Some
               properties and a linear model. Omega, 64, 126-130.
    """

    MODELS = ('nonlinear', 'linear')

    def __init__(self,
                 a_b: np.ndarray | list | tuple,
                 a_w: np.ndarray | list | tuple,
                 model: str = 'nonlinear'):
        super().__init__()

        self._xi = None
        self.model = model

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

        if len(self.a_b) < 2:
            raise ValueError('At least two criteria are required.')

        # Validates the best and the worst criterion
        self._best_worst()

    @property
    def model(self) -> str:
        """ Optimization model ('nonlinear' or 'linear'). """
        return self._model

    @model.setter
    def model(self, value: str):
        if value not in self.MODELS:
            raise ValueError(f'Unknown model {value!r}. Available models: {", ".join(self.MODELS)}.')
        self._model = value
        # Cached weights and xi were derived with the previous model
        self._weights = None
        self._xi = None

    def _ratios(self) -> list:
        """ Comparisons as ``(numerator, denominator, value)`` triples of weight indices. """
        a_b, a_w = self.a_b, self.a_w
        n = len(a_b)
        best_idx, worst_idx = self._best_worst()
        ratios = [(best_idx, j, a_b[j]) for j in range(n) if j != best_idx]
        ratios += [(j, worst_idx, a_w[j]) for j in range(n) if j != worst_idx]
        return ratios

    def _calculate_weights(self) -> np.ndarray:
        """
        Solve the original nonlinear BWM optimization problem (model (6) in [#bwm1]_) or the
        linear BWM model (model (19) in [#bwm2]_).

        For a fixed xi the constraints |w_B / w_j - a_Bj| <= xi and |w_j / w_W - a_jW| <= xi are
        linear in the weights, because w_j > 0. The smallest feasible xi is therefore found by
        bisection, each step being a linear feasibility problem (see
        ``OptimizationWeightsBase._minimize_ratio_deviation``). This yields the global optimum
        of the nonconvex model, which a local nonlinear solver may miss.

        If several criteria have a value of 1 in ``a_b`` (or ``a_w``), the best (worst) criterion is
        the one with the largest value in ``a_w`` (``a_b``), i.e. a_BW = a_WB.

        Returns
        -------
        np.ndarray
            Vector of criteria weights.
        """
        if self.model == 'linear':
            weights, self._xi = self._minimize_linear_deviation(self._ratios(), len(self.a_b))
        else:
            weights, self._xi = self._minimize_ratio_deviation(self._ratios(), len(self.a_b))
        return weights

    @staticmethod
    def _reference_index(a_ref: np.ndarray, a_other: np.ndarray) -> int:
        """ Index of the reference (best or worst) criterion, resolving ties by a_BW = a_WB. """
        candidates = np.where(np.isclose(a_ref, 1.0))[0]
        return int(candidates[np.argmax(a_other[candidates])])

    def _best_worst(self):
        """ Indices of the best and the worst criterion, checked as in Rezaei (2015).

            The best and the worst criterion are different criteria (if several criteria are the best or the worst,
            one is chosen, footnote 4 of [#bwm1]_), and the preference of the best criterion over the worst one,
            a_BW, is a single judgment, so it has to be the same in both vectors (Definition 3 of [#bwm1]_).
        """
        a_b, a_w = self.a_b, self.a_w
        best = self._reference_index(a_b, a_w)
        worst = self._reference_index(a_w, a_b)
        if best == worst:
            # Another candidate for the worst criterion, e.g. when all criteria are equally important
            others = [j for j in np.where(np.isclose(a_w, 1.0))[0] if j != best]
            if not others:
                raise ValueError(f'Criterion {best} is both the best (a_b = 1) and the worst (a_w = 1) criterion; '
                                 'the best and the worst criterion should be different.')
            worst = int(others[0])
        if not np.isclose(a_b[worst], a_w[best]):
            raise ValueError(f'The preference of the best criterion ({best}) over the worst one ({worst}) should be '
                             f'the same in a_b and a_w, but is {a_b[worst]:g} and {a_w[best]:g}.')
        return best, worst

    def get_xi(self) -> float:
        """
        Return the optimal value of xi (consistency indicator).

        For the linear model this is xi^L [#bwm2]_, which is not comparable with the
        Consistency Index of the nonlinear model.

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
        best_idx, worst_idx = self._best_worst()

        xi = 0.0
        for j in range(n):
            xi = max(xi, abs(self._weights[best_idx] / self._weights[j] - self.a_b[j]))
            xi = max(xi, abs(self._weights[j] / self._weights[worst_idx] - self.a_w[j]))
        return float(xi)

    def get_weight_intervals(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Return the ranges of the optimal weights of the nonlinear model (models (5) and (6)
        in [#bwm2]_).

        For not fully consistent comparisons of more than three criteria the nonlinear model may
        have multiple optimal solutions. The bounds are the smallest and the largest value of
        each weight among the weight vectors with the optimal xi. Their centers can be used as
        representative weights.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            Lower and upper bounds of the weights.
        """
        if self.model != 'nonlinear':
            raise ValueError('Weight intervals are defined for the nonlinear model only; '
                             'the linear model has a unique solution.')
        return self._ratio_weight_bounds(self._ratios(), len(self.a_b), self.get_xi())

    def get_interval_preference_degrees(self) -> np.ndarray:
        """
        Return the matrix of degrees of preference of the weight intervals (Eqs. (14)-(16)
        in [#bwm2]_).

        The element ``[i, j]`` is the degree to which the weight interval of criterion ``i`` is
        greater than that of criterion ``j``. Criteria can be ranked by the number of elements
        greater than 0.5 in their rows (matrix of preferences, Eq. (17) in [#bwm2]_).

        Returns
        -------
        np.ndarray
            Square matrix of degrees of preference.
        """
        lower, upper = self.get_weight_intervals()
        n = len(lower)
        dp = np.full((n, n), 0.5)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                width = (upper[i] - lower[i]) + (upper[j] - lower[j])
                if width > 0:
                    dp[i, j] = (max(0.0, upper[i] - lower[j]) - max(0.0, lower[i] - upper[j])) / width
                elif not np.isclose(lower[i], lower[j]):
                    dp[i, j] = float(lower[i] > lower[j])
        return dp
