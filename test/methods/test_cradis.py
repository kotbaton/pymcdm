# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestCRADIS(unittest.TestCase):
    """ Test output method with reference:
    [1] Puška, A., Stević, Ž., & Pamučar, D. (2022). Evaluation and selection of healthcare waste incinerators using
    extended sustainability criteria and multi-criteria analysis methods. Environment, Development and
    Sustainability, 24(9), 11195-11225.
    """

    # Table 9: assessments of the sustainability sub-criteria (C11-C34) by three experts
    experts = np.array([
        [[3, 2, 3, 3, 5, 3, 3, 4, 4, 5, 3, 1],
         [3, 2, 3, 3, 4, 3, 3, 4, 4, 6, 3, 1],
         [4, 3, 3, 3, 5, 4, 4, 5, 3, 6, 4, 1],
         [3, 2, 3, 4, 4, 3, 3, 4, 4, 6, 4, 2],
         [5, 3, 4, 4, 5, 4, 4, 4, 2, 5, 5, 2],
         [4, 3, 4, 4, 5, 4, 4, 5, 2, 6, 5, 2]],
        [[1, 2, 2, 3, 4, 4, 2, 3, 4, 5, 2, 1],
         [1, 2, 2, 3, 4, 4, 2, 3, 4, 6, 2, 1],
         [2, 3, 3, 3, 5, 5, 2, 3, 3, 6, 3, 1],
         [1, 2, 2, 4, 4, 4, 2, 3, 4, 6, 3, 2],
         [2, 3, 3, 4, 5, 6, 3, 4, 2, 5, 3, 3],
         [2, 2, 3, 4, 5, 5, 3, 4, 3, 6, 4, 2]],
        [[2, 1, 3, 2, 4, 3, 2, 3, 5, 6, 2, 2],
         [2, 1, 3, 2, 3, 3, 2, 3, 5, 6, 2, 2],
         [3, 2, 4, 3, 4, 3, 2, 4, 4, 6, 3, 3],
         [2, 1, 3, 2, 3, 3, 2, 3, 5, 6, 3, 2],
         [3, 3, 5, 4, 5, 4, 3, 4, 3, 5, 4, 4],
         [3, 2, 4, 3, 5, 4, 3, 4, 4, 6, 4, 3]],
    ])
    # Table 9: technical characteristics (C41-C44)
    technical = np.array([[0.36, 30, 10.0, 5.02],
                          [0.54, 40, 11.5, 6.26],
                          [0.75, 50, 12.5, 8.97],
                          [0.57, 65, 17.5, 8.79],
                          [1.35, 100, 16.5, 11.68],
                          [1.20, 100, 15.5, 12.90]])
    # Table 8: initial decision matrix, the geometric mean of the experts' assessments
    matrix = np.hstack([np.prod(experts, axis=0) ** (1 / 3), technical])
    types = np.array([-1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1])
    # Table 3 (weights of the sub-criteria) and Table 6 (harmonized weights of the main criteria)
    weights = (np.array([0.30, 0.22, 0.21, 0.27, 0.32, 0.22, 0.22, 0.23,
                         0.24, 0.32, 0.22, 0.23, 0.32, 0.22, 0.23, 0.23])
               * np.repeat([0.2337, 0.2735, 0.2085, 0.2843], 4))

    def test_normalized_matrix(self):
        """ Table 10. """
        body = methods.CRADIS()
        nmatrix = body(self.matrix, self.weights, self.types, verbose=True).results[0].data
        self.assertListEqual(
            [[1.0, 1.0, 1.0, 1.0, 0.84, 1.0, 1.0, 1.0, 1.0, 0.89, 1.0, 1.0, 0.27, 0.3, 1.0, 1.0],
             [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.4, 0.4, 0.87, 0.8],
             [0.63, 0.61, 0.79, 0.87, 0.78, 0.84, 0.91, 0.84, 0.77, 1.0, 0.69, 0.87, 0.56, 0.5, 0.8, 0.56],
             [1.0, 1.0, 1.0, 0.83, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.69, 0.63, 0.42, 0.65, 0.57, 0.57],
             [0.58, 0.53, 0.67, 0.66, 0.73, 0.72, 0.69, 0.83, 0.53, 0.83, 0.58, 0.44, 1.0, 1.0, 0.61, 0.43],
             [0.63, 0.69, 0.72, 0.72, 0.73, 0.77, 0.69, 0.77, 0.67, 1.0, 0.53, 0.55, 0.89, 1.0, 0.65, 0.39]],
            np.round(nmatrix, 2).tolist())

    def test_output(self):
        """ Table 12. The paper gives only rounded weights of the sub-criteria, so the ideal solution is 0.0910
            instead of 0.0907 and K+ of A1 differs at the second decimal place (0.7758 instead of 0.7742). K- and the
            final scores are compared with two decimal places.
        """
        body = methods.CRADIS()
        *_, k_minus, pref = [table.data for table in
                             body(self.matrix, self.weights, self.types, verbose=True).results]

        self.assertListEqual([0.81, 0.84, 0.64, 0.75, 0.56, 0.6], np.round(k_minus, 2).tolist())
        self.assertListEqual([0.79, 0.82, 0.64, 0.74, 0.58, 0.61], np.round(pref, 2).tolist())
        self.assertListEqual([2, 1, 4, 3, 6, 5], body.rank(pref).astype(int).tolist())

    def test_dynamic_decision_matrix(self):
        """ Fig. 1: removing the worst alternative one by one (A5, A6, A3, A4) does not change the order of the
            remaining alternatives.
        """
        body = methods.CRADIS()
        alternatives = [0, 1, 2, 3, 4, 5]
        for removed, expected in ((4, [2, 1, 4, 3, 5]), (5, [2, 1, 4, 3]), (2, [2, 1, 3]), (3, [2, 1])):
            alternatives.remove(removed)
            with self.subTest(removed=f'A{removed + 1}'):
                pref = body(self.matrix[alternatives], self.weights, self.types)
                self.assertListEqual(expected, body.rank(pref).astype(int).tolist())

    def test_equal_weights(self):
        """ With equal weights the optimal alternative reaches the ideal solution on every criterion (Eq. 11): K+ is
            0 for every alternative and 1 for an alternative equal to the ideal solution, instead of 0 / 0.
        """
        matrix = np.array([[9, 1, 8], [5, 4, 6], [3, 6, 2], [7, 3, 5]], dtype=float)
        types = np.array([1, -1, 1])
        body = methods.CRADIS()
        results = body(matrix, np.ones(3) / 3, types, verbose=True)
        k_plus, pref = results.results[4].data, results.results[-1].data

        self.assertListEqual([1.0, 0.0, 0.0, 0.0], k_plus.tolist())
        self.assertTrue(np.all(np.isfinite(pref)))
        self.assertListEqual([1.0, 3.0, 4.0, 2.0], body.rank(pref).tolist())
