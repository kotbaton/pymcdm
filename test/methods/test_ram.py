# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestRAM(unittest.TestCase):
    """ Test output method with reference:
    [1] Sotoudeh-Anvari, A. (2023). Root Assessment Method (RAM): A novel
    multi-criteria decision making method and its applications in
    sustainability challenges. Journal of Cleaner Production, 138695.
    """
    def test_output(self):
        matrix = np.array([
            [0.068, 0.066, 0.150, 0.098, 0.156, 0.114, 0.098],
            [0.078, 0.076, 0.108, 0.136, 0.082, 0.171, 0.105],
            [0.157, 0.114, 0.128, 0.083, 0.108, 0.113, 0.131],
            [0.106, 0.139, 0.058, 0.074, 0.132, 0.084, 0.120],
            [0.103, 0.187, 0.125, 0.176, 0.074, 0.064, 0.057],
            [0.105, 0.083, 0.150, 0.051, 0.134, 0.094, 0.113],
            [0.137, 0.127, 0.056, 0.133, 0.122, 0.119, 0.114],
            [0.100, 0.082, 0.086, 0.060, 0.062, 0.109, 0.093],
            [0.053, 0.052, 0.043, 0.100, 0.050, 0.078, 0.063],
            [0.094, 0.074, 0.097, 0.087, 0.080, 0.054, 0.106]
        ])

        weights = np.array([0.132, 0.135, 0.138, 0.162, 0.09, 0.223, 0.12])

        types = np.array([1, -1, -1, 1, 1, 1, 1])

        ram = methods.RAM()
        output_method = ram(matrix, weights, types)

        output_method = list(np.round(output_method, 4))

        output = [1.4332, 1.4392, 1.4353, 1.4322, 1.4279,
                  1.4301, 1.4394, 1.4308, 1.4294, 1.4288]
        self.assertListEqual(output, output_method)
