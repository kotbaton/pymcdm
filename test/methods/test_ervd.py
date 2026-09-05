# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestERVD(unittest.TestCase):
    """ Test output method with reference:
    [1] Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method based on
    relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.
    """
    def test_output(self):
        matrix = np.array([
            [80, 70, 87, 77, 76, 80, 75],
            [85, 65, 76, 80, 75, 65, 75],
            [78, 90, 72, 80, 85, 90, 85],
            [75, 84, 69, 85, 65, 65, 70],
            [84, 67, 60, 75, 85, 75, 80],
            [85, 78, 82, 81, 79, 80, 80],
            [77, 83, 74, 70, 71, 65, 70],
            [78, 82, 72, 80, 78, 70, 60],
            [85, 90, 80, 88, 90, 80, 85],
            [89, 75, 79, 67, 77, 70, 75],
            [65, 55, 68, 62, 70, 50, 60],
            [70, 64, 65, 65, 60, 60, 65],
            [95, 80, 70, 75, 70, 75, 75],
            [70, 80, 79, 80, 85, 80, 70],
            [60, 78, 87, 70, 66, 70, 65],
            [92, 85, 88, 90, 85, 90, 95],
            [86, 87, 80, 70, 72, 80, 85]
        ])

        weights = np.array([0.066, 0.196, 0.066, 0.130, 0.130, 0.216, 0.196])
        types = np.ones(7)

        ref = np.ones(7) * 80

        ervd = methods.ERVD(ref_point=ref)
        output_method = list(np.round(ervd(matrix, weights, types), 3))
        output = [0.660, 0.503, 0.885, 0.521, 0.610, 0.796, 0.498, 0.549, 0.908, 0.565, 0.070, 0.199, 0.632, 0.716, 0.438, 0.972, 0.767]

        self.assertListEqual(output, output_method)
