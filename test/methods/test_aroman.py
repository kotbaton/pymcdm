# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestAROMAN(unittest.TestCase):
    """ Test AROMAN method.

    Reference:
    Bošković, S., Švadlenka, L., Jovčić, S., Dobrodolac, M., Simić, V., & Bacanin, N. (2023). An alternative
    ranking order method accounting for two-step normalization (AROMAN)—A case study of the electric vehicle
    selection problem. IEEE access, 11, 39496-39507.
    """

    def test_output(self):
        matrix = np.array([
            [40000, 1.200, 1.4, 8, 9],
            [38500, 1.150, 1.2, 6, 6],
            [39400, 0.600, 1.1, 7, 5],
            [48000, 1.300, 1.6, 10, 12]
        ])

        weights = np.array([0.28, 0.22, 0.26, 0.15, 0.09])

        types = np.array([-1, 1, 1, 1, 1])
        aroman = methods.AROMAN()
        output_method = list(np.round(aroman(matrix, weights, types), 4))
        expected = [0.6727, 0.5535, 0.4721, 0.8718]
        self.assertListEqual(expected, output_method)
