# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods
from pymcdm.normalizations import vector_normalization, minmax_normalization, sum_normalization


class TestHELLWIG(unittest.TestCase):
    """ Test output method with reference:
    [1] Roszkowska, E. (2024). Modifying Hellwig's method for multi-criteria decision-making with Mahalanobis
    distance for addressing asymmetrical relationships. Symmetry, 16(1), 77.
    """

    weights = np.ones(4) / 4
    types = np.ones(4)

    def _variants(self, matrix):
        """ H1, H2, H3 (Euclidean distance with the vector, max-min and sum normalization) and HM (Mahalanobis). """
        bodies = [methods.HELLWIG(vector_normalization), methods.HELLWIG(minmax_normalization),
                  methods.HELLWIG(sum_normalization), methods.HELLWIG(distance='mahalanobis')]
        return [body(matrix, self.weights, self.types, verbose=True).results for body in bodies]

    def _check(self, matrix, distances, measures):
        for k, results in enumerate(self._variants(matrix)):
            with self.subTest(variant=['H1', 'H2', 'H3', 'HM'][k]):
                self.assertListEqual(distances[k], np.round(results[2].data, 3).tolist())
                self.assertListEqual(measures[k], np.round(results[3].data, 3).tolist())

    def test_example_1(self):
        """ Example 1 (Tables 1-2): negligible or weak correlation between criteria. """
        matrix = np.array([[1, 18, 7, 6], [3, 2, 10, 10], [5, 30, 15, 30], [3, 1, 15, 20], [8, 10, 20, 8],
                           [2, 20, 10, 5], [10, 4, 6, 25], [12, 25, 10, 2], [5, 5, 15, 8], [6, 2, 5, 9]])
        self._check(matrix,
                    [[0.211, 0.218, 0.092, 0.194, 0.161, 0.197, 0.165, 0.162, 0.195, 0.217],
                     [0.408, 0.4, 0.18, 0.345, 0.277, 0.37, 0.33, 0.304, 0.342, 0.418],
                     [0.08, 0.086, 0.034, 0.078, 0.064, 0.075, 0.065, 0.062, 0.077, 0.085],
                     [2.333, 2.177, 1.123, 1.872, 1.584, 2.116, 1.819, 1.741, 1.88, 2.277]],
                    [[0.168, 0.141, 0.639, 0.235, 0.366, 0.225, 0.352, 0.363, 0.234, 0.144],
                     [0.139, 0.155, 0.62, 0.27, 0.415, 0.219, 0.303, 0.358, 0.276, 0.117],
                     [0.202, 0.14, 0.663, 0.222, 0.355, 0.252, 0.349, 0.38, 0.226, 0.148],
                     [0.096, 0.157, 0.565, 0.275, 0.387, 0.18, 0.296, 0.326, 0.272, 0.118]])

    def test_example_2(self):
        """ Example 2 (Tables 3-4): from weak to very strong correlation between criteria. The ideal solution in
            Table 3 is [12, 20, 20, 25], but the results in Table 4 follow from the data, i.e. [12, 24, 20, 33].
        """
        matrix = np.array([[1, 4, 3, 5], [4, 10, 12, 10], [5, 20, 13, 33], [3, 12, 9, 20], [2, 2, 2, 8],
                           [2, 8, 6, 5], [10, 16, 16, 25], [12, 20, 20, 2], [3, 12, 9, 10], [6, 24, 18, 9]])
        self._check(matrix,
                    [[0.255, 0.182, 0.106, 0.168, 0.248, 0.231, 0.07, 0.156, 0.192, 0.145],
                     [0.47, 0.324, 0.192, 0.308, 0.466, 0.417, 0.133, 0.254, 0.344, 0.238],
                     [0.097, 0.07, 0.041, 0.064, 0.093, 0.088, 0.026, 0.062, 0.074, 0.057],
                     [1.959, 2.364, 1.141, 1.51, 1.8, 1.891, 0.855, 1.594, 1.712, 1.972]],
                    [[0.117, 0.37, 0.632, 0.42, 0.143, 0.201, 0.758, 0.459, 0.334, 0.499],
                     [0.113, 0.388, 0.638, 0.419, 0.121, 0.214, 0.75, 0.521, 0.351, 0.55],
                     [0.119, 0.365, 0.63, 0.421, 0.151, 0.198, 0.762, 0.441, 0.329, 0.483],
                     [0.218, 0.056, 0.544, 0.397, 0.281, 0.245, 0.659, 0.363, 0.316, 0.212]])

    def test_example_3(self):
        """ Example 3 (Tables 5-6): from negligible to very strong correlation between criteria. """
        matrix = np.array([[1, 2, 2, 5], [4, 6, 10, 10], [5, 23, 24, 33], [3, 1, 6, 10], [2, 10, 4, 8],
                           [4, 7, 8, 6], [10, 6, 12, 15], [12, 20, 8, 6], [3, 6, 7, 10], [6, 8, 10, 6]])
        self._check(matrix,
                    [[0.31, 0.233, 0.092, 0.272, 0.263, 0.251, 0.185, 0.199, 0.25, 0.231],
                     [0.494, 0.371, 0.159, 0.434, 0.418, 0.397, 0.289, 0.304, 0.398, 0.362],
                     [0.12, 0.09, 0.035, 0.105, 0.101, 0.097, 0.072, 0.076, 0.096, 0.089],
                     [2.223, 2.001, 1.36, 1.848, 2.146, 2.239, 1.32, 1.9, 1.857, 2.282]],
                    [[0.092, 0.318, 0.73, 0.204, 0.231, 0.266, 0.46, 0.419, 0.269, 0.325],
                     [0.084, 0.312, 0.705, 0.196, 0.225, 0.265, 0.464, 0.437, 0.262, 0.329],
                     [0.095, 0.316, 0.735, 0.203, 0.237, 0.266, 0.455, 0.421, 0.271, 0.323],
                     [0.135, 0.221, 0.471, 0.281, 0.165, 0.129, 0.486, 0.261, 0.278, 0.112]])

    def test_example_4(self):
        """ Example 4 (Tables 7-8): strong or very strong correlation between criteria; A8 is the ideal solution and
            A6 and A9 are identical.
        """
        matrix = np.array([[2, 4, 3, 6], [5, 10, 9, 10], [7, 8, 9, 9], [3, 6, 5, 10], [6, 10, 10, 13],
                           [3, 6, 4, 6], [6, 12, 6, 14], [8, 12, 10, 16], [3, 6, 4, 6], [6, 5, 3, 7]])
        self._check(matrix,
                    [[0.162, 0.068, 0.068, 0.119, 0.042, 0.14, 0.057, 0.0, 0.14, 0.129],
                     [0.5, 0.208, 0.222, 0.365, 0.128, 0.432, 0.173, 0.0, 0.432, 0.41],
                     [0.055, 0.023, 0.023, 0.041, 0.014, 0.047, 0.02, 0.0, 0.047, 0.044],
                     [1.552, 1.446, 1.324, 1.326, 0.81, 1.573, 1.312, 0.0, 1.573, 1.544]],
                    [[0.157, 0.645, 0.644, 0.378, 0.78, 0.273, 0.703, 1.0, 0.273, 0.331],
                     [0.162, 0.651, 0.628, 0.389, 0.785, 0.275, 0.71, 1.0, 0.275, 0.313],
                     [0.157, 0.647, 0.648, 0.378, 0.781, 0.273, 0.7, 1.0, 0.273, 0.33],
                     [0.289, 0.338, 0.394, 0.392, 0.629, 0.28, 0.399, 1.0, 0.28, 0.293]])

    def test_mahalanobis_normalization_invariance(self):
        """ Property 2: the Mahalanobis distance-based measure does not depend on the normalization. """
        matrix = np.array([[1, 18, 7, 6], [3, 2, 10, 10], [5, 30, 15, 30], [3, 1, 15, 20], [8, 10, 20, 8],
                           [2, 20, 10, 5], [10, 4, 6, 25], [12, 25, 10, 2], [5, 5, 15, 8], [6, 2, 5, 9]])
        reference = methods.HELLWIG(distance='mahalanobis')(matrix, self.weights, self.types)
        for normalization in (vector_normalization, minmax_normalization, sum_normalization):
            np.testing.assert_allclose(reference, methods.HELLWIG(normalization, distance='mahalanobis')(
                matrix, self.weights, self.types))
        np.testing.assert_allclose(reference, methods.HELLWIG(distance='mahalanobis')(
            matrix * [2, 3, 0.5, 10] + [1, -4, 7, 0], self.weights, self.types))

    def test_cost_criteria(self):
        """ The pattern of a cost criterion is its smallest value. """
        matrix = np.array([[1, 18, 7, 6], [3, 2, 10, 10], [5, 30, 15, 30], [3, 1, 15, 20], [8, 10, 20, 8],
                           [2, 20, 10, 5], [10, 4, 6, 25], [12, 25, 10, 2], [5, 5, 15, 8], [6, 2, 5, 9]])
        mirrored = matrix.copy()
        mirrored[:, 0] = -matrix[:, 0]
        types = np.array([-1, 1, 1, 1])
        for distance in ('euclidean', 'mahalanobis'):
            np.testing.assert_allclose(methods.HELLWIG(distance=distance)(matrix, self.weights, self.types),
                                       methods.HELLWIG(distance=distance)(mirrored, self.weights, types))

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.HELLWIG(distance='manhattan')
        with self.assertRaises(ValueError):
            methods.HELLWIG(distance='mahalanobis')(np.array([[1, 2, 3, 4], [4, 3, 2, 1]]), self.weights,
                                                    self.types)


