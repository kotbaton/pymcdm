# Copyright (c) 2023 Andrii Shekhovtsov
# Copyright (c) 2023 Bartłomiej Kizielewicz

import unittest

import numpy as np

from pymcdm.methods import TOPSIS, COMET
from pymcdm.methods.comet_tools import (MethodExpert, Submodel,
                                        StructuralCOMET, triads_consistency)


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
                                 TOPSIS(),
                                 np.ones(3)/3, [1, 1, 1]),
                             'P_1'),
                    Submodel((3, 4),
                             [0.00000000e+00, 4.43071484e-01, 1.00000000e+00],
                             MethodExpert(
                                 TOPSIS(),
                                 np.ones(2)/2, [1, 1]),
                             'P_2'),
                    Submodel((5, 6, 7),
                             [1.49566750e-01, 4.81255932e-01, 7.15106856e-01],
                             MethodExpert(
                                 TOPSIS(),
                                 np.ones(3)/3, [-1, -1, 1]),
                             'P_3'),
                    Submodel(('P_1', 'P_3', 'P_2', 'C_9'),
                             None,
                             MethodExpert(
                                 TOPSIS(),
                                 np.ones(4)/4, [1, 1, 1, -1]),
                             'P Final')
                    ],
                cvalues=cvalues,
                criteria_names=criteria_names
                )

        res = model(matrix, weights=None, types=None, verbose=True)

        reference = {
            'P_1': [0.7851, 0.6136, 0.5950, 0.7187, 0.1378,
                    0.0917, 0.3298, 0.5354, 0.6491, 0.0824],
            'P_2': [1.0000, 1.0000, 0.3492, 0.6850, 0.1715,
                    0.1715, 0.1715, 0.2110, 0.6709, 0.0000],
            'P_3': [0.3684, 0.3684, 0.7151, 0.3927, 0.6439,
                    0.6439, 0.4342, 0.4062, 0.6901, 0.1496],
            'P Final': [0.5732, 0.5972, 0.7718, 0.6996, 0.4911,
                        0.4619, 0.4595, 0.5138, 0.8374, 0.1512]
        }

        res = res.to_dict()
        for key in reference:
            self.assertListEqual(list(np.round(res[key].data, 4)), reference[key])


class TestTriadsConsistency_MEJ(unittest.TestCase):
    """ Test output of the triads_consistency coefficient.
    Sałabun, W., Shekhovtsov, A., & Kizielewicz, B. (2021, June). A new
    consistency coefficient in the multi-criteria decision analysis domain.
    In Computational Science–ICCS 2021: 21st International Conference, Krakow,
    Poland, June 16–18, 2021, Proceedings, Part I (pp. 715-727).
    Cham: Springer International Publishing.
    """
    def test_output(self):
        mej = np.array([
            [0.5,   0,   0,   0,   0,   0],
            [  1, 0.5,   0,   0,   0,   0],
            [  1,   1, 0.5,   0,   0,   0],
            [  1,   1,   1, 0.5,   0,   0],
            [  1,   1,   1,   1, 0.5,   0],
            [  1,   1,   1,   1,   1, 0.5]
        ])

        self.assertEqual(triads_consistency(mej), 1.0)

        mej = np.array([
            [0.5,   0,   0,   0,   0,   1],
            [  1, 0.5,   0,   0,   0,   0],
            [  1,   1, 0.5,   0,   0,   0],
            [  1,   1,   1, 0.5,   0,   0],
            [  1,   1,   1,   1, 0.5,   0],
            [  0,   1,   1,   1,   1, 0.5]
        ])

        self.assertEqual(triads_consistency(mej), 0.8)

        mej = np.array([
            [0.5,   0,   0,   1,   0,   1],
            [  1, 0.5,   0,   0,   0,   0],
            [  1,   1, 0.5,   0,   0,   0],
            [  0,   1,   1, 0.5,   0,   0],
            [  1,   1,   1,   1, 0.5,   0],
            [  0,   1,   1,   1,   1, 0.5]
        ])

        self.assertEqual(triads_consistency(mej), 0.75)

class TestTriadsConsistency_COMET(unittest.TestCase):
    """ Test output of the triads_consistency coefficient."""
    def test_output(self):
        cvalues = [
                [1, 3, 5],
                [1, 3, 5]
                ]
        comet = COMET(cvalues, MethodExpert(TOPSIS(), np.ones(2)/2, [1, -1]))

        self.assertEqual(triads_consistency(comet), 1.0)
