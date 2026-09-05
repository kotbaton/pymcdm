# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestLoPM(unittest.TestCase):
    """ Test output method with reference:
    [1] Farag, M. M. (2020). Materials and process selection for engineering design. CRC press.

    Output was slightly modified due to rounding errors.
    """
    def test_output(self):
        matrix = np.array([
            [14_820, 18, 0.0002, 2.1,  9.5, 4.5],
            [21_450, 18, 0.0012, 2.7, 14.4, 9.0],
            [78_000, 16, 0.0006, 2.6,  9.0, 8.5],
            [20_475, 17, 0.0006, 2.6,  6.5, 2.6],
            [16_575, 14, 0.0010, 3.1,  5.6, 3.5],
            [21_450, 16, 0.0005, 2.2,  8.6, 1.0]
        ])
        weights = np.array([0.20, 0.33, 0.13, 0.07, 0.07, 0.20])
        lopm = methods.LoPM([10_000, 14, 0.0015, 3.5, 2.3, 9.0], [1, 1, -1, -1, 0, -1])
        output_method = list(np.round(lopm(matrix, weights, None), 2))
        output = [0.77, 1.08, 0.81, 0.66, 0.78, 0.68]
        self.assertListEqual(output, output_method)
