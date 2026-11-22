# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from scipy.optimize import brentq
from .ordered_criteria_base import OrderedCriteriaWeightsBase


class ROC(OrderedCriteriaWeightsBase):
    """
    Rank Order Centroid (ROC) weights [#roc1]_.

    The weights are the centroid of the set of all weight vectors consistent with the ranking of the criteria
    :math:`w_1 \\geq w_2 \\geq \\ldots \\geq w_n \\geq 0`, :math:`\\sum_j w_j = 1`. The weight of the criterion
    at position :math:`i` of the ranking is

    .. math:: w_i = \\frac{1}{n} \\sum_{k=i}^{n} \\frac{1}{k}

    Parameters
    ----------
    order : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance.

    Examples
    --------
    >>> from pymcdm.weights.subjective import ROC
    >>> np.round(ROC([0, 1, 2, 3])(), 4).tolist()
    [0.5208, 0.2708, 0.1458, 0.0625]

    References
    ----------
    .. [#roc1] Barron, F. H., & Barrett, B. E. (1996). Decision quality using ranked attribute weights. Management
               Science, 42(11), 1515-1523.
    """

    def _calculate_weights(self) -> np.ndarray:
        reciprocals = 1 / np.arange(1, self.n + 1)
        ordered = np.cumsum(reciprocals[::-1])[::-1] / self.n
        return self._reindex_from_order(ordered)


class RS(OrderedCriteriaWeightsBase):
    """
    Rank Sum (RS) weights [#rs1]_.

    The weight of the criterion at position :math:`i` of the ranking is proportional to :math:`n - i + 1`:

    .. math:: w_i = \\frac{n - i + 1}{\\sum_{k=1}^{n} (n - k + 1)} = \\frac{2 (n - i + 1)}{n (n + 1)}

    Parameters
    ----------
    order : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance.

    Examples
    --------
    >>> from pymcdm.weights.subjective import RS
    >>> np.round(RS([0, 1, 2, 3])(), 4).tolist()
    [0.4, 0.3, 0.2, 0.1]

    References
    ----------
    .. [#rs1] Stillwell, W. G., Seaver, D. A., & Edwards, W. (1981). A comparison of weight approximation
              techniques in multiattribute utility decision making. Organizational Behavior and Human Performance,
              28(1), 62-77.
    """

    def _calculate_weights(self) -> np.ndarray:
        ordered = np.arange(self.n, 0, -1, dtype=float)
        return self._reindex_from_order(ordered / np.sum(ordered))


class RR(OrderedCriteriaWeightsBase):
    """
    Rank Reciprocal (RR) weights [#rr1]_.

    The weight of the criterion at position :math:`i` of the ranking is proportional to :math:`1 / i`:

    .. math:: w_i = \\frac{1 / i}{\\sum_{k=1}^{n} 1 / k}

    Parameters
    ----------
    order : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance.

    Examples
    --------
    >>> from pymcdm.weights.subjective import RR
    >>> np.round(RR([0, 1, 2, 3])(), 4).tolist()
    [0.48, 0.24, 0.16, 0.12]

    References
    ----------
    .. [#rr1] Stillwell, W. G., Seaver, D. A., & Edwards, W. (1981). A comparison of weight approximation
              techniques in multiattribute utility decision making. Organizational Behavior and Human Performance,
              28(1), 62-77.
    """

    def _calculate_weights(self) -> np.ndarray:
        ordered = 1 / np.arange(1, self.n + 1)
        return self._reindex_from_order(ordered / np.sum(ordered))


class RE(OrderedCriteriaWeightsBase):
    """
    Rank Exponent (RE) weights [#re1]_.

    The weight of the criterion at position :math:`i` of the ranking is proportional to :math:`(n - i + 1)^z`:

    .. math:: w_i = \\frac{(n - i + 1)^z}{\\sum_{k=1}^{n} (n - k + 1)^z}

    The exponent :math:`z` is given directly or determined from the weight of the most important criterion judged
    by the decision maker. :math:`z = 0` gives equal weights and :math:`z = 1` gives rank sum weights.

    Parameters
    ----------
    order : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance.
    z : float | None
        Exponent, must be >= 0. Exactly one of `z` and `w_top` should be given.
    w_top : float | None
        Weight of the most important criterion, in [1/n, 1). The exponent is found numerically so that the most
        important criterion obtains this weight.

    Examples
    --------
    >>> from pymcdm.weights.subjective import RE
    >>> np.round(RE([0, 1, 2, 3], z=2)(), 4).tolist()
    [0.5333, 0.3, 0.1333, 0.0333]
    >>> re = RE([0, 1, 2, 3], w_top=0.4)
    >>> round(re.z, 4), np.round(re(), 4).tolist()
    (1.0, [0.4, 0.3, 0.2, 0.1])

    References
    ----------
    .. [#re1] Stillwell, W. G., Seaver, D. A., & Edwards, W. (1981). A comparison of weight approximation
              techniques in multiattribute utility decision making. Organizational Behavior and Human Performance,
              28(1), 62-77.
    """

    def __init__(self,
                 order: np.ndarray | list | tuple,
                 z: float | None = None,
                 w_top: float | None = None):
        super().__init__(order=order)

        if (z is None) == (w_top is None):
            raise ValueError('Exactly one of z and w_top should be given.')

        if z is not None:
            if z < 0:
                raise ValueError(f'z must be >= 0, but is {z}.')
            self.z = float(z)
        else:
            if not 1 / self.n <= w_top < 1:
                raise ValueError(f'w_top must be in [1/n, 1) = [{1 / self.n:.4f}, 1), but is {w_top}.')
            self.z = self._solve_z(w_top)
        self.w_top = w_top

    def _ordered(self, z):
        values = np.arange(self.n, 0, -1, dtype=float) ** z
        return values / np.sum(values)

    def _solve_z(self, w_top):
        if np.isclose(w_top, 1 / self.n):
            return 0.0
        upper = 1.0
        while self._ordered(upper)[0] < w_top:
            upper *= 2
        return brentq(lambda z: self._ordered(z)[0] - w_top, 0, upper, xtol=1e-12)

    def _calculate_weights(self) -> np.ndarray:
        return self._reindex_from_order(self._ordered(self.z))
