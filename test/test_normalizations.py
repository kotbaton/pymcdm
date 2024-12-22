# Copyright (c) 2024 Andrii Shekhovtsov
# Copyright (c) 2024 Bartłomiej Kizielewicz

import unittest
import numpy as np

from pymcdm import normalizations as norm
from pymcdm import helpers


class TestMinmaxNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.85294118, 0.1875, 0.0, 1.0, 0.25, 0.85542169, 0.88235294, 0.625, 0.21686747, 0.0, 0.1875,
                  0.04819277, 0.94117647, 1.0, 1.0, 0.61764706, 0.0, 0.54216867]

        for arg in (norm.minmax_normalization, 'minmax', 'minmax_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 8) for val in output_method]
            self.assertListEqual(output, output_method)


class TestMaxNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.30526316, 0.05084746, 0.53370787, 0.35789474, 0.06779661, 0.93258427, 0.31578947, 0.16949153,
                  0.63483146, 0.0, 0.05084746, 0.55617978, 0.33684211, 0.27118644, 1.0, 0.22105263, 0.0, 0.78651685]

        for arg in (norm.max_normalization, 'max', 'max_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
        output_method = [round(val, 8) for val in output_method]
        self.assertListEqual(output, output_method)


class TestSumNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.17447136, 0.155945, 0.12010114, 0.1887723, 0.15878037, 0.20986094, 0.17715554, 0.17822286,
                  0.14285714, 0.12121168, 0.155945, 0.12515803, 0.18277952, 0.20309117, 0.22503161, 0.15560959,
                  0.1480156, 0.17699115]

        for arg in (norm.sum_normalization, 'sum', 'sum_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
        output_method = [round(val, 8) for val in output_method]
        self.assertListEqual(output, output_method)


class TestVectorNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.62375904, 0.57085288, 0.28587109, 0.65226214, 0.57851622, 0.49952212, 0.62945966, 0.62449627,
                  0.34003614, 0.45844104, 0.57085288, 0.29790777, 0.6408609, 0.67047632, 0.53563215, 0.57815408,
                  0.54786285, 0.42128371]

        for arg in (norm.vector_normalization, 'vector', 'vector_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
        output_method = [round(val, 8) for val in output_method]
        self.assertListEqual(output, output_method)


class TestLogarithmicNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[2, 10, 6],
                           [2, 5, 7],
                           [3, 3, 11],
                           [4, 2, 2],
                           [2, 9, 4],
                           [1, 5, 6]])

        types = np.array([-1, -1, 1])
        output = [0.16962777, 0.15157776, 0.1790548, 0.16962777, 0.16615431, 0.19445945, 0.15186115, 0.17689672,
                  0.2396274, 0.13925554, 0.18542345, 0.06926785, 0.16962777, 0.15379344, 0.1385357, 0.2, 0.16615431,
                  0.1790548]

        for arg in (norm.logarithmic_normalization, 'logarithmic', 'logarithmic_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 8) for val in output_method]
            self.assertListEqual(output, output_method)


class TestLinearNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.92424242, 0.76785714, 0.53370787, 1.0, 0.78181818, 0.93258427, 0.93846154, 0.87755102, 0.63483146,
                  0.64210526, 0.76785714, 0.55617978, 0.96825397, 1.0, 1.0, 0.82432432, 0.72881356, 0.78651685]

        for arg in (norm.linear_normalization, 'linear', 'linear_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 8) for val in output_method]
            self.assertListEqual(output, output_method)


class TestNonlinearNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.78951011, 0.4527321, 0.28484409, 1.0, 0.47787829, 0.86971342, 0.82651252, 0.67579835, 0.40301098,
                  0.26473947, 0.4527321, 0.30933594, 0.90775334, 1.0, 1.0, 0.56013711, 0.38712332, 0.61860876]

        for arg in (norm.nonlinear_normalization, 'nonlinear', 'nonlinear_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 8) for val in output_method]
            self.assertListEqual(output, output_method)


class TestEANormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.9137931, 0.78333333, 0.70036101, 1.0, 0.8, 0.9566787, 0.93103448, 0.9, 0.76534296, 0.4137931,
                  0.78333333, 0.71480144, 0.96551724, 1.0, 1.0, 0.77586207, 0.73333333, 0.86281588]

        for arg in (norm.enhanced_accuracy_normalization,
                    'enhanced_accuracy',
                    'enhanced_accuracy_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 8) for val in output_method]
            self.assertListEqual(output, output_method)


class TestZTNormalization(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[66, 56, 95],
                           [61, 55, 166],
                           [65, 49, 113],
                           [95, 56, 99],
                           [63, 43, 178],
                           [74, 59, 140]])

        types = np.array([-1, -1, 1])
        output = [0.91803279, 0.69767442, 0.53370787,
                  1.0, 0.72093023, 0.93258427,
                  0.93442623, 0.86046512, 0.63483146,
                  0.44262295, 0.69767442, 0.55617978,
                  0.96721311, 1.0, 1.0,
                  0.78688525, 0.62790698, 0.78651685]

        for arg in (norm.zavadskas_turskis_normalization,
                    'zavadskas_turskis',
                    'zavadskas_turskis_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 8) for val in output_method]
            self.assertListEqual(output, output_method)

class TestZTNormalization2(unittest.TestCase):
    """ [1] Jahan, A., & Edwards, K. L. (2015). A state-of-the-art survey on the influence of normalization techniques in ranking: Improving the materials selection process in engineering design. Materials & Design (1980-2015), 65, 335-342. """

    def test_output(self):
        matrix = np.array([[1, 6],
                           [2, 7],
                           [5, 10]])

        types = np.array([1, 1])

        output = [0.2, 0.6, 0.4, 0.7, 1.0, 1.0]


        for arg in (norm.zavadskas_turskis_normalization,
                    'zavadskas_turskis',
                    'zavadskas_turskis_normalization'):
            output_method = helpers.normalize_matrix(matrix, arg, types).reshape(-1)
            output_method = [round(val, 1) for val in output_method]
            self.assertListEqual(output, output_method)


class TestNormalizeMatrix(unittest.TestCase):
    """ Test output method without reference """
    def setUp(self):
        self.matrix = np.array([[10, 3],
                                [4, 2],
                                [6, 5]])
        self.good_types = np.array([1, 1])
        self.bad_types = np.array([1, 1, -1])
        self.bad_types1 = np.array([0, 1])
        self.one_method = norm.max_normalization
        self.two_methods = [norm.max_normalization, norm.sum_normalization]
        self.wrong_methods = [norm.max_normalization]

    def test_correct_data1(self):
        output = list(helpers.normalize_matrix(self.matrix,
                                               self.one_method,
                                               self.good_types).T.reshape(-1))
        self.assertListEqual(output, [1, 0.4, 0.6, 0.6, 0.4, 1.0])

    def test_correct_data2(self):
        output = list(helpers.normalize_matrix(self.matrix,
                                               self.two_methods,
                                               self.good_types).T.reshape(-1))
        self.assertListEqual(output, [1, 0.4, 0.6, 0.3, 0.2, 0.5])

    def test_wrong_data1(self):
        self.assertRaises(
                ValueError,
                helpers.normalize_matrix,
                self.matrix,
                self.wrong_methods,
                self.good_types
                )

    def test_wrong_data2(self):
        self.assertRaises(
                ValueError,
                helpers.normalize_matrix,
                self.matrix,
                self.one_method,
                self.bad_types
                )

    def test_wrong_data3(self):
        self.assertRaises(
                ValueError,
                helpers.normalize_matrix,
                self.matrix,
                self.one_method,
                self.bad_types1
                )

    def test_wrong_norm1(self):
        self.assertRaises(
                AttributeError,
                helpers.normalize_matrix,
                self.matrix,
                'non_existed_norm',
                self.bad_types1
                )

    def test_wrong_norm2(self):
        self.assertRaises(
                AttributeError,
                helpers.normalize_matrix,
                self.matrix,
                ['non_existed_norm', 'non_existed_norm2'],
                self.good_types
                )