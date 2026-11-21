# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestMARCOS(unittest.TestCase):
    """ Test output method with reference:
    [1] Ulutaş, A., Karabasevic, D., Popovic, G., Stanujkic, D., Nguyen,
    P. T., & Karaköy, Ç. (2020). Development of a novel integrated CCSD-ITARA-MARCOS decision-making approach for
    stackers selection in a logistics system. Mathematics, 8(10), 1672.
    """

    def test_output(self):
        body = methods.MARCOS()
        matrix = np.array([[660, 1000, 1600, 18, 1200],
                           [800, 1000, 1600, 24, 900],
                           [980, 1000, 2500, 24, 900],
                           [920, 1500, 1600, 24, 900],
                           [1380, 1500, 1500, 24, 1150],
                           [1230, 1000, 1600, 24, 1150],
                           [680, 1500, 1600, 18, 1100],
                           [960, 2000, 1600, 12, 1150]])

        weights = np.array([0.1061, 0.3476, 0.3330, 0.1185, 0.0949])
        types = np.array([-1, 1, 1, 1, 1])

        output = [0.5649, 0.5543, 0.6410, 0.6174, 0.6016, 0.5453, 0.6282, 0.6543]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
