# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestOCRA(unittest.TestCase):
    """ Test output method with reference:
    [1] Işık, A. T., & Adalı, E. A. (2016). A new integrated decision making
    approach based on SWARA and OCRA methods for the hotel selection problem. International Journal of Advanced
    Operations Management, 8(2), 140-151.
    """

    def test_output(self):
        body = methods.OCRA()
        matrix = np.array([[7.7, 256, 7.2, 7.3, 7.3],
                           [8.1, 250, 7.9, 7.8, 7.7],
                           [8.7, 352, 8.6, 7.9, 8.0],
                           [8.1, 262, 7.0, 8.1, 7.2],
                           [6.5, 271, 6.3, 6.4, 6.1],
                           [6.8, 228, 7.1, 7.2, 6.5]])

        weights = np.array([0.239, 0.225, 0.197, 0.186, 0.153])
        types = np.array([1, -1, 1, 1, 1])

        output = [0.143, 0.210, 0.164, 0.167, 0, 0.112]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
