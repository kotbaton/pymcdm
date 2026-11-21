# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestCODAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Badi, I., Shetwan, A. G., & Abdulshahed, A. M. (2017, September).
    Supplier selection using COmbinative Distance-based ASsessment (CODAS) method for multi-criteria decision-making.
    In Proceedings of The 1st International Conference on Management, Engineering and Environment (ICMNEE) (pp.
    395-407).
    """

    def test_output(self):
        body = methods.CODAS()
        matrix = np.array([[45, 3600, 45, 0.9],
                           [25, 3800, 60, 0.8],
                           [23, 3100, 35, 0.9],
                           [14, 3400, 50, 0.7],
                           [15, 3300, 40, 0.8],
                           [28, 3000, 30, 0.6]])

        types = np.array([1, -1, 1, 1])
        weights = np.array([0.2857, 0.3036, 0.2321, 0.1786])

        output = [1.3914, 0.3411, -0.2170, -0.5381, -0.7292, -0.2481]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
