# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestVIKOR(unittest.TestCase):
    """ Test output method with reference:
    [1] Yang, W., & Wu, Y. (2020). A new improvement method to avoid rank reversal in VIKOR.
    IEEE Access, 8, 21261-21271.
    [2] Opricovic, S., & Tzeng, G. H. (2004). Compromise solution by MCDM methods: A comparative analysis of VIKOR and
    TOPSIS. European journal of operational research, 156(2), 445-455.
    """

    def test_output_yang(self):
        body = methods.VIKOR()

        matrix = np.array([[78, 56, 34, 6],
                           [4, 45, 3, 97],
                           [18, 2, 50, 63],
                           [9, 14, 11, 92],
                           [85, 9, 100, 29]])

        types = np.array([1, 1, 1, 1])

        weights = np.array([0.25, 0.25, 0.25, 0.25])

        output = [0.5679, 0.7667, 1, 0.7493, 0]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)

    def test_output_opricovic(self):

        body = methods.VIKOR()

        matrix = np.array([[1, 2, 5],
                           [3000, 3750, 4500]]).T

        weights = np.array([0.5, 0.5])

        types = np.array([-1, 1])

        output = [1, 0, 1]
        output_method = list(body(matrix, weights, types))

        self.assertListEqual(output, output_method)
