# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestPROMETHEE_II(unittest.TestCase):
    """ Test output method with reference:
    [1] Zhao, H., Peng, Y., & Li, W. (2013). Revised PROMETHEE II for improving efficiency in emergency response.
    Procedia Computer Science, 17, 181-188.
    """

    def test_output(self):
        body = methods.PROMETHEE_II('usual')
        matrix = np.array([[4, 3, 2],
                           [3, 2, 4],
                           [5, 1, 3]])

        weights = np.array([0.5, 0.3, 0.2])
        types = np.ones(3)

        output = [0.1, -0.3, 0.2]
        output_method = [round(preference, 2) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)

    def test_repeated_call_with_thresholds(self):
        matrix = np.array([[4, 3, 2],
                           [3, 2, 4],
                           [5, 1, 3]])
        weights = np.array([0.5, 0.3, 0.2])
        types = np.ones(3)

        bodies = [
            methods.PROMETHEE_II('vshape', p=[1, 1, 1]),
            methods.PROMETHEE_II('ushape', q=[1, 1, 1]),
            methods.PROMETHEE_II('vshape_2', p=[2, 2, 2], q=[1, 1, 1]),
        ]
        for body in bodies:
            first = body(matrix, weights, types)
            second = body(matrix, weights, types)
            np.testing.assert_array_equal(first, second)

    def test_thresholds_length(self):
        matrix = np.array([[4, 3, 2],
                           [3, 2, 4],
                           [5, 1, 3]])
        weights = np.array([0.5, 0.3, 0.2])
        types = np.ones(3)

        with self.assertRaises(ValueError):
            methods.PROMETHEE_II('vshape', p=[1, 1])(matrix, weights, types)
        with self.assertRaises(ValueError):
            methods.PROMETHEE_II('vshape_2', p=[2, 2, 2], q=[1, 1])
