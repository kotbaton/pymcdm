# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestWPM(unittest.TestCase):
    """ Test output method with reference:
    Self-reference
    """
    def test_output(self):
        body = methods.WPM()
        matrix = np.array([[96, 83, 75, 7],
                            [63, 5, 56, 9],
                            [72, 30, 32, 48],
                            [11, 4, 27, 9],
                            [77, 21, 17, 11]])
        weights = np.array([8 / 13, 5 / 13, 6 / 13, 7 / 13])
        types = np.array([1, 1, -1, -1])
        output_method = list(np.round(body(matrix, weights, types, validation=False), 3))
        output = [0.065, 0.017, 0.019, 0.007, 0.052]

        self.assertListEqual(output, output_method)
