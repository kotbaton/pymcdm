# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .decision_matrix_base import DecisionMatrixWeightsBase


class OWCM(DecisionMatrixWeightsBase):
    """
    A subclass of DecisionMatrixWeightsBase implementing the OWCM (Opinion Weight Criteria
    Method) [#owcm1]_.

    OWCM derives criteria weights from a crisp opinion matrix where decision-makers assess each
    alternative against the ideal solution using a five-point Likert scale (1 = No Difference,
    5 = Huge Difference). The method achieves zero inconsistency by comparing values within the
    same criterion rather than between different criteria.

    Parameters
    ----------
    M : np.ndarray | list | tuple
        Crisp opinion matrix of shape ``(m, n)`` where ``m`` is the number of
        alternatives and ``n`` is the number of criteria. Values must be in range 1–5.

    Examples
    --------
    >>> from pymcdm.weights.subjective import OWCM
    >>> import numpy as np
    >>> M = np.array([
    ...     [1, 1, 1],
    ...     [2, 3, 1],
    ...     [3, 1, 2],
    ...     [3, 2, 3],
    ... ])
    >>> owcm = OWCM(M=M)
    >>> weights = owcm()
    >>> print(np.round(weights, 4))
    [0.3333 0.3333 0.3333]

    References
    ----------
    .. [#owcm1] Ahmed Mandil, A. D., Salih, M. M., & Muhsen, Y. R. (2024).
       Opinion Weight Criteria Method (OWCM): A New Method for Weighting
       Criteria With Zero Inconsistency. IEEE Access, 12, 5605–5616.
    """

    def __init__(self,
                 M: np.ndarray | list | tuple):
        M_arr = np.asarray(M, dtype=float)

        if M_arr.ndim != 2:
            raise ValueError(
                f'Crisp opinion matrix M should be 2-dimensional, but has shape {M_arr.shape}.'
            )

        if np.any((M_arr < 1) | (M_arr > 5)):
            raise ValueError(
                'All values in the crisp opinion matrix M must be in the range 1–5.'
            )

        super().__init__(matrix=M_arr)

    # backward-compatible alias
    @property
    def M(self):
        return self._matrix

    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights from the crisp opinion matrix (Eqs. 4–8 from [#owcm1]_).

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        # Step 2: Column normalization (Eq. 4)
        col_max = np.max(self._matrix, axis=0)
        R = self._matrix / col_max

        # Step 3: Mean of each criterion (Eq. 5)
        N_bar = np.mean(R, axis=0)

        # Step 4: Preference variation (Eq. 6)
        phi = np.sum((R - N_bar) ** 2, axis=0)

        # Step 5: Deviation of preference values (Eq. 7)
        omega = 1 - phi
        if np.any(omega < 0):
            raise ValueError(f'Preference variations exceed 1 for criteria with indices {np.flatnonzero(omega < 0)} '
                             f'(phi = {np.round(phi[omega < 0], 4)}), which would give them negative weights. '
                             'The OWCM weights are not applicable to this opinion matrix.')

        # Step 6: Normalize to final weights (Eq. 8)
        return omega / np.sum(omega)
