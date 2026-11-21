# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestMAIRCA(unittest.TestCase):
    """ Test output method with reference:
    [1] Aksoy, E. (2021). An Analysis on Turkey's Merger and Acquisition
    Activities: MAIRCA Method. Gümüşhane Üniversitesi Sosyal Bilimler Enstitüsü Elektronik Dergisi, 12(1), 1-11.
    """

    def test_output(self):
        body = methods.MAIRCA()
        matrix = np.array([[70, 245, 16.4, 19],
                           [52, 246, 7.3, 22],
                           [53, 295, 10.3, 25],
                           [63, 256, 12, 8],
                           [64, 233, 5.3, 17]])
        weights = np.array([0.04744, 0.02464, 0.51357, 0.41435])
        types = np.array([1, 1, 1, 1])

        output = [0.0332, 0.1122, 0.0654, 0.1304, 0.1498]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
