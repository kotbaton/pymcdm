# Copyright (c) 2025-2026 Andrii Shekhovtsov
# Copyright (c) 2025-2026 Bartłomiej Kizielewicz

import unittest
from unittest import TestCase

import numpy as np

from pymcdm import weights


class TestEqualWeights(unittest.TestCase):
    """ Test output method without reference (no needed) """

    def test_output(self):
        matrix = np.array([[1, 2, 3, 5],
                           [2, 3, 4, 8]])

        output = [0.25, 0.25, 0.25, 0.25]
        output_method = list(weights.equal_weights(matrix))

        self.assertListEqual(output, output_method)


class TestEntropyWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Elsayed, Elsayed A., A. Shaik Dawood, and R. Karthikeyan. "Evaluating alternatives through the application of
    TOPSIS method with entropy weight." Int. J. Eng. Trends Technol 46.2 (2017): 60-66.
    """

    def test_output(self):
        matrix = np.array([[7, 312, 1891, 6613, 163],
                           [72, 88, 728, 941804, 1078],
                           [10, 252, 2594, 3466, 117471],
                           [10, 145, 980, 2371, 86329],
                           [65, 54, 350, 501, 29897],
                           [29, 48, 380, 912, 34051],
                           [7, 476, 3300, 78470, 2212],
                           [70, 87, 650, 733, 819000],
                           [4, 86, 591, 3015, 103],
                           [12, 79, 579, 3240, 96098],
                           [21, 45, 261, 1253, 453],
                           [1, 72, 530, 4333, 0.104800]])

        output = [0.104991, 0.069124, 0.071373, 0.449937, 0.304575]
        output_method = [round(weight, 6) for weight in weights.entropy_weights(matrix)]

        self.assertListEqual(output, output_method)


class TestSTDWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Jahan, A., & Edwards, K. L. (2013). Weighting of dependent and target-based criteria for optimal decision-making
     in materials selection process: Biomedical applications. Materials & Design, 49, 1000-1008.
    """

    def test_output(self):
        matrix = np.array([[0, 0, 0],
                           [0.39, 0.3, 0.77],
                           [0.17, 0.36, 0.8],
                           [0.35, 0.29, 0.93],
                           [0.3, 0.4, 0.94],
                           [0.84, 0.71, 1],
                           [1, 1, 0.99]])

        output = [0.35, 0.31, 0.34]
        output_method = [round(weight, 2) for weight in weights.standard_deviation_weights(matrix)]

        self.assertListEqual(output, output_method)


class TestMERECWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Keshavarz-Ghorabaee, M., Amiri, M., Zavadskas, E. K., Turskis, Z., & Antucheviciene, J. (2021). Determination of
    Objective Weights Using a New Method Based on the Removal Effects of Criteria (MEREC). Symmetry, 13(4), 525.
    """

    def test_output(self):
        matrix = np.array([[450, 8000, 54, 145],
                           [10, 9100, 2, 160],
                           [100, 8200, 31, 153],
                           [220, 9300, 1, 162],
                           [5, 8400, 23, 158]])

        types = np.array([1, 1, -1, -1])

        output = [0.5752, 0.0141, 0.4016, 0.0091]
        output_method = [round(weight, 4) for weight in weights.merec_weights(matrix, types)]

        self.assertListEqual(output, output_method)


class TestCRITICWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Tuş, A., & Adalı, E. A. (2019). The new combination with CRITIC and WASPAS methods for the time and attendance
    software selection problem. Opsearch, 56(2), 528-538.
    """

    def test_output(self):
        matrix = np.array([[5000, 3, 3, 4, 3, 2],
                           [680, 5, 3, 2, 2, 1],
                           [2000, 3, 2, 3, 4, 3],
                           [600, 4, 3, 1, 2, 2],
                           [800, 2, 4, 3, 3, 4]])

        output = [0.157, 0.249, 0.168, 0.121, 0.154, 0.151]
        output_method = [round(weight, 3) for weight in weights.critic_weights(matrix)]

        self.assertListEqual(output, output_method)


class TestCILOSWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Zavadskas, E. K., & Podvezko, V. (2016). Integrated determination of objective criteria weights in MCDM.
    International Journal of Information Technology & Decision Making, 15(02), 267-283.
    """

    def test_output(self):
        matrix = np.array([[3, 100, 10, 7],
                           [2.5, 80, 8, 5],
                           [1.8, 50, 20, 11],
                           [2.2, 70, 12, 9]])

        types = np.array([-1, 1, -1, 1])

        output = [0.3343, 0.2199, 0.1957, 0.2501]
        output_method = [round(weight, 4) for weight in weights.cilos_weights(matrix, types)]

        self.assertListEqual(output, output_method)


class TestIDOCRIWWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Zavadskas, E. K., & Podvezko, V. (2016). Integrated determination of objective criteria weights in MCDM.
    International Journal of Information Technology & Decision Making, 15(02), 267-283.
    """

    def test_output(self):
        matrix = np.array([[3, 100, 10, 7],
                           [2.5, 80, 8, 5],
                           [1.8, 50, 20, 11],
                           [2.2, 70, 12, 9]])

        types = np.array([-1, 1, -1, 1])

        output = [0.1658, 0.1885, 0.3545, 0.2911]
        output_method = [round(weight, 4) for weight in weights.idocriw_weights(matrix, types)]

        self.assertListEqual(output, output_method)


