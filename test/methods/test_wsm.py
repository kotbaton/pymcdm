# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestWSM(unittest.TestCase):
    """ Test output method with reference:
    Self-reference
    """
    def test_output(self):
        body = methods.WSM()
        matrix = np.array([[96, 83, 75, 7],
                            [63, 5, 56, 9],
                            [72, 30, 32, 48],
                            [11, 4, 27, 9],
                            [77, 21, 17, 11]])
        weights = np.array([8 / 13, 5 / 13, 6 / 13, 7 / 13])
        types = np.array([1, 1, -1, -1])
        output_method = list(np.round(body(matrix, weights, types, validation=False), 3))
        output = [0.609, 0.313, 0.334, 0.265, 0.479]

        self.assertListEqual(output, output_method)
