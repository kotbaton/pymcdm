# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestPROBID(unittest.TestCase):
    """ Test output method with reference:
    [1] Wang, Z., Rangaiah, G. P., & Wang, X. (2021). Preference ranking on the basis of ideal-average distance method
    for multi-criteria decision-making. Industrial & Engineering Chemistry Research, 60(30), 11216-11230.
    """
    def test_output(self):
        matrix = np.array([
            [1.679 * 10**6, 1.525 * 10**(-7), 3.747 * 10**(-5), 0.251, 2.917],
            [2.213 * 10**6, 1.304 * 10**(-7), 3.250 * 10**(-5), 0.218, 6.633],
            [2.461 * 10**6, 1.445 * 10**(-7), 3.854 * 10**(-5), 0.259, 0.553],
            [2.854 * 10**6, 1.540 * 10**(-7), 3.970 * 10**(-5), 0.266, 1.597],
            [3.107 * 10**6, 1.522 * 10**(-7), 3.779 * 10**(-5), 0.254, 2.905],
            [3.574 * 10**6, 1.469 * 10**(-7), 3.297 * 10**(-5), 0.221, 6.378],
            [3.932 * 10**6, 1.977 * 10**(-7), 3.129 * 10**(-5), 0.210, 11.381],
            [4.383 * 10**6, 1.292 * 10**(-7), 3.142 * 10**(-5), 0.211, 9.929],
            [4.988 * 10**6, 1.690 * 10**(-7), 3.767 * 10**(-5), 0.253, 8.459],
            [5.497 * 10**6, 5.703 * 10**(-7), 3.012 * 10**(-5), 0.200, 18.918],
            [5.751 * 10**6, 4.653 * 10**(-7), 3.017 * 10**(-5), 0.201, 17.517],
        ])

        weights = np.array([0.1819, 0.2131, 0.1838, 0.1832, 0.2379])
        types = np.array([1, -1, -1, -1, -1])

        pr = methods.PROBID()
        output_method = list(np.round(pr(matrix, weights, types), 4))
        output = [0.8568, 0.7826, 0.9362, 0.9369, 0.9379, 0.8716, 0.5489, 0.7231, 0.7792, 0.3331, 0.3387]
        self.assertListEqual(output, output_method)

        # Example is slightly modified to eliminate rounding errors
        pr = methods.SPROBID()
        output_method = list(np.round(pr(matrix, weights, types), 4))
        output = [2.4246, 2.0596, 3.2806, 3.3702, 3.4374, 2.6435, 1.2628, 1.8158, 2.0885, 0.3399, 0.4279]
        self.assertListEqual(output, output_method)
