# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestEDAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Yazdani, M., Torkayesh, A. E., Santibanez-Gonzalez, E. D.,
    & Otaghsara, S. K. (2020). Evaluation of renewable energy resources using integrated Shannon Entropy—EDAS model.
    Sustainable Operations and Computers, 1, 35-42.
    """

    def test_output(self):
        body = methods.EDAS()
        matrix = np.array([[3873, 39.55, 0.27, 0.87, 150, 0.07, 12, 2130],
                           [5067, 67.26, 0.23, 0.23, 40, 0.02, 21, 2200],
                           [2213, 24.69, 0.08, 0.17, 200, 0.04, 35, 570],
                           [6243, 132, 0.07, 0.25, 100, 0.04, 16, 100],
                           [8312, 460.47, 0.05, 0.21, 25, 0.1, 25, 200]])

        weights = np.array([0.131, 0.113, 0.126, 0.125, 0.126, 0.129, 0.132, 0.117])
        types = np.array([-1, -1, -1, 1, 1, -1, 1, 1])

        output = [0.841, 0.632, 0.883, 0.457, 0.104]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
