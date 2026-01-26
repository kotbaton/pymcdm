# Copyright (c) 2020-2026 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc
from ..validators import matrix_bounds_validator


class RAFSI(MCDA_method):
    """ Ranking of Alternatives through Functional mapping
        of criterion sub-intervals into a Single Interval (RAFSI) [#rafsi1]_.

        ...

        Parameters
        ----------
        ideal : float
            Ideal value for all criteria (function as an upper/lower bound, depending on the type).

        anti_ideal : float
            Anti-ideal value for all criteria (function as a lower/upper bound, depending on the type).

        n1 : float
            Parameter n1 for RAFSI calculations. Default is 1.

        n2k : float
            Parameter n2k for RAFSI calculations.
            Indicates how much ideal solution is better than anti-ideal. Default is 6.

        References
        ----------
        .. [#rafsi1] Žižović, M., Pamučar, D., Albijanić, M., Chatterjee, P., & Pribićević, I. (2020). Eliminating rank reversal problem using a new multi-attribute model—the RAFSI method. Mathematics, 8(6), 1015.
        """
    _reverse_ranking = True
    _tables = [
        TableDesc(caption='Standarized decision matrix',
                  label='smatrix', symbol='$s_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Normalized decision matrix',
                  label='snmatrix', symbol='$\\hat{s}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$V(A_i)$', rows='A', cols=None)
    ]

    def __init__(self, ideal, anti_ideal, n1=1, n2k=6):
        # For validation purposes and order ensuring
        self.bounds = np.array([anti_ideal, ideal]).T
        self.bounds.sort(axis=1)
        anti_ideal, ideal = self.bounds.T

        # Parameters for RAFSI calculations
        self.ideal = ideal
        self.anti_ideal = anti_ideal

        self.n1 = n1
        self.n2k = n2k
        if n1 <= 0 or n2k <= 0 or n1 >= n2k:
            raise ValueError("n1 and n2k should be positive numbers and n1 should be smaller than n2k.")

        self.a_value = (n1 + n2k) / 2
        self.h_value = 2 / (1 / n1 + 1 / n2k)
        self.first = (n2k - n1) / (ideal - anti_ideal)
        self.second = (n1 * ideal - n2k * anti_ideal) / (ideal - anti_ideal)

    def _method(self, matrix, weights, types):
        smatrix = (self.first * matrix + self.second)

        snmatrix = np.empty_like(matrix, dtype='float')
        for j in range(matrix.shape[1]):
            if types[j] == 1:
                snmatrix[:, j] = smatrix[:, j] / (2 * self.a_value)
            else:
                snmatrix[:, j] = self.h_value / (2 * smatrix[:, j])

        vai = np.sum(snmatrix * weights, axis=1)
        return smatrix, snmatrix, vai

    def _additional_validation(self, matrix, weights, types):
        matrix_bounds_validator(matrix, self.bounds)


