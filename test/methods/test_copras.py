# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestCOPRAS(unittest.TestCase):
    """Reference tests for the COPRAS method."""

    def test_zavadskas_1994(self):
        """Test from the original COPRAS paper.

        Reference:
        Zavadskas, E. K., Kaklauskas, A., & Šarka, V. (1994).
        The new method of multicriteria complex proportional assessment
        of projects.
        Technological and Economic Development of Economy, 1(3), 131-139.
        """

        matrix = np.array([
            [223.0, 25.1, 0.7, 0.7, 0.5, 0.8, 0.9, 0.3, 1.0,  2902.3, 6150.0, 0.3, 0.5],
            [203.0, 14.9, 0.8, 0.8, 0.4, 0.5, 0.7, 0.2, 0.2,  2880.0, 6040.0, 0.2, 0.5],
            [410.0, 100.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.3, 19230.0, 1005.0, 1.0, 1.0],
        ])

        weights = np.array([
            0.2869, 0.0480, 0.0287, 0.0230, 0.0086, 0.0345, 0.2238,
            0.0143, 0.3242, 0.2575, 0.4075, 0.0287, 0.0143,
        ])

        types = np.array([
            -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1,
        ])

        body = methods.COPRAS()

        # Skip validation as sum of the weights in the paper is 1.7
        output = [1.0000, 0.7415, 0.7178]
        output_method = [
            round(preference, 4)
            for preference in body(matrix, weights, types, validation=False)
        ]

        self.assertListEqual(output, output_method)

    def test_kaklauskas_2006(self):
        """Test from a COPRAS application to low-e window selection.

        Reference:
        Kaklauskas, A., Zavadskas, E. K., Raslanas, S., Ginevicius, R.,
        Komka, A., & Malinauskas, P. (2006).
        Selection of low-e windows in retrofit of public buildings by
        applying multiple criteria method COPRAS: A Lithuanian case.
        Energy and Buildings, 38(5), 454-462.
        """

        matrix = np.array([
            [1.0, 10000.0, 1.2, 1.10, 0.05, 34.0, 0.18, 600.0, 10.0, 35.0, 81.0, 60.0, 78.50, 78.50],
            [1.0, 10000.0, 1.4, 1.20, 0.10, 33.0, 0.15, 300.0,  5.0, 30.0, 78.0, 50.0, 100.0, 100.0],
            [1.0, 10000.0, 1.4, 1.10, 0.05, 34.0, 0.18, 600.0,  5.0, 50.0, 81.0, 60.0, 37.00, 37.00],
            [1.0, 1000.0,  1.4, 1.10, 0.05, 33.0, 0.30, 250.0,  5.0, 40.0, 79.0, 60.0, 100.0, 100.0],
            [1.0, 10000.0, 1.4, 1.14, 0.05, 32.0, 0.31, 250.0,  5.0, 30.0, 78.0, 60.0, 27.43, 27.43],
        ])

        weights = np.array([
            0.06875, 0.07275, 0.09100, 0.10800, 0.05750, 0.08275, 0.06150,
            0.07550, 0.07550, 0.07725, 0.05500, 0.05625, 0.05375, 0.06450,
        ])

        types = np.array([
            1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1,
        ])

        body = methods.COPRAS()

        expected = np.array([1.0000, 0.8687, 0.8977, 0.8154, 0.7504])

        output = body(matrix, weights, types)

        np.testing.assert_allclose(
            output,
            expected,
            atol=1e-2,
        )

    def test_kundakci_isik_2016(self):
        """Test from COPRAS application to air compressor selection.

        Reference:
        Kundakcı, N., & Işık, A. (2016).
        Integration of MACBETH and COPRAS methods to select air compressor
        for a textile company.
        Decision Science Letters, 5(3), 381-394.
        https://doi.org/10.5267/j.dsl.2016.2.003
        """

        matrix = np.array([
            [1543, 2000, 39000, 15, 13.76, 3.86, 5, 3, 5000],
            [1496, 3600, 43000, 14, 14.00, 2.50, 4, 4, 4000],
            [1584, 3100, 24500, 10, 13.10, 3.70, 2, 2, 3500],
            [1560, 2700, 36000, 12, 13.20, 3.20, 3, 3, 3500],
            [1572, 2500, 31500, 13, 13.30, 3.40, 3, 2, 3500],
            [1580, 2400, 20000, 12, 12.80, 3.90, 2, 2, 3000],
        ])

        weights = np.array([
            0.2027, 0.1757, 0.1622, 0.1351, 0.1081,
            0.0946, 0.0676, 0.0405, 0.0135,
        ])

        types = np.array([
            -1, -1, -1, 1, 1, -1, 1, 1, 1,
        ])

        body = methods.COPRAS()

        # Expected utility degrees from the paper.
        # Rounded to 4 decimal places.
        output = [1.0000, 0.9167, 0.8675, 0.9084, 0.9315, 0.9486]

        output_method = [
            round(preference, 4)
            for preference in body(matrix, weights, types)
        ]

        self.assertListEqual(output, output_method)
