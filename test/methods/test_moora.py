# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestMOORA(unittest.TestCase):
    """ Test output method with reference:
    [1] Siregar, V. M. M., Tampubolon, M. R., Parapat, E. P. S., Malau, E. I.,
    & Hutagalung, D. S. (2021, February). Decision support system for selection technique using MOORA method. In IOP
    Conference Series: Materials Science and Engineering (Vol. 1088, No. 1, p. 012022). IOP Publishing.
    """

    def test_output(self):
        body = methods.MOORA()
        matrix = np.array([[1.5, 3, 5, 3.3],
                           [2, 7, 5, 3.35],
                           [3, 1, 5, 3.07],
                           [2.2, 4, 5, 3.5],
                           [2, 5, 3, 3.09],
                           [3.2, 2, 3, 3.48],
                           [2.775, 3, 5, 3.27]])

        weights = np.array([0.3, 0.2, 0.1, 0.4])
        types = np.array([-1, 1, 1, 1])

        output = [0.1801, 0.2345, 0.0625, 0.1757, 0.1683, 0.0742, 0.1197]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)
