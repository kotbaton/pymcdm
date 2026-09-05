# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestSPOTIS(unittest.TestCase):
    """ Test output method with reference:
    [1] Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The spotis rank reversal free method for
    multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION)
    (pp. 1-8). IEEE.
    """

    def test_output(self):
        matrix = np.array([[10.5, -3.1, 1.7],
                           [-4.7, 0, 3.4],
                           [8.1, 0.3, 1.3],
                           [3.2, 7.3, -5.3]])
        bounds = np.array([[-5, 12],
                           [-6, 10],
                           [-8, 5]], dtype=float)
        weights = np.array([0.2, 0.3, 0.5])

        types = np.array([1, -1, 1])

        body = methods.SPOTIS(bounds)
        output = [0.1989, 0.3705, 0.3063, 0.7491]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestSPOTIS2(unittest.TestCase):
    """ Test output method with reference:
    [1] Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The spotis rank reversal free method for
    multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION)
    (pp. 1-8). IEEE.
    """

    def test_output(self):
        matrix = np.array([
            [15000, 4.3, 99, 42, 737],
            [15290, 5.0, 116, 42, 892],
            [15350, 5.0, 114, 45, 952],
            [15490, 5.3, 123, 45, 1120],
            ], dtype='float')
        bounds = np.array([
            [14000, 16000],
            [3, 8],
            [80, 140],
            [35, 60],
            [650, 1300]
            ])
        weights = np.array([0.2941, 0.2353, 0.2353, 0.0588, 0.1765])

        types = np.array([-1, -1, -1, 1, 1])

        esp = np.array([15300, 4, 115, 50, 900])

        body = methods.SPOTIS(bounds, esp)
        output = [0.1841, 0.0734, 0.0842, 0.1920]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
