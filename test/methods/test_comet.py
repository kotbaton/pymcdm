# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods
from pymcdm.methods.comet_tools import MethodExpert

class TestCOMET(unittest.TestCase):
    """ Test output method with reference:
    [1] Paradowski, B., Bączkiewicz, A., & Watrąbski, J. (2021). Towards
    proper consumer choices-MCDM based product selection. Procedia Computer Science, 192, 1347-1358.
    """

    def test_output(self):
        matrix = np.array([[64, 128, 2.9, 4.3, 3.2, 280, 495, 24763, 3990],
                           [28, 56, 3.1, 3.8, 3.8, 255, 417, 12975, 2999],
                           [8, 16, 3.5, 5.3, 4.8, 125, 636, 5725, 539],
                           [12, 24, 3.7, 4.8, 4.5, 105, 637, 8468, 549],
                           [10, 20, 3.7, 5.3, 4.9, 125, 539, 6399, 499],
                           [8, 16, 3.6, 4.4, 4.0, 65, 501, 4834, 329],
                           [6, 12, 3.7, 4.6, 4.2, 65, 604, 4562, 299],
                           [16, 32, 3.4, 4.9, 4.2, 105, 647, 10428, 799],
                           [8, 16, 3.6, 5.0, 4.5, 125, 609, 5615, 399],
                           [18, 36, 3.0, 4.8, 4.3, 165, 480, 8848, 979],
                           [24, 48, 3.8, 4.5, 4.0, 280, 509, 13552, 1399],
                           [28, 56, 2.5, 3.8, 2.8, 205, 376, 8585, 10000]])

        cvalues = np.vstack((
            np.min(matrix, axis=0),
            np.max(matrix, axis=0)
        )).T

        types = np.array([1, 1, 1, 1, 1, -1, 1, 1, -1])
        weights = np.array([1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9])

        body = methods.COMET(cvalues, MethodExpert(methods.TOPSIS(), weights, types))

        output = [0.5433, 0.3447, 0.6115, 0.6168, 0.6060, 0.4842, 0.5516, 0.6100, 0.5719, 0.4711, 0.4979, 0.1452]
        output_method = [round(preference, 4) for preference in body(matrix)]

        self.assertListEqual(output, output_method)

    def test_gray_code(self):
        from pymcdm.methods.comet import _gray_code_product

        cvalues = np.array([[1, 2], [10, 20]])
        result = _gray_code_product(*cvalues)
        expected = [[1, 10], [1, 20], [2, 20], [2, 10]]
        self.assertListEqual(list(result), expected)
