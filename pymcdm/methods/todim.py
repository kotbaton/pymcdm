# Copyright (c) 2025 Vaishnudebi Dutta, Subhomoy Haldar

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method
from ..io import TableDesc


class TODIM(MCDA_method):
    """ TOmada de Decisão Interativa e Multicritério (TODIM).

        The TODIM method is based on prospect theory and evaluates alternatives through
        pairwise dominance degrees that model the psychology of risk — gains are weighted
        differently from losses, controlled by the attenuation factor theta [#todim1]_.

        Parameters
        ----------
            normalization_function : callable
                Function which should be used to normalize `matrix` columns.
                It should match signature ``foo(x, cost)``, where ``x`` is a vector
                to be normalized and ``cost`` is a bool indicating a cost criterion.
                Defaults to :func:`~pymcdm.normalizations.todim_normalization`.

            theta : float
                Attenuation factor (risk aversion parameter) for the loss domain.
                Must be positive. Higher values make the method more risk-averse.
                Default is 2.5.

        References
        ----------
        .. [#todim1] Dutta, V., & Haldar, S. (2025). Performance Comparison of TODIM and
           CPT-TODIM in Social Sustainability Assessment for G7 Countries. International
           Journal of Information Technology & Decision Making.
           https://doi.org/10.1142/S021962202550097X

           Based on the original method by Gomes, L. F. A. M., & Lima, M. M. P. P. (1991).
           TODIM: Basics and application to multicriteria ranking of projects with
           environmental impacts. Foundations of Computing and Decision Sciences, 16(4),
           113-127.

        Examples
        --------
        >>> from pymcdm.methods import TODIM
        >>> import numpy as np
        >>> body = TODIM()
        >>> matrix = np.array([[53198.17, 64.73, 0.31, 20199.55],
        ...                    [46480.62, 66.02, 0.29, 29682.22],
        ...                    [53637.80, 76.09, 0.28, 43769.63]])
        >>> weights = np.array([0.038095, 0.07619, 0.009524, 0.133333])
        >>> weights = weights / weights.sum()
        >>> types = np.array([1, 1, -1, 1])
        >>> [round(p, 4) for p in body(matrix, weights, types)]
        [0.0, 0.251, 1.0]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$P_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Relative criterion weights',
                  label='rel_weights', symbol='$w_{rc}$', rows='C', cols=None),
        TableDesc(caption='Global dominance matrix',
                  label='dominance', symbol='$\\delta(A_i, A_j)$', rows='A', cols='A'),
        TableDesc(caption='Sum of dominance degrees',
                  label='delta_sum', symbol='$\\sum_j \\delta(A_i, A_j)$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$\\xi_i$', rows='A', cols=None),
    ]

    def __init__(self, normalization_function=normalizations.todim_normalization, theta=2.5):
        if theta <= 0:
            raise ValueError(f"Parameter 'theta' must be positive, got {theta}.")
        self.normalization = normalization_function
        self.theta = theta

    def _method(self, matrix, weights, types):
        n, m = matrix.shape
        theta = self.theta

        # Step 1: Normalize decision matrix (Eq. 2)
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)

        # Step 2: Relative criterion weights (Eq. 3)
        w_r = np.max(weights)
        rel_weights = weights / w_r
        sum_rel = np.sum(rel_weights)

        # Step 3: Pairwise dominance degrees (Eqs. 4-5)
        dominance = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                delta = 0.0
                for c in range(m):
                    diff = nmatrix[i, c] - nmatrix[j, c]
                    if diff > 0:
                        delta += np.sqrt(diff * rel_weights[c] / sum_rel)
                    elif diff < 0:
                        delta -= (1.0 / theta) * np.sqrt(sum_rel * (-diff) / rel_weights[c])
                dominance[i, j] = delta

        # Step 4: Global performance score (Eq. 6)
        delta_sum = np.sum(dominance, axis=1)
        d_min = np.min(delta_sum)
        d_max = np.max(delta_sum)
        if d_max == d_min:
            xi = np.ones(n)
        else:
            xi = (delta_sum - d_min) / (d_max - d_min)

        return nmatrix, rel_weights, dominance, delta_sum, xi
