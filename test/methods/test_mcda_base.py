# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np
import warnings

from pymcdm import methods

class TestMCDA(unittest.TestCase):

    def test_validation(self):
        # Catch warning about dominated alternatives
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            with self.assertRaises(ValueError):
                body = methods.TOPSIS()
                matrix = np.array([[1, 2, 3], [1, 2, 3]])
                weights = np.array([0.5, 0.5])
                types = np.array([1, -1, -1])

                body(matrix=matrix, weights=weights, types=types)
