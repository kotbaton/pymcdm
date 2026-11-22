# Copyright (c) 2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestPIV(unittest.TestCase):
    """ Test output method with reference:
    [1] Mufazzal, S., & Muzakkir, S. M. (2018). A new multi-criterion decision making (MCDM) method based on proximity
    indexed value for minimizing rank reversals. Computers & Industrial Engineering, 119, 427-438.

    Case study I is not used: its weighted normalized matrix (Table 5) does not follow from the decision matrix and
    weights of Table 4 with Eqs. (1)-(2), e.g. A1 on x2 gives 0.3 * 7 / sqrt(109) = 0.201 instead of 0.109, although
    Tables 6 and 7 are consistent with Table 5.
    """

    def test_case_study_2(self):
        """ Pick-and-place robot selection, overall proximity values and ranks (Table 8). """
        matrix = np.array([[60, 2.5, 2540, 500, 990],
                           [6.35, 6.667, 1016, 3000, 1041],
                           [6.8, 10, 1727, 1500, 1676],
                           [10, 5, 1000, 2000, 965],
                           [2.5, 9.8, 560, 500, 915],
                           [4.5, 12.5, 1016, 350, 508],
                           [3, 10, 1778, 1000, 920]])
        weights = np.array([0.1761, 0.2042, 0.2668, 0.1243, 0.2286])
        types = np.ones(5)
        body = methods.PIV()
        pref = body(matrix, weights, types)

        self.assertListEqual([0.22, 0.36, 0.27, 0.40, 0.46, 0.44, 0.36], np.round(pref, 2).tolist())
        self.assertListEqual([1, 4, 2, 5, 7, 6, 3], body.rank(pref).astype(int).tolist())

    def test_case_study_3(self):
        """ Industrial robot selection with 27 alternatives (Table 9). All ranks agree with the paper. The paper
            gives the overall proximity values of A1 and A21 as 0.19 and 0.29, while the data give 0.1848 and 0.2849;
            the other values agree with two decimals.
        """
        matrix = np.array([[0.15, 7.20, 60.0, 1.35], [0.05, 4.80, 6.0, 1.10], [1.27, 5.00, 45.0, 1.27],
                           [0.03, 7.20, 1.5, 0.66], [0.25, 9.60, 50.0, 0.05], [0.10, 1.07, 1.0, 0.30],
                           [0.10, 1.76, 5.0, 1.00], [0.10, 3.20, 15.0, 1.00], [0.20, 6.72, 10.0, 1.10],
                           [0.05, 2.40, 6.0, 1.00], [0.50, 2.88, 30.0, 0.90], [1.00, 6.90, 13.6, 0.15],
                           [0.05, 3.20, 10.0, 1.20], [0.05, 4.00, 30.0, 1.20], [1.00, 3.68, 47.0, 1.00],
                           [1.00, 6.88, 80.0, 1.00], [2.00, 8.00, 15.0, 2.00], [0.20, 6.30, 10.0, 1.00],
                           [0.05, 0.94, 10.0, 0.30], [2.00, 0.16, 1.5, 0.80], [2.00, 2.81, 27.0, 1.70],
                           [0.05, 3.80, 0.9, 1.00], [0.10, 1.25, 2.5, 0.50], [0.10, 1.37, 2.5, 0.50],
                           [0.20, 3.63, 10.0, 1.00], [1.27, 5.30, 70.0, 1.25], [2.03, 4.00, 205.0, 0.75]])
        weights = np.array([0.35, 0.20, 0.15, 0.30])
        types = np.array([-1, -1, 1, 1])
        body = methods.PIV()
        pref = body(matrix, weights, types)

        output = [0.18, 0.20, 0.26, 0.25, 0.29, 0.23, 0.19, 0.20, 0.23, 0.19, 0.22, 0.34, 0.18, 0.18, 0.25, 0.25,
                  0.32, 0.23, 0.22, 0.33, 0.28, 0.20, 0.22, 0.22, 0.21, 0.25, 0.25]
        self.assertListEqual(output, np.round(pref, 2).tolist())
        ranks = [3, 7, 22, 19, 24, 14, 4, 6, 15, 5, 13, 27, 2, 1, 17, 21, 25, 16, 11, 26, 23, 8, 10, 12, 9, 20, 18]
        self.assertListEqual(ranks, body.rank(pref).astype(int).tolist())

    def test_weighted_proximity_index(self):
        """ The best alternative of every criterion has a zero proximity index for that criterion (Eq. 3). """
        matrix = np.array([[1, 5, 3], [2, 4, 6], [3, 1, 2]])
        body = methods.PIV()
        _, wpi, _ = [table.data for table in body(matrix, np.ones(3) / 3, np.array([1, -1, 1]), verbose=True).results]
        self.assertListEqual([0.0, 0.0, 0.0], np.min(wpi, axis=0).tolist())
        self.assertListEqual([2, 2, 1], np.argmin(wpi, axis=0).tolist())
