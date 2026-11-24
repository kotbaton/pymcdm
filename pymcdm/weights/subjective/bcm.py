# Copyright (c) 2026 Bartłomiej Kizielewicz

import warnings

import numpy as np
from .optimization_base import OptimizationWeightsBase


class BCM(OptimizationWeightsBase):
    """
    A subclass of OptimizationWeightsBase implementing the BCM (Base-Criterion Method) [#bcm1]_.

    In BCM, one criterion is chosen as a base-criterion and pairwise comparisons between the
    base-criterion and other criteria are obtained. A min-max optimization problem is solved
    to determine the weights. BCM requires only ``n - 1`` comparisons and achieves zero
    inconsistency (ξ = 0) by construction.

    Parameters
    ----------
    a_b : np.ndarray | list | tuple
        Base-to-others comparison vector. Element ``a_b[j]`` indicates the relative
        importance of the base-criterion over criterion ``j`` on the scale from 1/9 to 9.
        The base-criterion element should have value 1. All values must be > 0.
    base_index : int, optional
        Index of the base-criterion. Auto-detected as the index where ``a_b[j] == 1``
        if only one such element exists.

    Attributes
    ----------
    xi : float or None
        Optimal value of ξ (consistency indicator). For consistent input, ξ = 0.

    Examples
    --------
    >>> from pymcdm.weights.subjective import BCM
    >>> bcm = BCM(a_b=[8, 2, 1])
    >>> weights = bcm()
    >>> print(np.round(weights, 4))
    [0.0769 0.3077 0.6154]
    >>> print(round(bcm.xi, 4))
    0.0

    References
    ----------
    .. [#bcm1] Haseli, G., Sheikh, R., & Sana, S. S. (2020). Base-criterion on multi-criteria
               decision-making method and its applications. International Journal of Management
               Science and Engineering Management, 15(2), 79-88.
    """

    def __init__(self,
                 a_b: np.ndarray | list | tuple,
                 base_index: int = None):
        super().__init__()

        self.a_b = np.asarray(a_b, dtype=float)
        self.xi = None

        if np.any(self.a_b <= 0):
            raise ValueError('All comparison values in a_b must be > 0.')

        if base_index is not None:
            if base_index < 0 or base_index >= len(self.a_b):
                raise ValueError(
                    f'base_index must be in range [0, {len(self.a_b) - 1}], '
                    f'but got {base_index}.'
                )
            self._base_index = base_index
        else:
            ones_mask = np.isclose(self.a_b, 1.0)
            ones_count = np.sum(ones_mask)
            if ones_count == 0:
                raise ValueError(
                    'Cannot auto-detect base-criterion: no element in a_b equals 1. '
                    'Please provide base_index explicitly.'
                )
            if ones_count > 1:
                raise ValueError(
                    f'Cannot auto-detect base-criterion: {ones_count} elements in a_b '
                    f'equal 1. Please provide base_index explicitly.'
                )
            self._base_index = int(np.argmax(ones_mask))

        if not np.isclose(self.a_b[self._base_index], 1.0):
            self.a_b = self.a_b / self.a_b[self._base_index]

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights by solving the BCM min-max optimization problem (Eq. 6 from [#bcm1]_).

        For a fixed xi the constraints are linear in the weights, so the model is solved to its
        global optimum by bisection on xi, each step being a linear feasibility problem.

        Returns
        -------
        np.ndarray
            Vector of criteria weights.
        """
        n = len(self.a_b)
        B = self._base_index
        ratios = [(B, j, self.a_b[j]) for j in range(n) if j != B]
        w, self.xi = self._minimize_ratio_deviation(ratios, n)
        return w

    def get_xi(self) -> float:
        """
        Return the optimal value of ξ (consistency indicator).

        Returns
        -------
        float
            The optimal ξ value. For BCM with consistent input, ξ = 0.
        """
        if self._weights is None:
            self()
        return self.xi

    def get_full_matrix(self) -> np.ndarray:
        """
        Construct the complete pairwise comparison matrix from the base-comparisons (Eq. 2).

        Returns
        -------
        np.ndarray
            Complete ``n x n`` pairwise comparison matrix.
        """
        n = len(self.a_b)
        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                matrix[i, j] = self.a_b[j] / self.a_b[i]

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i, j] < 1.0 / 9.0 - 1e-9 or matrix[i, j] > 9.0 + 1e-9:
                    warnings.warn(
                        f'Final comparison a[{i},{j}] = {matrix[i, j]:.4f} is outside '
                        f'the scale [1/9, 9].',
                        UserWarning
                    )
        return matrix