class TestAngleWeights(unittest.TestCase):
    """ Test output method with reference:
    [1] Shuai, D., Zongzhun, Z., Yongji, W., & Lei, L. (2012, May). A new angular method to determine the objective
    weights. In 2012 24th Chinese Control and Decision Conference (CCDC) (pp. 3889-3892). IEEE.
    """

    def test_output(self):
        matrix = np.array([[30, 30, 38, 29],
                           [19, 54, 86, 29],
                           [19, 15, 85, 29.1],
                           [68, 70, 60, 29]])

        output = [0.415, 0.3612, 0.2227, 0.0012]
        output_method = [round(weight, 4) for weight in weights.angle_weights(matrix)]

        self.assertListEqual(output, output_method)


class TestGiniWeights(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[5, 6, 7],
                           [5.5, 6.1, 8],
                           [4, 5, 9]])

        output = [0.412, 0.2562, 0.3319]
        output_method = [round(weight, 4) for weight in weights.gini_weights(matrix)]

        self.assertListEqual(output, output_method)


class TestVarianceWeights(unittest.TestCase):
    """ Test output method without reference """

    def test_output(self):
        matrix = np.array([[100, 4, 500],
                           [110, 5, 550],
                           [120, 6, 600],
                           [121, 8, 400]])

        output = [0.3761, 0.312, 0.312]
        output_method = [round(weight, 4) for weight in weights.variance_weights(matrix)]

        self.assertListEqual(output, output_method)


class TestRANCOMWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Więckowski, J., Kizielewicz, B., Shekhovtsov, A., & Sałabun, W. (2023). RANCOM: A novel approach to
        identifying criteria relevance based on inaccuracy expert judgments. Engineering Applications of Artificial
        Intelligence, 122, 106114.
    """

    def test_output(self):
        matrix = np.array([
            [0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 0.5, 0.0],
            [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        ])

        output = [0.2449, 0.2449, 0.1429, 0.0204, 0.0612, 0.1020, 0.1837]
        output_method = [round(weight, 4) for weight in weights.subjective.RANCOM(matrix=matrix)()]
        self.assertListEqual(output, output_method)

    def test_matrix_as_list(self):
        """ The matrix can be given as a list, as documented. """
        matrix = [[0.5, 1, 1, 1], [0, 0.5, 1, 1], [0, 0, 0.5, 0], [0, 0, 1, 0.5]]
        np.testing.assert_allclose(weights.subjective.RANCOM(matrix=matrix)(),
                                   weights.subjective.RANCOM(matrix=np.array(matrix))())


class TestAHPWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Wang, Y. M., & Chin, K. S. (2011). A linear programming approximation to the eigenvector method in the
        analytic hierarchy process. Information Sciences, 181(23), 5240-5248.
    """

    def test_output(self):
        matrix = np.array([
            [1, 4, 3, 1, 3, 4],
            [1/4, 1, 7, 3, 1/5, 1],
            [1/3, 1/7, 1, 1/5, 1/5, 1/6],
            [1, 1/3, 5, 1, 1, 1/3],
            [1/3, 5, 5, 1, 1, 3],
            [1/4, 1, 6, 3, 1/3, 1]
        ])
        output = [0.3208, 0.1395, 0.0348, 0.1285, 0.2374, 0.1391]
        output_method = [round(weight, 4) for weight in weights.subjective.AHP(matrix=matrix)()]
        self.assertListEqual(output, output_method)

    def test_prioritization_attribute_clears_cache(self):
        # For n = 3 both methods always coincide, so an inconsistent 4x4 matrix is needed
        matrix = np.array([
            [1, 3, 5, 1],
            [1/3, 1, 4, 1/2],
            [1/5, 1/4, 1, 1/7],
            [1, 2, 7, 1]
        ])
        ahp = weights.subjective.AHP(matrix=matrix)
        w_ev = ahp()
        ahp.prioritization = 'geometric_mean'
        w_gm = ahp()
        np.testing.assert_allclose(w_gm, weights.subjective.AHP(matrix=matrix, prioritization='geometric_mean')())
        self.assertFalse(np.allclose(w_ev, w_gm))

    def test_matrix_as_list(self):
        """ The matrix can be given as a list, as documented. """
        matrix = [[1, 3, 7, 5], [1/3, 1, 5, 3], [1/7, 1/5, 1, 1/3], [1/5, 1/3, 3, 1]]
        np.testing.assert_allclose(weights.subjective.AHP(matrix=matrix)(),
                                   weights.subjective.AHP(matrix=np.array(matrix))())

    def test_get_cr_without_matrix(self):
        ahp = weights.subjective.AHP(object_names=['A', 'B', 'C'])
        with self.assertRaises(ValueError):
            ahp.get_cr()

    def test_get_cr_too_large_matrix(self):
        ahp = weights.subjective.AHP(matrix=np.ones((16, 16)))
        with self.assertRaises(ValueError):
            ahp.get_cr()

    def test_unknown_prioritization(self):
        with self.assertRaises(ValueError):
            weights.subjective.AHP(matrix=np.ones((3, 3)), prioritization='row_sum')


class TestAHPGeometricMeanWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Wang, Y. M., Parkan, C., & Luo, Y. (2007). Priority estimation in the AHP through maximization of
        correlation coefficient. Applied Mathematical Modelling, 31(12), 2711-2718.
    """

    def test_output(self):
        matrix = np.array([
            [1, 4, 3, 1, 3, 4],
            [1/4, 1, 7, 3, 1/5, 1],
            [1/3, 1/7, 1, 1/5, 1/5, 1/6],
            [1, 1/3, 5, 1, 1, 1/3],
            [1/3, 5, 5, 1, 1, 3],
            [1/4, 1, 6, 3, 1/3, 1]
        ])
        output = [0.3160, 0.1391, 0.0360, 0.1251, 0.2360, 0.1477]
        output_method = [round(weight, 4) for weight in
                         weights.subjective.AHP(matrix=matrix, prioritization='geometric_mean')()]
        self.assertListEqual(output, output_method)

    def test_output_example_2(self):
        matrix = np.array([
            [1, 5, 3, 7, 6, 6, 1/3, 1/4],
            [1/5, 1, 1/3, 5, 3, 3, 1/5, 1/7],
            [1/3, 3, 1, 6, 3, 4, 6, 1/5],
            [1/7, 1/5, 1/6, 1, 1/3, 1/4, 1/7, 1/8],
            [1/6, 1/3, 1/3, 3, 1, 1/2, 1/5, 1/6],
            [1/6, 1/3, 1/4, 4, 2, 1, 1/5, 1/6],
            [3, 5, 1/6, 7, 5, 5, 1, 1/2],
            [4, 7, 5, 8, 6, 6, 2, 1]
        ])
        output = [0.1748, 0.0626, 0.1487, 0.0193, 0.0356, 0.0423, 0.1670, 0.3496]
        output_method = [round(weight, 4) for weight in
                         weights.subjective.AHP(matrix=matrix, prioritization='geometric_mean')()]
        self.assertListEqual(output, output_method)



class TestBWMIntervalsAndLinearModel(unittest.TestCase):
    """ Test output method with reference:
        [1] Rezaei, J. (2016). Best-worst multi-criteria decision-making method: Some properties and a linear
        model. Omega, 64, 126-130.
    """

    def test_output_consistent(self):
        """ Example 1 (Table 2): fully consistent comparisons, both models give the same unique solution. """
        output = [0.2105, 0.4211, 0.1053, 0.2105, 0.0526]
        for model in ('nonlinear', 'linear'):
            with self.subTest(model=model):
                bwm = weights.subjective.BWM(a_b=[2, 1, 4, 2, 8], a_w=[4, 8, 2, 4, 1], model=model)
                output_method = [round(weight, 4) for weight in bwm()]
                self.assertListEqual(output, output_method)
                self.assertEqual(round(bwm.get_xi(), 4), 0.0)

        lower, upper = weights.subjective.BWM(a_b=[2, 1, 4, 2, 8], a_w=[4, 8, 2, 4, 1]).get_weight_intervals()
        self.assertListEqual(output, [round(v, 4) for v in lower])
        self.assertListEqual(output, [round(v, 4) for v in upper])

    def test_output_intervals(self):
        """ Example 2 (Table 3): xi* = 0.1459 and the intervals of the optimal weights from models (5)-(6). """
        bwm = weights.subjective.BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 2, 3, 1])
        lower, upper = bwm.get_weight_intervals()

        self.assertEqual(round(bwm.get_xi(), 4), 0.1459)
        self.assertListEqual([0.2145, 0.4461, 0.1085, 0.1563, 0.0548], [round(v, 4) for v in lower])
        self.assertListEqual([0.2289, 0.4571, 0.1176, 0.1602, 0.0561], [round(v, 4) for v in upper])

    def test_output_preference_degrees(self):
        """ Example 2: matrix of degrees of preference (16); price > quality > safety > comfort > style. """
        bwm = weights.subjective.BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 2, 3, 1])
        dp = bwm.get_interval_preference_degrees()

        output = [[0.5, 0, 1, 1, 1],
                  [1, 0.5, 1, 1, 1],
                  [0, 0, 0.5, 0, 1],
                  [0, 0, 1, 0.5, 1],
                  [0, 0, 0, 0, 0.5]]
        self.assertListEqual(output, np.round(dp, 4).tolist())
        self.assertListEqual([3, 4, 1, 2, 0], (dp > 0.5).sum(axis=1).tolist())

    def test_output_intervals_overlapping(self):
        """ Example 3 (Table 4): xi* = 1, overlapping intervals and their degrees of preference;
            price > quality > comfort > safety > style.
        """
        bwm = weights.subjective.BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 4, 2, 1])
        lower, upper = bwm.get_weight_intervals()

        self.assertListEqual([0.1579, 0.4286, 0.1429, 0.1111, 0.0476], [round(v, 4) for v in lower])
        self.assertListEqual([0.2469, 0.4932, 0.1644, 0.1579, 0.0548], [round(v, 4) for v in upper])

        output = [[0.5, 0, 0.9413, 1, 1],
                  [1, 0.5, 1, 1, 1],
                  [0.0587, 0, 0.5, 0.7799, 1],
                  [0, 0, 0.2201, 0.5, 1],
                  [0, 0, 0, 0, 0.5]]
        dp = bwm.get_interval_preference_degrees()
        self.assertListEqual(output, np.round(dp, 4).tolist())
        self.assertListEqual([3, 4, 2, 1, 0], (dp > 0.5).sum(axis=1).tolist())

    def test_output_linear(self):
        """ Example 2 of Section 4.1: unique solution of the linear model (19). """
        bwm = weights.subjective.BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 2, 3, 1], model='linear')

        output = [0.2295, 0.4481, 0.1148, 0.153, 0.0546]
        output_method = [round(weight, 4) for weight in bwm()]
        self.assertListEqual(output, output_method)
        self.assertEqual(round(bwm.get_xi(), 4), 0.0109)

    def test_model_change(self):
        """ Changing the model clears the cached weights; intervals are defined for the nonlinear model only. """
        bwm = weights.subjective.BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 2, 3, 1])
        bwm()
        bwm.model = 'linear'

        self.assertEqual(round(bwm()[0], 4), 0.2295)
        with self.assertRaises(ValueError):
            bwm.get_weight_intervals()
        with self.assertRaises(ValueError):
            bwm.model = 'quadratic'


class TestSWARAWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Keršulienė, V., Zavadskas, E. K., & Turskis, Z. (2010). Selection of rational dispute resolution method
        by applying new step-wise weight assessment ratio analysis (SWARA). Journal of Business Economics and
        Management, 11(2), 243-258.
    """

    def test_output(self):
        """ Weights of the dispute resolution attributes from Table 1. """
        swara = weights.subjective.SWARA(s=[0, 1, 2, 3, 4, 5], s_v=[0.15, 0.04, 0.29, 0.02, 0.04])

        output = [0.22, 0.19, 0.18, 0.14, 0.14, 0.13]
        output_method = [round(weight, 2) for weight in swara()]
        self.assertListEqual(output, output_method)

    def test_order_with_gaps(self):
        """ Every criterion has to be in the ordering, otherwise it would silently get a zero weight. """
        with self.assertRaises(ValueError):
            weights.subjective.SWARA(s=[0, 2], s_v=[0.1])
        with self.assertRaises(ValueError):
            weights.subjective.SWARA(s=[1, 2], s_v=[0.1])


class TestPIPRECIAWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Stanujkić, D., Karabašević, D., Popović, G., & Sava, C. (2021). Simplified pivot pairwise relative
        criteria importance assessment (PIPRECIA-S) method. Romanian Journal of Economic Forecasting, 24(4),
        141-154.
    """

    def test_output(self):
        """ Weights obtained using the PIPRECIA method from Table 2. """
        piprecia = weights.subjective.PIPRECIA(s=[0, 1, 2, 3], s_v=[1.0, 0.5, 0.5])

        output = [0.32, 0.32, 0.21, 0.14]
        output_method = [round(weight, 2) for weight in piprecia()]
        self.assertListEqual(output, output_method)

    def test_output_simplified(self):
        """ Weights obtained using the Simplified PIPRECIA method from Table 3. """
        piprecia = weights.subjective.PIPRECIA(s=[0, 1, 2, 3], s_v=[1.0, 0.5, 0.25], comparison='first')

        output = [0.31, 0.31, 0.21, 0.18]
        output_method = [round(weight, 2) for weight in piprecia()]
        self.assertListEqual(output, output_method)

    def test_output_simplified_websites(self):
        """ Weights of the winery website criteria obtained using the Simplified PIPRECIA method from Table 4. """
        piprecia = weights.subjective.PIPRECIA(s=[0, 1, 2, 3, 4], s_v=[0.9, 0.8, 0.65, 0.6], comparison='first')

        output = [0.24, 0.22, 0.2, 0.18, 0.17]
        output_method = [round(weight, 2) for weight in piprecia()]
        self.assertListEqual(output, output_method)

    def test_comparison_change(self):
        """ Changing the comparison clears the cached weights. """
        piprecia = weights.subjective.PIPRECIA(s=[0, 1, 2, 3], s_v=[1.0, 0.5, 0.25])
        piprecia()
        piprecia.comparison = 'first'

        output = [0.31, 0.31, 0.21, 0.18]
        output_method = [round(weight, 2) for weight in piprecia()]
        self.assertListEqual(output, output_method)
        with self.assertRaises(ValueError):
            piprecia.comparison = 'last'


class TestFUCOMWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Pamučar, D., Stević, Ž., & Sremac, S. (2018). A new model for determining weight coefficients of
        criteria in MCDM models: Full Consistency Method (FUCOM). Symmetry, 10(9), 393.
    """

    def test_output(self):
        """ Example 1: comparative priorities given directly (Step 2a, Table 1). """
        fucom = weights.subjective.FUCOM(o=[0, 1, 2, 3], i=[1.08, 1.25, 1.45])

        output = [0.315, 0.291, 0.233, 0.161]
        output_method = [round(weight, 3) for weight in fucom()]
        self.assertListEqual(output, output_method)
        self.assertEqual(round(fucom.dfc, 2), 0.0)

    def test_output_significance(self):
        """ Example 2: ranking C2 > C1 > C4 > C3 > C5 and significance scores (Step 2b, Table 2).
            The exact solution gives w2 = 0.4375 and w5 = 0.0625, which the paper prints as 0.437 and 0.063,
            so the weights are compared with two decimals.
        """
        fucom = weights.subjective.FUCOM(o=[1, 0, 3, 2, 4], v=[1, 2.1, 3, 3, 7])

        output = [0.21, 0.44, 0.15, 0.15, 0.06]
        output_method = [round(weight, 2) for weight in fucom()]
        self.assertListEqual(output, output_method)

    def test_output_ties(self):
        """ Example 3: eight criteria with ties, C3 = C5 = C7 > C1 > C2 = C4 = C6 = C8 (Tables 5 and 6). """
        fucom = weights.subjective.FUCOM(o=[2, 4, 6, 0, 1, 3, 5, 7], v=[1, 1, 1, 2, 4, 4, 4, 4])

        output = [0.1111, 0.0556, 0.2222, 0.0556, 0.2222, 0.0556, 0.2222, 0.0556]
        output_method = [round(weight, 4) for weight in fucom()]
        self.assertListEqual(output, output_method)


class TestBWMWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Rezaei, J. (2015). Best-worst multi-criteria decision-making method. Omega, 53, 49-57.
    """

    def test_output(self):
        """ Example 1: transportation mode, C3 is the best and C1 the worst criterion. """
        bwm = weights.subjective.BWM(a_b=[8, 2, 1], a_w=[1, 5, 8])

        output = [0.0714, 0.3387, 0.5899]
        output_method = [round(weight, 4) for weight in bwm()]
        self.assertListEqual(output, output_method)
        self.assertEqual(round(bwm.get_xi(), 2), 0.26)

    def test_output_multiple_optima(self):
        """ Example 3 of Rezaei, J. (2016). Best-worst multi-criteria decision-making method: Some properties
            and a linear model. Omega, 64, 126-130 (Table 4): five criteria with multiple optimal solutions.
            The weights must be optimal (xi* = 1) and lie within the intervals obtained with models (5) and (6).
        """
        bwm = weights.subjective.BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 4, 2, 1])
        w = bwm()

        self.assertEqual(round(bwm.get_xi(), 4), 1.0)
        lower = [0.1579, 0.4286, 0.1429, 0.1111, 0.0476]
        upper = [0.2469, 0.4932, 0.1644, 0.1579, 0.0548]
        for weight, lo, up in zip(w, lower, upper):
            self.assertTrue(lo - 1e-4 <= weight <= up + 1e-4)

    def test_output_all_combinations(self):
        """ Example 2 (Table 5): xi and weights for a_32, a_21 in {1, ..., 8} with a_31 = 8.
            Rows are a_21, columns are a_32. The table includes inputs with two criteria
            equal to the best one (a_32 = 1). Weights are rounded to two decimals in the paper,
            hence the tolerance.
        """
        xi = np.array([
            [1.54, 1.16, 0.85, 0.61, 0.41, 0.24, 0.11, 0.00],
            [1.16, 0.70, 0.32, 0.00, 0.26, 0.47, 0.64, 0.78],
            [0.85, 0.32, 0.15, 0.54, 0.86, 1.13, 1.35, 1.53],
            [0.61, 0.00, 0.54, 1.00, 1.39, 1.73, 2.00, 2.23],
            [0.41, 0.26, 0.86, 1.39, 1.86, 2.26, 2.59, 2.88],
            [0.24, 0.47, 1.13, 1.73, 2.26, 2.73, 3.13, 3.47],
            [0.11, 0.64, 1.35, 2.00, 2.59, 3.13, 3.59, 4.00],
            [0.00, 0.78, 1.53, 2.23, 2.88, 3.47, 4.00, 4.47],
        ])
        w1 = np.array([
            [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
            [0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09],
            [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08],
            [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08],
            [0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07],
            [0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07],
            [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06],
            [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06],
        ])
        w2 = np.array([
            [0.25, 0.22, 0.19, 0.16, 0.14, 0.12, 0.11, 0.10],
            [0.29, 0.25, 0.21, 0.18, 0.16, 0.14, 0.12, 0.11],
            [0.32, 0.28, 0.24, 0.21, 0.18, 0.16, 0.14, 0.12],
            [0.35, 0.31, 0.27, 0.23, 0.20, 0.17, 0.15, 0.14],
            [0.39, 0.34, 0.30, 0.26, 0.22, 0.20, 0.17, 0.15],
            [0.42, 0.37, 0.32, 0.28, 0.25, 0.22, 0.19, 0.17],
            [0.44, 0.40, 0.35, 0.31, 0.28, 0.24, 0.21, 0.19],
            [0.47, 0.42, 0.38, 0.34, 0.30, 0.27, 0.24, 0.21],
        ])
        w3 = np.array([
            [0.65, 0.68, 0.71, 0.74, 0.76, 0.78, 0.79, 0.80],
            [0.62, 0.66, 0.70, 0.73, 0.75, 0.77, 0.79, 0.80],
            [0.60, 0.64, 0.68, 0.71, 0.74, 0.76, 0.78, 0.79],
            [0.57, 0.62, 0.66, 0.69, 0.72, 0.75, 0.77, 0.79],
            [0.54, 0.59, 0.63, 0.67, 0.70, 0.73, 0.76, 0.78],
            [0.52, 0.56, 0.61, 0.65, 0.68, 0.72, 0.74, 0.76],
            [0.49, 0.54, 0.58, 0.62, 0.66, 0.70, 0.72, 0.75],
            [0.47, 0.52, 0.56, 0.60, 0.64, 0.67, 0.71, 0.73],
        ])
        for a21 in range(1, 9):
            for a32 in range(1, 9):
                with self.subTest(a21=a21, a32=a32):
                    bwm = weights.subjective.BWM(a_b=[8, a32, 1], a_w=[1, a21, 8])
                    output = [xi[a21 - 1, a32 - 1], w1[a21 - 1, a32 - 1], w2[a21 - 1, a32 - 1], w3[a21 - 1, a32 - 1]]
                    output_method = [bwm.get_xi(), *bwm()]
                    np.testing.assert_allclose(output_method, output, atol=0.0051)


class TestBCMWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Haseli, G., Sheikh, R., & Sana, S. S. (2020). Base-criterion on multi-criteria decision-making method and
        its applications. International Journal of Management Science and Engineering Management, 15(2), 79-88.
    """

    def test_output(self):
        """ Example 1: transportation mode selection, cost (C3) is the base-criterion (Table 1). """
        bcm = weights.subjective.BCM(a_b=[8, 2, 1])

        output = [0.0769, 0.3077, 0.6154]
        output_method = [round(weight, 4) for weight in bcm()]
        self.assertListEqual(output, output_method)
        self.assertEqual(round(bcm.get_xi(), 4), 0.0)

    def test_output_full_matrix(self):
        """ Example 1: complete pairwise comparison matrix, e.g. a21 = 4 (Table 2). """
        bcm = weights.subjective.BCM(a_b=[8, 2, 1])

        output = [[1, 0.25, 0.125], [4, 1, 0.5], [8, 2, 1]]
        output_method = np.round(bcm.get_full_matrix(), 4).tolist()
        self.assertListEqual(output, output_method)

    def test_output_car(self):
        """ Example 2: car selection, safety (C) is the base-criterion (Tables 3 and 4). """
        bcm = weights.subjective.BCM(a_b=[1, 1 / 3, 1, 2, 1 / 2, 1 / 4], base_index=2)

        output = [0.0870, 0.2609, 0.0870, 0.0435, 0.1739, 0.3478]
        output_method = [round(weight, 4) for weight in bcm()]
        self.assertListEqual(output, output_method)
        self.assertEqual(round(bcm.get_xi(), 4), 0.0)

        output = [[1, 0.3333, 1, 2, 0.5, 0.25],
                  [3, 1, 3, 6, 1.5, 0.75],
                  [1, 0.3333, 1, 2, 0.5, 0.25],
                  [0.5, 0.1667, 0.5, 1, 0.25, 0.125],
                  [2, 0.6667, 2, 4, 1, 0.5],
                  [4, 1.3333, 4, 8, 2, 1]]
        output_method = np.round(bcm.get_full_matrix(), 4).tolist()
        self.assertListEqual(output, output_method)


class TestVIMMWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Zakeri, S., Ecer, F., Konstantas, D., & Cheikhrouhou, N. (2023). The vital-immaterial-mediocre
        multi-criteria decision-making method. Kybernetes, 52(3), 937-963.
    """

    def setUp(self):
        # Criteria: cost, quality, delivery, service, social responsibility, risk, agility (Example 1)
        self.vimm = weights.subjective.VIMM(n_criteria=7, vital_index=0, immaterial_index=4,
                                            c_vital=[[9, 7.5, 8, 6.5, 7], [8, 8.5, 7]],
                                            c_immaterial=[[9, 8, 8.5, 6, 7.5], [8.5, 9, 8]])

    def test_output(self):
        """ Weights of the supplier selection criteria from Table 11. """
        output = [0.286, 0.243, 0.186, 0.192, 0.014, 0.027, 0.05]
        output_method = [round(weight, 3) for weight in self.vimm()]
        self.assertListEqual(output, output_method)

    def test_output_scores(self):
        """ Scores of the criteria from Table 11. The score of delivery is 12.9625, which the paper rounds up to
            12.963 and Python's round down to 12.962, so the scores are compared with two decimals.
        """
        output = [20.0, 17.0, 12.96, 13.44, 1.0, 1.91, 3.52]
        output_method = [round(score, 2) for score in self.vimm.get_scores()]
        self.assertListEqual(output, output_method)

    def test_tied_scores(self):
        """ When all remaining criteria have the same score, a vital and an immaterial criterion cannot be chosen. """
        vimm = weights.subjective.VIMM(n_criteria=6, vital_index=0, immaterial_index=1,
                                       c_vital=[[5, 5, 5, 5], [6, 7]], c_immaterial=[[5, 5, 5, 5], [6, 7]])
        with self.assertRaises(ValueError):
            vimm()


class TestOWCMWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Ahmed Mandil, A. D., Salih, M. M., & Muhsen, Y. R. (2024). Opinion Weight Criteria Method (OWCM): A New
        Method for Weighting Criteria With Zero Inconsistency. IEEE Access, 12, 5605-5616.
    """

    def test_output(self):
        """ Machine learning methods for COVID-19 classification from Table 6. The crisp matrix of Table 4 gives
            Train time of Neural Network as 1, but the opinion matrix (Table 3) gives H_D, i.e. 5, which is also
            the value used in Table 5 (normalized value 1) and in the mean of Train time (0.575).
        """
        matrix = np.array([
            [5, 4, 1, 1, 1, 1, 1, 2, 1],
            [4, 5, 1, 2, 2, 2, 2, 1, 2],
            [2, 4, 2, 2, 3, 2, 3, 2, 3],
            [1, 5, 2, 3, 4, 3, 4, 3, 3],
            [3, 4, 2, 3, 4, 3, 4, 2, 3],
            [2, 4, 3, 4, 5, 4, 5, 5, 4],
            [3, 1, 5, 4, 5, 4, 5, 4, 4],
            [3, 3, 5, 5, 5, 5, 5, 5, 5],
        ])
        owcm = weights.subjective.OWCM(M=matrix)

        output = [0.1383109, 0.1321909, 0.0697674, 0.127295, 0.0893513, 0.127295, 0.0893513, 0.0881273, 0.1383109]
        output_method = [round(weight, 7) for weight in owcm()]
        self.assertListEqual(output, output_method)


class TestLBWAWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Žižović, M., & Pamučar, D. (2019). New model for determining criteria weights: Level Based Weight
        Assessment (LBWA) model. Decision Making: Applications in Management and Engineering, 2(2), 126-137.
    """

    def test_output(self):
        """ Example 1: criteria for the evaluation of level crossings, r0 = 7. """
        lbwa = weights.subjective.LBWA(i=[[1, 4, 6, 5, 0, 2], [7, 3]], l=[0, 2, 3, 4, 4, 5, 1, 2], r0=7)

        output = [0.121, 0.191, 0.111, 0.084, 0.148, 0.121, 0.134, 0.089]
        output_method = [round(weight, 3) for weight in lbwa()]
        self.assertListEqual(output, output_method)

    def test_output_empty_levels(self):
        """ Example 2: advisors in the transport of dangerous goods, levels S3, S5 and S6 are empty, r0 = 5.
            The final vector in the paper gives w2 with two decimals (0.03); Step 6 gives 0.031.
        """
        lbwa = weights.subjective.LBWA(i=[[4, 7, 8, 0], [2, 3], [], [5], [], [], [1, 6]],
                                       l=[0, 1, 2, 4, 1, 2, 2, 1, 3], r0=5)

        output = [0.124, 0.031, 0.102, 0.093, 0.224, 0.051, 0.029, 0.186, 0.16]
        output_method = [round(weight, 3) for weight in lbwa()]
        self.assertListEqual(output, output_method)


class TestSIMOSWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Figueira, J., & Roy, B. (2002). Determining the weights of criteria in the ELECTRE type methods with
        a revised Simos' procedure. European Journal of Operational Research, 139(2), 317-326.
    """

    def test_output(self):
        """ Normalized weights before rounding from Table 2, criteria a, ..., l are 0, ..., 11. """
        simos = weights.subjective.SIMOS(r=[[2, 6, 11], [3], [1, 5, 8, 9], [4], [0, 7], [10]], w_c=[0, 1, 0, 0, 0])

        output = [13.372, 8.721, 2.326, 4.651, 11.628, 8.721, 2.326, 13.372, 8.721, 8.721, 15.116, 2.326]
        output_method = [round(100 * weight, 3) for weight in simos()]
        self.assertListEqual(output, output_method)

    def test_output_subfamily(self):
        """ Subfamily of Table 3: criteria c, g, l, d, b, f, i, j are 0, ..., 7. """
        simos = weights.subjective.SIMOS(r=[[0, 1, 2], [3], [4, 5, 6, 7]], w_c=[0, 1])

        output = [5.0, 5.0, 5.0, 10.0, 18.75, 18.75, 18.75, 18.75]
        output_method = [round(100 * weight, 3) for weight in simos()]
        self.assertListEqual(output, output_method)


class TestSRFWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Figueira, J., & Roy, B. (2002). Determining the weights of criteria in the ELECTRE type methods with
        a revised Simos' procedure. European Journal of Operational Research, 139(2), 317-326.
    """

    def test_output(self):
        """ Normalized weights for w = 1 and z = 6.5 from Table 5, criteria a, ..., l are 0, ..., 11. """
        srf = weights.subjective.SRF(r=[[2, 6, 11], [3], [1, 5, 8, 9], [4], [0, 7], [10]], w_c=[0, 1, 0, 0, 0],
                                     z=6.5, w=1)

        output = [13.2, 8.9, 2.4, 4.5, 11.0, 8.9, 2.4, 13.2, 8.9, 8.9, 15.3, 2.4]
        output_method = [round(100 * weight, 1) for weight in srf()]
        self.assertListEqual(output, output_method)
        self.assertAlmostEqual(sum(output_method), 100.0)

    def test_rounding_ties(self):
        """ When only a part of an ex aequo subset is rounded up, the criteria with the higher subscripts are
            selected (Section 3.2.2). Here two of the three criteria of the first subset are rounded up.
        """
        srf = weights.subjective.SRF(r=[[0, 1, 2], [3], [4]], w_c=[1, 0], z=1.5, w=1)

        output = [17.1, 17.2, 17.2, 22.8, 25.7]
        output_method = [round(100 * weight, 1) for weight in srf()]
        self.assertListEqual(output, output_method)


class TestCOBRACWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Pamucar, D., Simic, V., Gorcun, O. F., & Kucukonder, H. (2024). Selection of the best Big Data platform
        using COBRAC-ARTASI methodology with adaptive standardized intervals. Expert Systems with Applications,
        239, 122312.
    """

    criteria = ['C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C21', 'C22', 'C23', 'C31', 'C32', 'C41', 'C42',
                'C43', 'C51', 'C52', 'C53', 'C54', 'C55', 'C56', 'C57', 'C61', 'C62', 'C71', 'C72', 'C73', 'C74',
                'C81', 'C82']
    ranking = ['C11', 'C12', 'C21', 'C71', 'C13', 'C72', 'C14', 'C31', 'C51', 'C52', 'C22', 'C61', 'C23', 'C41',
               'C15', 'C32', 'C42', 'C62', 'C73', 'C16', 'C53', 'C74', 'C43', 'C17', 'C54', 'C55', 'C56', 'C57',
               'C81', 'C82']
    xis = [0.53, 0.50, 0.58, 0.55, 0.50, 0.54, 0.50, 0.50, 0.50, 0.60, 0.50, 0.55, 0.50, 0.60, 0.51, 0.51, 0.52,
           0.52, 0.62, 0.53, 0.56, 0.64, 0.61, 0.68, 0.52, 0.58, 0.59, 0.55, 0.65]

    def test_output(self):
        """ Comparisons of adjacently ranked sub-criteria from Table 6. The paper reports the weights only as
            a bar chart (Fig. 2), so the test checks that all relations (2) hold exactly (delta = 0), that C11,
            C12 and C21 have the highest and C81 and C82 the lowest weights, as stated in the paper.
        """
        idx = {c: i for i, c in enumerate(self.criteria)}
        pairs = [(idx[a], idx[b]) for a, b in zip(self.ranking, self.ranking[1:])]
        cobrac = weights.subjective.COBRAC(n_criteria=30, pairs=pairs, xis=self.xis)
        w = cobrac()

        self.assertAlmostEqual(cobrac.get_delta(), 0.0, places=8)
        self.assertAlmostEqual(w.sum(), 1.0)
        for (i, j), xi in zip(pairs, self.xis):
            self.assertAlmostEqual(w[i] / w[j], xi / (1 - xi), places=8)

        order = [self.criteria[i] for i in np.argsort(-w, kind='stable')]
        self.assertSetEqual(set(order[:3]), {'C11', 'C12', 'C21'})
        self.assertSetEqual(set(order[-2:]), {'C81', 'C82'})

    def test_output_inconsistent(self):
        """ Additional non-adjacent comparison makes the comparisons inconsistent: the optimal delta is the
            largest deviation of the returned weights.
        """
        cobrac = weights.subjective.COBRAC(n_criteria=3, pairs=[(0, 1), (1, 2), (0, 2)], xis=[0.7, 0.6, 0.6])
        w = cobrac()
        ratios = [w[0] / w[1] - 7 / 3, w[1] / w[2] - 1.5, w[0] / w[2] - 1.5]

        self.assertAlmostEqual(cobrac.get_delta(), max(abs(r) for r in ratios))
        self.assertEqual(round(cobrac.get_delta(), 3), 0.457)


