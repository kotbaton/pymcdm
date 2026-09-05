# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestTODIM(unittest.TestCase):
    """ Test output method with reference:
    Dutta, V., & Haldar, S. (2025). Performance Comparison of TODIM and
    CPT-TODIM in Social Sustainability Assessment for G7 Countries.
    International Journal of Information Technology & Decision Making.
    https://doi.org/10.1142/S021962202550097X
    """

    def test_output(self):
        body = methods.TODIM()
        matrix = np.array([
            [53198.17, 64.73, 0.31, 20199.55, 0.30, 0.12, 1670,   51.7,   4, 57.88, 49.052, 12.917, 54.40, 20.89],
            [46480.62, 66.02, 0.29, 29682.22, 0.25, 0.08, 1505,   52.9, 122, 36.89, 77.838, 10.201, 54.31, 31.68],
            [53637.80, 76.09, 0.28, 43769.63, 0.25, 0.10, 1386.1, 33.3, 237, 29.06, 82.723,  8.373, 49.33, 24.76],
            [39189.37, 59.07, 0.33, 25941.40, 0.40, 0.13, 1717.8, 27.8, 205, 19.32, 61.715,  5.311, 56.07, 25.36],
            [38617.47, 77.95, 0.33, 68863.34, 0.33, 0.15, 1644,   15.8, 347, 51.92, 32.416,  4.265, 36.87, 23.51],
            [47226.09, 75.61, 0.35, 33964.07, 0.34, 0.11, 1538,   30.8, 275, 45.78, 24.991, 17.918, 54.47, 24.49],
            [65835.58, 62.56, 0.39, 163538.70, 0.38, 0.17, 1779,  16.7,  36, 47.43, 35.205,  5.18,  55.41, 30.02],
        ])
        weights = np.array([0.038095, 0.07619,  0.009524, 0.133333, 0.047619, 0.057143,
                            0.066667, 0.095238, 0.12381,  0.085714, 0.104762, 0.114286,
                            0.019048, 0.028571])
        types = np.array([1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1])

        # Expected scores from Table 8 (theta=2.5): CA, FR, DE, IT, JP, UK, USA
        # Rounded to 4dp — the paper's 6dp values differ by up to 2e-6 due to
        # rounding in intermediate steps.
        output = [0.9573, 1.0, 0.764, 0.1654, 0.0, 0.491, 0.4412]
        output_method = [round(p, 4) for p in body(matrix, weights, types)]
        self.assertListEqual(output, output_method)

    def test_gomes_rangel_2009(self):
        """ Test from the original TODIM paper (all-profit, zeros in data, theta=1).

        Reference: Gomes, L. F. A. M., & Rangel, L. A. D. (2009). An application of
        the TODIM method to the multicriteria rental evaluation of residential
        properties. European Journal of Operational Research, 193(1), 204-211.
        https://doi.org/10.1016/j.ejor.2007.10.046
        Table 8 (decision matrix), Table 7 (weights), Table 10 (results, theta=1).
        """
        matrix = np.array([
            [3, 290, 3, 3, 1, 6, 4, 0],
            [4, 180, 2, 2, 1, 4, 2, 0],
            [3, 347, 1, 2, 2, 5, 1, 0],
            [3, 124, 2, 3, 2, 5, 4, 0],
            [5, 360, 3, 4, 4, 9, 1, 1],
            [2,  89, 2, 3, 1, 5, 1, 0],
            [1,  85, 1, 1, 1, 4, 0, 1],
            [5,  80, 2, 3, 1, 6, 0, 1],
            [2, 121, 2, 3, 0, 6, 0, 0],
            [2, 120, 1, 3, 1, 5, 1, 0],
            [4, 280, 2, 2, 2, 7, 3, 1],
            [1,  90, 1, 1, 1, 5, 2, 0],
            [2, 160, 3, 3, 2, 6, 1, 1],
            [3, 320, 3, 3, 2, 8, 2, 1],
            [4, 180, 2, 4, 1, 6, 1, 1],
        ], dtype=float)
        weights = np.array([0.25, 0.15, 0.10, 0.20, 0.05, 0.10, 0.05, 0.10])
        types = np.ones(8, dtype=int)

        body = methods.TODIM(theta=1)
        output_method = [round(p, 4) for p in body(matrix, weights, types)]
        # Expected: Table 10 (Gomes & Rangel 2009), 4dp
        expected = [0.6916, 0.3862, 0.3992, 0.6210, 1.0000,
                    0.2860, 0.0000, 0.4407, 0.0202, 0.2127,
                    0.8576, 0.1073, 0.7188, 0.9372, 0.6733]
        self.assertListEqual(expected, output_method)
