# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestMIDIA(unittest.TestCase):
    """ Test output method with reference:
    [1] Roszkowska, E., & Filipowicz-Chomko, M. (2024). A multi-criteria method integrating distances to ideal and
    anti-ideal points. Symmetry, 16(8), 1025.
    """

    weights = np.ones(5) / 5
    types = np.ones(5)

    def _check(self, matrix, expected):
        for alpha, values in expected.items():
            with self.subTest(alpha=alpha):
                pref = methods.MIDIA(alpha)(matrix, self.weights, self.types)
                self.assertListEqual(values, np.round(pref, 3).tolist())

    def test_example_1(self):
        """ Example 1 (Tables 1-2): full consistency of rankings for all coefficients alpha. """
        matrix = np.array([[16, 50, 98, 20, 64], [11, 50, 97, 23, 68], [17, 29, 90, 23, 70], [8, 55, 98, 22, 54],
                           [11, 43, 91, 18, 56], [9, 58, 86, 10, 50], [18, 44, 82, 5, 49], [4, 25, 85, 14, 66],
                           [6, 35, 80, 8, 59], [3, 38, 78, 5, 58]])
        self._check(matrix, {
            0: [0.834, 0.833, 0.787, 0.747, 0.56, 0.56, 0.541, 0.449, 0.29, 0.275],
            0.5: [0.818, 0.793, 0.662, 0.641, 0.544, 0.458, 0.406, 0.356, 0.269, 0.217],
            1: [0.802, 0.752, 0.537, 0.534, 0.528, 0.355, 0.271, 0.262, 0.248, 0.159]})

    def test_example_2(self):
        """ Example 2 (Tables 5-7): partial consistency of rankings. """
        matrix = np.array([[20, 3, 91, 50, 80], [16, 50, 100, 11, 62], [11, 50, 97, 22, 68], [10, 100, 85, 10, 50],
                           [10, 55, 98, 10, 54], [12, 43, 92, 18, 56], [8, 35, 84, 6, 59], [4, 30, 89, 15, 43],
                           [2, 36, 76, 5, 53], [13, 45, 79, 4, 5]])
        self._check(matrix, {
            0: [0.812, 0.673, 0.638, 0.631, 0.575, 0.537, 0.43, 0.366, 0.353, 0.346],
            0.5: [0.644, 0.6, 0.6, 0.546, 0.523, 0.517, 0.381, 0.339, 0.275, 0.274],
            1: [0.477, 0.528, 0.563, 0.461, 0.47, 0.496, 0.331, 0.312, 0.196, 0.203]})

    def test_example_3(self):
        """ Example 3 (Tables 10-12): no consistency of rankings. """
        matrix = np.array([[20, 3, 91, 50, 80], [16, 50, 100, 11, 62], [11, 50, 97, 25, 68], [10, 100, 85, 10, 50],
                           [11, 60, 98, 10, 54], [20, 35, 84, 6, 59], [12, 43, 92, 18, 56], [2, 36, 76, 5, 53],
                           [13, 45, 79, 4, 5], [4, 20, 80, 15, 43]])
        self._check(matrix, {
            0: [0.815, 0.667, 0.651, 0.631, 0.595, 0.58, 0.537, 0.365, 0.332, 0.3],
            0.5: [0.647, 0.593, 0.617, 0.545, 0.541, 0.485, 0.516, 0.286, 0.26, 0.273],
            1: [0.479, 0.52, 0.583, 0.46, 0.487, 0.389, 0.495, 0.207, 0.188, 0.245]})
        self.assertListEqual([5, 2, 1, 6, 4, 7, 3, 9, 10, 8],
                             methods.MIDIA(1).rank(methods.MIDIA(1)(matrix, self.weights, self.types))
                             .astype(int).tolist())

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.MIDIA(alpha=1.5)