class TestITARAWeights(unittest.TestCase):
    """ Test output method with reference:
        [1] Hatefi, M. A. (2019). Indifference threshold-based attribute ratio analysis: A method for assigning the
        weights to the attributes in multiple attribute decision making. Applied Soft Computing, 74, 643-651.
    """

    def test_output(self):
        """ Location selection in banking with p = 1 from Table 1. """
        matrix = np.array([
            [7400000, 98.4, 73.1, 50800, 4.1, 90.1, 2.4, 20.4, 393, 10.6, 3.5],
            [33500000, 78.2, 66.5, 144600, 4.1, 84, 6.4, 10.1, 347, 8, 1.83],
            [10850000, 96, 61.4, 255000, 4, 75.6, 1.1, 10.4, 275, 6.3, 7.52],
            [29200, 86.6, 82.3, 657000, 5.6, 89.3, 4.6, 21.4, 150, 12.9, 3.99],
        ])
        itara = weights.subjective.ITARA(t=[1000000, 10, 10, 50000, 0, 0, 2, 7, 50, 2, 3], p=1)

        output = [0.441, 0.0, 0.0, 0.309, 0.067, 0.032, 0.01, 0.036, 0.062, 0.018, 0.024]
        output_method = [round(weight, 3) for weight in itara(matrix)]
        self.assertListEqual(output, output_method)


class TestLOPCOWWeights(unittest.TestCase):
    """ Test output method with reference:

        [1] Ecer, F., & Pamucar, D. (2022). A novel LOPCOW‐DOBI multi‐criteria sustainability performance
        assessment methodology: An application in developing country banking sector. Omega, 112, 102690.
    """
    def test_output(self):
            matrix = np.array([
                # A1
                [21.8, 14.1, 10.7, 1.6, 1.8, 770, 12750, 18, 5100, 1.5, 9.1, 1.054, 4.196, 29.407, 7.03, 15.08, 9.705],
                # A2
                [16.4, 8.5, 13.9, 1.2, 1.3, 524, 12087, 5.7, 2941, 2.208, 15.2, 1.123, 3.86, 5.228, 14.724, 32.103, 19.0],
                # A3
                [14.5, 7.0, 2.3, 0.2, 0.2, 238, 3265, 1.9, 320, 2.32, 16.202, 1.008, 3.095, 5.549, 17.34, 65.129, 32.056],
                # A4
                [18.2, 10.3, 11.4, 1.2, 1.1, 835, 16037, 21.3, 4332, 0.875, 9.484, 0.856, 2.191, 23.75, 13.1, 58.157, 27.46],
                # A5
                [18.5, 8.1, 11.1, 1.0, 1.1, 504, 9464, 1.4, 1743, 2.95, 0.7, 0.479, 2.44, 8.77, 13.48, 33.45, 17.68],
                # A6
                [18.7, 11.4, 10.8, 1.3, 1.5, 1227, 24053, 20.0, 6521, 0.733, 1.6, 0.857, 2.377, 4.985, 11.743, 26.732, 24.485],
                # A7
                [18.5, 12.6, 10.8, 1.4, 1.8, 912, 18800, 18.2, 5300, 1.29, 8.27, 0.558, 0.635, 5.22, 13.829, 31.914, 7.515],
                # A8
                [16.4, 6.7, 12.6, 0.9, 0.9, 951, 16767, 22.0, 3917, 2.46, 3.9, 0.724, 0.568, 4.491, 14.357, 28.869, 7.313],
                # A9
                [15.2, 6.3, 6.9, 0.5, 0.5, 1013, 20170, 10.97, 4060, 1.67, 1.7, 0.704, 2.96, 3.24, 10.029, 60.981, 23.541],
            ], dtype=float)

            # Criteria types: 1 for profit (Max), -1 for cost (Min)
            # From the prompt: first 10 criteria are Max, last 7 are Min
            types = np.array([1] * 10 + [-1] * 7, dtype=int)

            # Compute LOPCOW weights
            w = np.round(weights.lopcow_weights(matrix, types), 4)

            expected = [0.0495, 0.0366, 0.0846, 0.0706, 0.0637, 0.0661, 0.0699, 0.0504, 0.0690, 0.0492, 0.0556,
                        0.0487, 0.0482, 0.0763, 0.0551, 0.0532, 0.0534]

            self.assertListEqual(list(w), expected)
