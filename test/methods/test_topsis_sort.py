# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import warnings

import numpy as np

from pymcdm.methods.sorting import TOPSIS_SORT


class TestTOPSIS_SORT(unittest.TestCase):
    """ Test output method with reference:
    [1] de Lima Silva, D. F., & de Almeida Filho, A. T. (2020). Sorting with TOPSIS through boundary and
    characteristic profiles. Computers & Industrial Engineering, 141, 106328.

    Economic freedom of 10 countries (Table 6): 12 equally weighted benefit criteria with domain [0, 100]. The paper
    numbers the categories from C1 (Free, the best) to C5 (Repressed); pymcdm numbers them from 1 (the worst), so
    category c of the paper is 6 - c in pymcdm, and the profiles are given from the worst to the best.
    """

    matrix = np.array([
        [19.6, 29.6, 25.2, 91.7, 80.3, 99.3, 49.2, 60.4, 76.7, 66.0, 10, 10],
        [54.8, 30.6, 40.4, 86.3, 73.9, 80.6, 69.3, 52.7, 81.5, 87.8, 70, 70],
        [31.6, 36.2, 28.9, 76.4, 48.7, 18.7, 61.6, 49.9, 74.9, 67.4, 30, 30],
        [35.9, 26.6, 20.5, 83.9, 80.7, 58.2, 55.7, 58.8, 55.4, 61.2, 30, 40],
        [47.8, 44.5, 33.5, 69.3, 49.5, 33.0, 56.4, 46.9, 60.2, 70.0, 55, 60],
        [57.2, 46.3, 38.6, 84.7, 79.0, 53.0, 78.3, 71.4, 77.8, 80.8, 75, 70],
        [79.1, 86.5, 79.9, 62.8, 60.1, 86.2, 88.3, 84.1, 86.6, 87.6, 80, 90],
        [84.2, 71.3, 77.4, 50.5, 24.5, 85.5, 74.9, 68.7, 81.5, 86.0, 90, 70],
        [59.1, 53.1, 44.7, 87.5, 59.5, 89.4, 69.5, 63.9, 63.0, 74.6, 60, 60],
        [42.2, 46.9, 43.7, 97.3, 86.8, 65.7, 68.5, 67.5, 78.1, 47.8, 50, 60],
    ])
    weights = np.ones(12) / 12
    types = np.ones(12)
    bounds = np.array([[0, 100]] * 12)

    def test_closeness_coefficients(self):
        """ Closeness coefficients of the alternatives from Table 8, for both normalizations. """
        output = [0.5109, 0.6453, 0.4667, 0.505, 0.5207, 0.6615, 0.7932, 0.6918, 0.6437, 0.6145]
        profiles = np.repeat([[50], [60], [70], [80]], 12, axis=1)
        for normalization in ('max', 'minmax'):
            with self.subTest(normalization=normalization):
                body = TOPSIS_SORT(profiles, self.bounds, normalization=normalization)
                results = body(self.matrix, self.weights, self.types, verbose=True)
                self.assertListEqual(output, np.round(results.results[0].data, 4).tolist())

    def test_output_boundary(self):
        """ Scenario #1, TOPSIS-Sort-B with boundary profiles 50, 60, 70 and 80 (Tables 4, 6 and 8). """
        profiles = np.repeat([[50], [60], [70], [80]], 12, axis=1)
        body = TOPSIS_SORT(profiles, self.bounds)
        results = body(self.matrix, self.weights, self.types, verbose=True)

        self.assertListEqual([0.5, 0.6, 0.7, 0.8], np.round(results.results[1].data, 4).tolist())
        output = [4, 3, 5, 4, 4, 3, 2, 3, 3, 3]
        self.assertListEqual(output, (6 - body(self.matrix, self.weights, self.types)).tolist())

    def test_output_characteristic_medians(self):
        """ Scenario #2, TOPSIS-Sort-C with the medians of the intervals as characteristic profiles. Table 8 gives
            Cl(P2) = 0.7, but its distances (0.0722 and 0.2165) give 0.75, as the profile value 75 implies.
        """
        profiles = np.repeat([[25], [55], [65], [75], [90]], 12, axis=1)
        body = TOPSIS_SORT(profiles, self.bounds, profiles_type='characteristic')
        results = body(self.matrix, self.weights, self.types, verbose=True)

        self.assertListEqual([0.25, 0.55, 0.65, 0.75, 0.9], np.round(results.results[1].data, 4).tolist())
        output = [4, 3, 4, 4, 4, 3, 2, 3, 3, 3]
        self.assertListEqual(output, (6 - body(self.matrix, self.weights, self.types)).tolist())

    def test_output_characteristic_averages(self):
        """ Scenario #3, TOPSIS-Sort-C with the average scores of the original allocations (Table 6). """
        profiles = np.array([
            [30.07, 23.68, 24.95, 71.05, 55.38, 34.46, 41.05, 44.03, 64.46, 59.60, 32.27, 25.91],
            [41.70, 38.11, 31.46, 72.82, 56.61, 57.77, 58.51, 58.02, 72.60, 69.26, 45.31, 37.34],
            [57.45, 46.40, 42.19, 77.35, 63.57, 75.91, 68.36, 61.18, 78.70, 78.73, 68.14, 55.76],
            [78.98, 69.33, 69.46, 78.98, 71.52, 88.28, 80.11, 66.72, 80.81, 85.01, 77.76, 68.97],
            [89.32, 81.35, 86.92, 79.74, 72.28, 91.68, 87.50, 83.13, 86.33, 90.53, 85.00, 83.33],
        ])
        body = TOPSIS_SORT(profiles, self.bounds, profiles_type='characteristic')
        results = body(self.matrix, self.weights, self.types, verbose=True)

        self.assertListEqual([0.4297, 0.5306, 0.6364, 0.757, 0.8408], np.round(results.results[1].data, 4).tolist())
        output = [4, 3, 5, 4, 4, 3, 2, 3, 3, 3]
        self.assertListEqual(output, (6 - body(self.matrix, self.weights, self.types)).tolist())

    def test_independence_of_alternatives(self):
        """ Irreversibility (Property 4): the category does not depend on the other alternatives. """
        body = TOPSIS_SORT(np.repeat([[50], [60], [70], [80]], 12, axis=1), self.bounds)
        categories = body(self.matrix, self.weights, self.types)
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            for i in range(len(self.matrix)):
                self.assertEqual(categories[i], body(self.matrix[i:i + 1], self.weights, self.types)[0])

    def test_cost_criteria(self):
        """ Cost criteria are handled by the fixed ideal solutions; reversing a criterion and its profiles gives
            the same categories.
        """
        profiles = np.repeat([[50], [60], [70], [80]], 12, axis=1)
        reversed_types = self.types.copy()
        reversed_types[0] = -1
        matrix, reversed_profiles = self.matrix.copy(), profiles.astype(float)
        matrix[:, 0] = 100 - matrix[:, 0]
        reversed_profiles[:, 0] = 100 - reversed_profiles[:, 0]

        self.assertListEqual(TOPSIS_SORT(profiles, self.bounds)(self.matrix, self.weights, self.types).tolist(),
                             TOPSIS_SORT(reversed_profiles, self.bounds)(matrix, self.weights,
                                                                         reversed_types).tolist())

    def test_validation(self):
        profiles = np.repeat([[50], [60]], 12, axis=1)
        with self.assertRaises(ValueError):
            TOPSIS_SORT(profiles, self.bounds, profiles_type='central')
        with self.assertRaises(ValueError):
            TOPSIS_SORT(profiles[:, :3], self.bounds)
        with self.assertRaises(ValueError):
            TOPSIS_SORT(profiles[::-1], self.bounds)(self.matrix, self.weights, self.types)
        with self.assertRaises(ValueError):
            TOPSIS_SORT(profiles + 60, self.bounds)(self.matrix, self.weights, self.types)
        with self.assertRaises(NotImplementedError):
            TOPSIS_SORT(profiles, self.bounds).rank(np.array([1, 2]))