class TestMIDIA(unittest.TestCase):
    """ Test output method with reference:
    [1] Roszkowska, E., & Filipowicz-Chomko, M. (2024). A multi-criteria method integrating distances to ideal and
    anti-ideal points. Symmetry, 16(8), 1025.
    """

    weights = np.ones(5) / 5
    types = np.ones(5)

    def _check(self, matrix, expected):
        for alpha, values in expected.items():
            with self.subTest(alpha=alpha):
                pref = methods.MIDIA(alpha)(matrix, self.weights, self.types)
                self.assertListEqual(values, np.round(pref, 3).tolist())

    def test_example_1(self):
        """ Example 1 (Tables 1-2): full consistency of rankings for all coefficients alpha. """
        matrix = np.array([[16, 50, 98, 20, 64], [11, 50, 97, 23, 68], [17, 29, 90, 23, 70], [8, 55, 98, 22, 54],
                           [11, 43, 91, 18, 56], [9, 58, 86, 10, 50], [18, 44, 82, 5, 49], [4, 25, 85, 14, 66],
                           [6, 35, 80, 8, 59], [3, 38, 78, 5, 58]])
        self._check(matrix, {
            0: [0.834, 0.833, 0.787, 0.747, 0.56, 0.56, 0.541, 0.449, 0.29, 0.275],
            0.5: [0.818, 0.793, 0.662, 0.641, 0.544, 0.458, 0.406, 0.356, 0.269, 0.217],
            1: [0.802, 0.752, 0.537, 0.534, 0.528, 0.355, 0.271, 0.262, 0.248, 0.159]})

    def test_example_2(self):
        """ Example 2 (Tables 5-7): partial consistency of rankings. """
        matrix = np.array([[20, 3, 91, 50, 80], [16, 50, 100, 11, 62], [11, 50, 97, 22, 68], [10, 100, 85, 10, 50],
                           [10, 55, 98, 10, 54], [12, 43, 92, 18, 56], [8, 35, 84, 6, 59], [4, 30, 89, 15, 43],
                           [2, 36, 76, 5, 53], [13, 45, 79, 4, 5]])
        self._check(matrix, {
            0: [0.812, 0.673, 0.638, 0.631, 0.575, 0.537, 0.43, 0.366, 0.353, 0.346],
            0.5: [0.644, 0.6, 0.6, 0.546, 0.523, 0.517, 0.381, 0.339, 0.275, 0.274],
            1: [0.477, 0.528, 0.563, 0.461, 0.47, 0.496, 0.331, 0.312, 0.196, 0.203]})

    def test_example_3(self):
        """ Example 3 (Tables 10-12): no consistency of rankings. """
        matrix = np.array([[20, 3, 91, 50, 80], [16, 50, 100, 11, 62], [11, 50, 97, 25, 68], [10, 100, 85, 10, 50],
                           [11, 60, 98, 10, 54], [20, 35, 84, 6, 59], [12, 43, 92, 18, 56], [2, 36, 76, 5, 53],
                           [13, 45, 79, 4, 5], [4, 20, 80, 15, 43]])
        self._check(matrix, {
            0: [0.815, 0.667, 0.651, 0.631, 0.595, 0.58, 0.537, 0.365, 0.332, 0.3],
            0.5: [0.647, 0.593, 0.617, 0.545, 0.541, 0.485, 0.516, 0.286, 0.26, 0.273],
            1: [0.479, 0.52, 0.583, 0.46, 0.487, 0.389, 0.495, 0.207, 0.188, 0.245]})
        self.assertListEqual([5, 2, 1, 6, 4, 7, 3, 9, 10, 8],
                             methods.MIDIA(1).rank(methods.MIDIA(1)(matrix, self.weights, self.types))
                             .astype(int).tolist())

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.MIDIA(alpha=1.5)
