# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .decision_matrix_base import DecisionMatrixWeightsBase


class ITARA(DecisionMatrixWeightsBase):
    """
    A subclass of DecisionMatrixWeightsBase implementing the ITARA method [#itara1]_.

    ITARA (Indifference Threshold-based Attribute RAtio Analysis) determines criteria weights
    based on indifference thresholds provided by the decision-maker and a decision matrix.
    The method evaluates how well criteria differentiate between alternatives by computing
    distances relative to given indifference thresholds.

    Parameters
    ----------
    t : np.ndarray | list | tuple
        Vector of indifference thresholds, one per criterion. Values must be >= 0.
    p : float, optional
        Parameter for the Lp metric (default is 1). Must be >= 1.
        Common values: 1 (Manhattan), 2 (Euclidean), np.inf (l-infinity).

    Examples
    --------
    >>> from pymcdm.weights.subjective import ITARA
    >>> import numpy as np
    >>> matrix = np.array([
    ...     [250, 16, 12, 5],
    ...     [200, 20,  8, 3],
    ...     [300, 12, 16, 4],
    ...     [275, 18, 10, 6]
    ... ])
    >>> t = [30, 3, 2, 1]
    >>> itara = ITARA(t=t, p=1)
    >>> weights = itara(matrix)

    References
    ----------
    .. [#itara1] Hatefi, M.A. (2019). Indifference threshold-based attribute ratio analysis:
       A method for assigning the weights to the attributes in multiple attribute decision
       making. Applied Soft Computing Journal, 74, 643–651.
    """

    def __init__(self,
                 t: np.ndarray | list | tuple,
                 p: float = 1):
        super().__init__()

        self.t = np.asarray(t, dtype=float)
        self.p = float(p)

        if np.any(self.t < 0):
            raise ValueError('All indifference thresholds in t must be >= 0.')
        if self.p < 1:
            raise ValueError('Parameter p must be >= 1.')

    def __call__(self, matrix: np.ndarray = None) -> np.ndarray:
        """
        Calculate weights based on the decision matrix and indifference thresholds.

        Parameters
        ----------
        matrix : np.ndarray, optional
            Decision matrix (alternatives in rows, criteria in columns).

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        if matrix is not None:
            self.set_matrix(matrix)

        if self._matrix is None:
            raise ValueError('Decision matrix must be provided.')

        if self._matrix.shape[1] != len(self.t):
            raise ValueError(
                f'Number of criteria in matrix ({self._matrix.shape[1]}) '
                f'does not match length of t ({len(self.t)}).'
            )

        if np.any(self._matrix < 0):
            import warnings
            warnings.warn(
                'Decision matrix contains negative values. '
                'ITARA is defined for strictly positive data (Hatefi, 2019).',
                UserWarning, stacklevel=2
            )

        if self._weights is None:
            self._weights = self._calculate_weights()
        return self._weights

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights using the ITARA algorithm (Hatefi, 2019).

        Returns
        -------
        np.ndarray
            Vector of criteria weights.
        """
        matrix = self._matrix
        m, n = matrix.shape

        col_sums = matrix.sum(axis=0)
        col_sums_safe = np.where(col_sums == 0, 1.0, col_sums)
        alpha = matrix / col_sums_safe
        NIT = self.t / col_sums_safe

        beta = np.sort(alpha, axis=0)
        gamma = np.diff(beta, axis=0)
        delta = np.maximum(gamma - NIT, 0.0)

        if np.isinf(self.p):
            v = np.max(delta, axis=0)
        else:
            v = np.sum(delta ** self.p, axis=0) ** (1.0 / self.p)

        total_v = v.sum()
        if total_v == 0:
            return np.ones(n) / n
        return v / total_v
