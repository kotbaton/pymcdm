# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np
from scipy.stats import rankdata

from pymcdm import methods


class TestGRA(unittest.TestCase):
    """ Test output method with reference:
    [1] Kuo, Y., Yang, T., & Huang, G. W. (2008). The use of grey relational analysis in solving multiple attribute
    decision-making problems. Computers & Industrial Engineering, 55(1), 80-93.
    """

    # Table 1: flow distance, adjacency score, shape ratio, flexibility, accessibility, maintenance. Tables 2-4 were
    # calculated with the flow distance 185.59 of alternative 9 (Table 1: 185.85) and the adjacency score 9 of
    # alternative 17 (Table 1: 8), and these values are used here.
    layout = np.array([[185.95, 8, 8.28, 0.0494, 0.0294, 0.0130],
                       [207.37, 9, 3.75, 0.0494, 0.0147, 0.0519],
                       [206.38, 8, 7.85, 0.0370, 0.0147, 0.0519],
                       [189.66, 8, 8.28, 0.0370, 0.0147, 0.0519],
                       [211.46, 8, 7.71, 0.0617, 0.0147, 0.0390],
                       [264.07, 5, 2.07, 0.0494, 0.0147, 0.0519],
                       [228.00, 8, 14.00, 0.0247, 0.0735, 0.0649],
                       [185.59, 9, 6.25, 0.0370, 0.0441, 0.0390],
                       [185.59, 9, 7.85, 0.0741, 0.0441, 0.0519],
                       [236.15, 8, 7.85, 0.0741, 0.0588, 0.0649],
                       [183.18, 8, 2.00, 0.0864, 0.1029, 0.0909],
                       [204.18, 8, 13.30, 0.0370, 0.0588, 0.0260],
                       [225.26, 8, 8.14, 0.0247, 0.0735, 0.0519],
                       [202.82, 8, 8.00, 0.0247, 0.0588, 0.0519],
                       [170.14, 9, 8.28, 0.0864, 0.1176, 0.1169],
                       [216.38, 9, 7.71, 0.0741, 0.0735, 0.0519],
                       [179.80, 9, 10.30, 0.0988, 0.1324, 0.0909],
                       [185.75, 10, 10.16, 0.0741, 0.0588, 0.0390]])
    layout_types = np.array([-1, 1, 1, 1, 1, 1])
    # The desired value of the shape ratio is 1
    layout_targets = np.array([np.nan, np.nan, 1, np.nan, np.nan, np.nan])

    def test_output_layout(self):
        """ Facility layout problem (Tables 2-4), equal weights, distinguishing coefficient 0.5. Table 2 gives 0.2489
            for the accessibility of alternative 9 instead of 0.2498, which is used in Table 3.
        """
        body = methods.GRA(targets=self.layout_targets)
        nmatrix, coefficients, grades = [table.data for table in
                                         body(self.layout, np.ones(6) / 6, self.layout_types, verbose=True).results]

        self.assertListEqual([0.8317, 0.6, 0.44, 0.3333, 0.1249, 0.0], np.round(nmatrix[0], 4).tolist())
        self.assertListEqual([0.8972, 0.8, 0.2846, 1.0, 1.0, 0.7498], np.round(nmatrix[16], 4).tolist())
        self.assertListEqual([0.7481, 0.5556, 0.4717, 0.4286, 0.3636, 0.3333], np.round(coefficients[0], 4).tolist())
        self.assertListEqual([0.7525, 0.7143, 0.4869, 0.6, 0.3999, 0.4442], np.round(coefficients[8], 4).tolist())
        self.assertListEqual([0.4835, 0.5302, 0.4599, 0.481, 0.4688, 0.4552, 0.445, 0.5325, 0.5663, 0.5004, 0.7145,
                              0.444, 0.4616, 0.4748, 0.789, 0.5424, 0.7703, 0.6017],
                             np.round(grades, 4).tolist())
        self.assertListEqual([10, 8, 15, 11, 13, 16, 17, 7, 5, 9, 3, 18, 14, 12, 1, 6, 2, 4],
                             body.rank(grades).astype(int).tolist())

    def test_distinguishing_coefficient_layout(self):
        """ Fig. 4: alternatives 15, 17, 11, 18 and 9 are ranked 1-5 for all distinguishing coefficients. """
        for zeta in (0.1, 0.3, 0.5, 0.7, 0.9):
            with self.subTest(zeta=zeta):
                body = methods.GRA(zeta=zeta, targets=self.layout_targets)
                ranking = body.rank(body(self.layout, np.ones(6) / 6, self.layout_types))
                self.assertListEqual([1, 2, 3, 4, 5], ranking[[14, 16, 10, 17, 8]].astype(int).tolist())

    # Table 7: comparability sequences of the dispatching rule selection problem (MD, SPT, SLK, DD, GCMD, COST,
    # VALUE, COV, LPT), which are their own grey relational generating as profit criteria.
    dispatching = np.array([[1.0000, 0.3820, 0.9998, 0.7962, 0.0727],
                            [0.9997, 0.3708, 1.0000, 0.7962, 0.0803],
                            [0.9177, 0.3146, 0.8600, 0.6423, 0.9998],
                            [0.8397, 0.1517, 0.7553, 0.5346, 0.9999],
                            [0.7481, 0.2135, 0.5948, 0.2962, 0.3802],
                            [0.7704, 0.2079, 0.6352, 1.0000, 0.1797],
                            [0.7011, 0.2191, 0.6335, 0.8077, 0.0000],
                            [0.8206, 1.0000, 0.6521, 0.4115, 1.0000],
                            [0.0000, 0.0000, 0.0000, 0.0000, 0.0713]])

    def test_output_dispatching(self):
        """ Dispatching rule selection problem (Tables 8-9), equal weights, distinguishing coefficient 0.5. The input
            are the comparability sequences rounded to four decimal places (Table 7), so the coefficients and grades
            are compared with the tolerance of 0.0002.
        """
        body = methods.GRA()
        _, coefficients, grades = [table.data for table in
                                   body(self.dispatching, np.ones(5) / 5, np.ones(5), verbose=True).results]

        np.testing.assert_allclose([[1.0, 0.4472, 0.9996, 0.7104, 0.3503],
                                    [0.9995, 0.4428, 1.0, 0.7104, 0.3522],
                                    [0.8587, 0.4218, 0.7812, 0.583, 0.9996],
                                    [0.7573, 0.3708, 0.6714, 0.5179, 0.9998],
                                    [0.6649, 0.3886, 0.5524, 0.4153, 0.4465],
                                    [0.6853, 0.387, 0.5781, 1.0, 0.3787],
                                    [0.6258, 0.3904, 0.577, 0.7222, 0.3333],
                                    [0.7359, 1.0, 0.5897, 0.4594, 1.0],
                                    [0.3333, 0.3333, 0.3333, 0.3333, 0.35]], coefficients, atol=2e-4)
        np.testing.assert_allclose([0.7015, 0.701, 0.7288, 0.6634, 0.4936, 0.6058, 0.5298, 0.757, 0.3367], grades,
                                   atol=2e-4)
        self.assertListEqual([3, 4, 2, 5, 8, 6, 7, 1, 9], body.rank(grades).astype(int).tolist())

    def test_distinguishing_coefficient_dispatching(self):
        """ Fig. 6: only for the distinguishing coefficient 0.1 the ranks of MD, SPT and SLK change. """
        reference = methods.GRA()(self.dispatching, np.ones(5) / 5, np.ones(5))
        for zeta in (0.1, 0.3, 0.7, 0.8):
            with self.subTest(zeta=zeta):
                grades = methods.GRA(zeta=zeta)(self.dispatching, np.ones(5) / 5, np.ones(5))
                changed = rankdata(-grades) != rankdata(-reference)
                expected = [True, True, True] + [False] * 6 if zeta == 0.1 else [False] * 9
                self.assertListEqual(expected, changed.tolist())

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.GRA(zeta=0)
        with self.assertRaises(ValueError):
            methods.GRA(targets=[1, np.nan])(self.dispatching, np.ones(5) / 5, np.ones(5))
