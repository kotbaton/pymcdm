# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestRAFSI(unittest.TestCase):
    """ Test output method with reference:

        Žižović, M., Pamučar, D., Albijanić, M., Chatterjee, P., & Pribićević, I. (2020). Eliminating rank reversal problem using a new multi-attribute model—the RAFSI method. Mathematics, 8(6), 1015.
    """
    def test_output(self):
        matrix = np.array([
            [180, 10.5, 15.5, 160, 3.7],
            [165, 9.2, 16.5, 131, 5.0],
            [160, 8.8, 14.0, 125, 4.5],
            [170, 9.5, 16.0, 135, 3.4],
            [185, 10.0, 14.5, 143, 4.3],
            [167, 8.9, 15.1, 140, 4.1]
        ])

        weights = np.array([0.35, 0.25, 0.15, 0.15, 0.1])
        types = np.array([1, 1, -1, -1, 1])

        ideal = np.array([200, 12, 10, 100, 8])
        anti_ideal = np.array([120, 6, 20, 200, 2])

        body = methods.RAFSI(ideal, anti_ideal)
        result = body(matrix, weights, types)
        expected = [0.5081, 0.4522, 0.4381, 0.4560, 0.5299, 0.4373]
        result_rounded = [round(x, 4) for x in result]

        self.assertListEqual(expected, result_rounded)
