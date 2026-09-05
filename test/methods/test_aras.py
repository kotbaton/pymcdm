# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestARAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Stanujkic, D., Djordjevic, B., & Karabasevic, D. (2015). Selection of
    candidates in the process of recruitment and selection of personnel based on the SWARA and ARAS methods.
    Quaestus, (7), 53.
    
    [2] Zavadskas, E. K., & Turskis, Z. (2010). A new additive ratio assessment (ARAS) method in Multicriteria
    Decision‐Aaking / Naujas adityvinis kriterijų santykių įvertinimo metodas (ARAS) Daugiakriteriniams uždaviniams
    spręsti. Technological and Economic Development of Economy, 16(2), 159–172. https://doi.org/10.3846/tede.2010.10
    """

    def test_output(self):
        body = methods.ARAS()
        matrix = np.array([[4.64, 3.00, 3.00, 3.00, 2.88, 3.63],
                           [4.00, 4.00, 4.64, 3.56, 3.63, 5.00],
                           [3.30, 4.31, 3.30, 4.00, 3.30, 4.00],
                           [2.62, 5.00, 4.22, 4.31, 5.00, 5.00]])

        weights = np.array([0.28, 0.25, 0.19, 0.15, 0.08, 0.04])
        types = np.array([1, 1, 1, 1, 1, 1])

        output = [0.74, 0.86, 0.78, 0.86]
        output_method = [round(preference, 2) for preference in body(matrix, weights, types, validation=False)]

        self.assertListEqual(output, output_method)

    def test_output2(self):
        xopt = np.array([15, 50, 24.5, 400, 0.05, 5])
        body = methods.ARAS(esp=xopt)
        matrix = np.array([
            [7.6, 46, 18, 390, 0.1, 11],
            [5.5, 32, 21, 360, 0.05, 11],
            [5.3, 32, 21, 290, 0.05, 11],
            [5.7, 37, 19, 270, 0.05, 9],
            [4.2, 38, 19, 240, 0.1, 8],
            [4.4, 38, 19, 260, 0.1, 8],
            [3.9, 42, 16, 270, 0.1, 5],
            [7.9, 44, 20, 400, 0.05, 6],
            [8.1, 44, 20, 380, 0.05, 6],
            [4.5, 46, 18, 320, 0.1, 7],
            [5.7, 48, 20, 320, 0.05, 11],
            [5.2, 48, 20, 310, 0.05, 11],
            [7.1, 49, 19, 280, 0.1, 12],
            [6.9, 50, 16, 250, 0.05, 10]
        ])

        weights = np.array([0.21, 0.16, 0.26, 0.17, 0.12, 0.08])
        types = np.array([1, 1, 1, 1, -1, -1])

        # The output is different from [2]. Supposedly because of numerical errors we got slightly different results.
        output = [0.6706, 0.6564, 0.6269, 0.6315, 0.5464, 0.5580, 0.5658,
                  0.7762, 0.7734, 0.6003, 0.6772, 0.6628, 0.6334, 0.6511]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types, validation=False)]

        self.assertListEqual(output, output_method)
