# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestRIM(unittest.TestCase):
    """ Test output method with reference:
    [1] Cables, E., Lamata, M. T., & Verdegay, J. L. (2016). RIM-reference ideal method in multicriteria decision
    making. Information Sciences, 337, 1-10.

    Note: The paper [1] which introduces the method has an error in the final results. The authors of the method confirm
    that result should be as the one we have obtained.
    """
    def test_output(self):
        matrix = np.array([
            [30,  0, 2, 3, 3, 2],
            [40,  9, 1, 3, 2, 2],
            [25,  0, 3, 1, 3, 2],
            [27,  0, 5, 3, 3, 1],
            [45, 15, 2, 2, 3, 4]
        ])

        weights = np.array([0.2262, 0.2143, 0.1786, 0.1429, 0.1190, 0.1190])

        range_t = np.array([
            [23, 60],
            [0, 15],
            [0, 10],
            [1, 3],
            [1, 3],
            [1, 5]
        ])

        ref_s = [
            [30, 35],
            [10, 15],
            [0, 0],
            [3, 3],
            [3, 3],
            [4, 5]
        ]

        pr = methods.RIM(range_t, ref_s)
        output_method = pr(matrix, weights, None, validation=False)

        output_method = list(np.round(output_method, 5))
        output = [0.58663, 0.75584, 0.37163, 0.46658, 0.74015]

        self.assertListEqual(output, output_method)
