# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestLMAW(unittest.TestCase):
    """ Test LMAW method.

    Reference:
    Pamučar, D., Žižović, M., Biswas, S., & Božanić, D. (2021). A new logarithm
    methodology of additive weights (LMAW) for multi-criteria decision-making:
    Application in logistics. Facta universitatis, series: mechanical engineering,
    19(3), 361-380.
    """

    def test_output(self):
        matrix = np.array([
            [647.34, 6.24, 49.87, 19.46, 212.58, 6.75],
            [115.64, 3.24, 16.26, 9.69, 207.59, 3.00],
            [373.61, 5.00, 26.43, 12.00, 184.62, 3.74],
            [37.63, 2.48, 2.85, 9.35, 142.50, 3.24],
            [858.01, 4.74, 62.85, 45.96, 267.95, 4.00],
            [222.92, 3.00, 19.24, 21.46, 221.38, 3.49]
        ], dtype=float)

        weights = np.array([0.215, 0.126, 0.152, 0.09, 0.19, 0.226])

        types = np.array([1, 1, -1, -1, -1, 1])

        lmaw = methods.LMAW()
        output_method = list(np.round(lmaw(matrix, weights, types), 3))
        expected = [4.840, 4.681, 4.799, 4.733, 4.736, 4.704]
        self.assertListEqual(expected, output_method)

    def test_matrix_aggregation(self):
        matrices = np.array([np.array([[val]]) for val in (3, 4, 4, 3)])
        expected_matrix = np.array([[3.49]])
        lmaw = methods.LMAW()
        aggregated_matrix = lmaw.aggregate_matrices(matrices)
        aggregated_matrix_rounded = np.round(aggregated_matrix, 2)
        self.assertTrue(np.array_equal(expected_matrix, aggregated_matrix_rounded))

    def test_weights_aggregation(self):
        weight_vectors = [
            np.array([4, 2, 2.5, 1.5, 3.5, 5]),
            np.array([4.5, 1.5, 2.5, 1, 3, 4.5]),
            np.array([4, 2, 2, 1.5, 3, 5]),
            np.array([4, 1.5, 2, 1, 3.5, 4])
        ]

        expected_weights = np.array([0.215, 0.126, 0.152, 0.09, 0.19, 0.226])

        lmaw = methods.LMAW()
        aggregated_weights = lmaw.aggregate_weights(weight_vectors)
        aggregated_weights_rounded = np.round(aggregated_weights, 3)
        self.assertTrue(np.array_equal(expected_weights, aggregated_weights_rounded))
