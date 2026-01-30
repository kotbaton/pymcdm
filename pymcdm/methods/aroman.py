# Copyright (c) 2026 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc
from ..normalizations import minmax_normalization, vector_normalization
from ..helpers import normalize_matrix


class AROMAN(MCDA_method):
    """ Alternative Ranking Order Method Accounting for Two-Step Normalization (AROMAN) method [#aroman1]_.

        An idea of the AROMAN method is to use both min-max and vector normalization techniques to
        normalize the decision matrix, and then combine the results to obtain a more robust evaluation of alternatives.

        Parameters
        ----------
        beta : float
            Weighting coefficient for combining min-max and vector normalized matrices. Default is 0.5.

        lam : float
            Weighting coefficient for combining cost and profit values. Default is 0.5.

        References
        ----------
        .. [#aroman1] Bošković, S., Švadlenka, L., Jovčić, S., Dobrodolac, M., Simić, V., & Bacanin, N. (2023). An alternative ranking order method accounting for two-step normalization (AROMAN)—A case study of the electric vehicle selection problem. IEEE access, 11, 39496-39507.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import AROMAN
        >>> matrix = np.array([
        ...     [40000, 1.200, 1.4, 8, 9],
        ...     [38500, 1.150, 1.2, 6, 6],
        ...     [39400, 0.600, 1.1, 7, 5],
        ...     [48000, 1.300, 1.6, 10, 12]
        ... ])
        >>> weights = np.array([0.28, 0.22, 0.26, 0.15, 0.09])
        >>> types = np.array([-1, 1, 1, 1, 1])
        >>> aroman = AROMAN()  # Using default parameters beta=0.5, lam=0.5
        >>> results = aroman(matrix, weights, types)
        >>> print(np.round(results, 4))
        [0.6727 0.5535 0.4721 0.8718]
    """
    _tables = [
        TableDesc(caption='Min-max normalized decision matrix.',
                  label='lin_nmatrix', symbol='$t_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Vector normalized decision matrix.',
                  label='vec_nmatrix', symbol='$t^{*}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Aggregated averaged normalized matrix',
                  label='norm_nmatrix', symbol='$t^{norm}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized matrix',
                  label='wnmatrix', symbol='$\\hat{t}^{norm}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Summarized cost values',
                  label='li_values', symbol='$L_i$', rows='A', cols=None),
        TableDesc(caption='Summarized profit values',
                  label='ai_values', symbol='$A_i$', rows='A', cols=None),
        TableDesc(caption='Overall preference rating',
                  label='pref', symbol='$P_i$', rows='A', cols=None)
    ]

    def __init__(self, beta=0.5, lam=0.5):
        self.beta = beta
        self.lam = lam

    def _method(self, matrix, weights, types):
        beta, lam = self.beta, self.lam

        lin_matrix = normalize_matrix(matrix, minmax_normalization, None)
        vec_matrix = normalize_matrix(matrix, vector_normalization, None)

        avg_matrix = (beta * lin_matrix + (1 - beta) * vec_matrix) / 2

        weighted_matrix = avg_matrix * weights

        Li = np.sum(weighted_matrix[:, types == -1], axis=1)
        Ai = np.sum(weighted_matrix[:, types == 1], axis=1)

        ri = Li**lam + Ai**(1 - lam)

        return lin_matrix, vec_matrix, avg_matrix, weighted_matrix, Li, Ai, ri