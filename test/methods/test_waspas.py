# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestWASPAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Chakraborty, S., Zavadskas, E. K., & Antucheviciene, J. (2015). Applications of WASPAS method as a
    multi-criteria  decision-making tool. Economic Computation and Economic Cybernetics Studies and Research, 49(1),
    5-22.
    """
    def test_output(self):
        body = methods.WASPAS()
        matrix = np.array([[30, 23, 5, 0.745, 0.745, 1500, 5000],
                           [18, 13, 15, 0.745, 0.745, 1300, 6000],
                           [15, 12, 10, 0.500, 0.500, 950, 7000],
                           [25, 20, 13, 0.745, 0.745, 1200, 4000],
                           [14, 18, 14, 0.255, 0.745, 950, 3500],
                           [17, 15, 9, 0.745, 0.500, 1250, 5250],
                           [23, 18, 20, 0.500, 0.745, 1100, 3000],
                           [16, 8, 14, 0.255, 0.500, 1500, 3000]])
        weights = np.array([0.1181, 0.1181, 0.0445, 0.1181, 0.2861, 0.2861, 0.0445])
        types = np.array([1, 1, 1, 1, 1, -1, -1])
        output_method = list(np.round(body(matrix, weights, types, validation=False), 4))
        output = [0.8329, 0.7884, 0.6987, 0.8831, 0.7971, 0.7036, 0.8728, 0.5749]

        self.assertListEqual(output, output_method)
