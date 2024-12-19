import unittest
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
