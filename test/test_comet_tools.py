import unittest

import numpy as np
import pandas as pd

import pymcdm as pm
from pymcdm.comet_tools import MethodExpert, Submodel, StructuralCOMET


class TestStructuralCOMET(unittest.TestCase):
    """ Test output method with reference:
    Shekhovtsov, A., Kołodziejczyk, J., & Sałabun, W. (2020). Fuzzy model
    identification using monolithic and structured approaches in decision
    problems with partially incomplete data. Symmetry, 12(9), 1541.
    """

    def test_output(self):
        cvalues = [
                [340, 909.3, 3000],
                [57, 107.3, 150],
                [100, 144, 180],
                [10, 87.9, 200],
                [80, 325.8, 610],
                [4, 7, 10],
                [10, 54, 120],
                [10.5, 37.57, 99],
                [12.9, 43.3, 120]
                ]

        criteria_names = [f'C_{i+1}' for i in range(len(cvalues))]

        matrix = np.array([
            [3000,  96, 145, 200, 610, 10.0, 120, 99.0, 120.0],
            [2000, 100, 145, 200, 610, 10.0, 120, 99.0,  90.0],
            [ 705, 120, 170,  80, 270,  4.0,  30, 24.0,  25.0],
            [ 613, 140, 180, 140, 400,  8.0,  40, 24.2,  50.0],
            [ 350, 100, 110,  30, 196,  4.5,  15, 10.5,  12.9],
            [ 350, 100, 100,  30, 196,  4.5,  15, 10.5,  15.5],
            [ 350, 100, 150,  30, 196,  7.0,  35, 16.0,  18.7],
            [ 635, 110, 170,  49, 200,  8.0,  35, 22.5,  31.5],
            [ 340, 150, 160, 110, 500,  6.0,  10, 35.0,  45.0],
            [ 750,  57, 110,  10,  80,  8.0, 120, 35.0,  24.4]
            ], dtype='float')

        model = StructuralCOMET(
                submodels=[
                    Submodel((0, 1, 2),
                             [8.24041444e-02, 4.53869580e-01, 7.85105159e-01],
                             MethodExpert(
                                 pm.methods.TOPSIS(),
                                 np.ones(3)/3, [1, 1, 1]),
                             'P_1'),
                    Submodel((3, 4),
                             [0.00000000e+00, 4.43071484e-01, 1.00000000e+00],
                             MethodExpert(
                                 pm.methods.TOPSIS(),
                                 np.ones(2)/2, [1, 1]),
                             'P_2'),
                    Submodel((5, 6, 7),
                             [1.49566750e-01, 4.81255932e-01, 7.15106856e-01],
                             MethodExpert(
                                 pm.methods.TOPSIS(),
                                 np.ones(3)/3, [-1, -1, 1]),
                             'P_3'),
                    Submodel(('P_1', 'P_3', 'P_2', 'C_9'),
                             None,
                             MethodExpert(
                                 pm.methods.TOPSIS(),
                                 np.ones(4)/4, [1, 1, 1, -1]),
                             'P Final')
                    ],
                cvalues=cvalues,
                criteria_names=criteria_names
                )

        res = model(matrix, True, True)

        reference = {
                'P_1': ... #TODO
        }

        # p1_res = np.round(res['P_1'], 4)
        # p2_res = np.round(res['P_2'], 4)
        # p3_res = np.round(res['P_3'], 4)
        # p_final_res = np.round(res['P Final'], 4)
        #
        # print(p1_res, p2_res, p3_res, p_final_res, sep='\n')

        # self.assertListEqual(output, output_method)
