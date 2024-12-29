# Copyright (c) 2023 Andrii Shekhovtsov
# Copyright (c) 2022 Bartłomiej Kizielewicz

import unittest
import numpy as np

from pymcdm import methods
from pymcdm.methods.mcda_method import MCDA_method
from pymcdm.methods.comet_tools import MethodExpert


class TestMCDA(unittest.TestCase):

    def test_validation(self):
        with self.assertRaises(ValueError):
            body = methods.TOPSIS()
            matrix = np.array([[1, 2, 3], [1, 2, 3]])
            weights = np.array([0.5, 0.5])
            types = np.array([1, -1, -1])
            body(matrix=matrix, weights=weights, types=types)


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


class TestCOCOSO(unittest.TestCase):
    """ Test output method with reference:
    [1] Yazdani, M., Zarate, P., Zavadskas, E. K., & Turskis, Z. (2019). A
    Combined Compromise Solution (CoCoSo) method for multi-criteria decision-making problems. Management Decision.
    """

    def test_output(self):
        body = methods.COCOSO()
        matrix = np.array([[60, 0.4, 2540, 500, 990],
                           [6.35, 0.15, 1016, 3000, 1041],
                           [6.8, 0.1, 1727.2, 1500, 1676],
                           [10, 0.2, 1000, 2000, 965],
                           [2.5, 0.1, 560, 500, 915],
                           [4.5, 0.08, 1016, 350, 508],
                           [3, 0.1, 1778, 1000, 920]])

        weights = np.array([0.036, 0.192, 0.326, 0.326, 0.12])
        types = np.array([1, -1, 1, 1, 1])

        output = [2.041, 2.788, 2.882, 2.416, 1.299, 1.443, 2.519]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestCODAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Badi, I., Shetwan, A. G., & Abdulshahed, A. M. (2017, September).
    Supplier selection using COmbinative Distance-based ASsessment (CODAS) method for multi-criteria decision-making.
    In Proceedings of The 1st International Conference on Management, Engineering and Environment (ICMNEE) (pp.
    395-407).
    """

    def test_output(self):
        body = methods.CODAS()
        matrix = np.array([[45, 3600, 45, 0.9],
                           [25, 3800, 60, 0.8],
                           [23, 3100, 35, 0.9],
                           [14, 3400, 50, 0.7],
                           [15, 3300, 40, 0.8],
                           [28, 3000, 30, 0.6]])

        types = np.array([1, -1, 1, 1])
        weights = np.array([0.2857, 0.3036, 0.2321, 0.1786])

        output = [1.3914, 0.3411, -0.2170, -0.5381, -0.7292, -0.2481]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestCOMET(unittest.TestCase):
    """ Test output method with reference:
    [1] Paradowski, B., Bączkiewicz, A., & Watrąbski, J. (2021). Towards
    proper consumer choices-MCDM based product selection. Procedia Computer Science, 192, 1347-1358.
    """

    def test_output(self):
        matrix = np.array([[64, 128, 2.9, 4.3, 3.2, 280, 495, 24763, 3990],
                           [28, 56, 3.1, 3.8, 3.8, 255, 417, 12975, 2999],
                           [8, 16, 3.5, 5.3, 4.8, 125, 636, 5725, 539],
                           [12, 24, 3.7, 4.8, 4.5, 105, 637, 8468, 549],
                           [10, 20, 3.7, 5.3, 4.9, 125, 539, 6399, 499],
                           [8, 16, 3.6, 4.4, 4.0, 65, 501, 4834, 329],
                           [6, 12, 3.7, 4.6, 4.2, 65, 604, 4562, 299],
                           [16, 32, 3.4, 4.9, 4.2, 105, 647, 10428, 799],
                           [8, 16, 3.6, 5.0, 4.5, 125, 609, 5615, 399],
                           [18, 36, 3.0, 4.8, 4.3, 165, 480, 8848, 979],
                           [24, 48, 3.8, 4.5, 4.0, 280, 509, 13552, 1399],
                           [28, 56, 2.5, 3.8, 2.8, 205, 376, 8585, 10000]])

        cvalues = np.vstack((
            np.min(matrix, axis=0),
            np.max(matrix, axis=0)
        )).T

        types = np.array([1, 1, 1, 1, 1, -1, 1, 1, -1])
        weights = np.array([1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9])

        body = methods.COMET(cvalues, MethodExpert(methods.TOPSIS(), weights, types))

        output = [0.5433, 0.3447, 0.6115, 0.6168, 0.6060, 0.4842, 0.5516, 0.6100, 0.5719, 0.4711, 0.4979, 0.1452]
        output_method = [round(preference, 4) for preference in body(matrix)]

        self.assertListEqual(output, output_method)


class TestCOPRAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Zavadskas, E. K., Kaklauskas, A., Peldschus, F., & Turskis, Z. (2007).
    Multi-attribute assessment of road design solutions by using the COPRAS
    method. The Baltic journal of Road and Bridge engineering, 2(4), 195-203.
    """

    def test_output(self):
        body = methods.COPRAS()

        # The alternatives are in columns in the referenced paper,
        # so we transpose the matrix to fit the pymcdm input format.
        matrix = np.array([
                [30, 20, 27, 18, 24, 16],
                [12.487, 12.372, 11.096, 10.982, 11.017, 10.903],
                [6.261, 5.961, 6.262, 5.962, 6.283, 5.983],
                [10.880, 10.880, 9.920, 9.920, 9.980, 9.980],
                [7.610, 7.460, 6.690, 6.540, 7.000, 6.850]
            ]).T

        types = np.array([1, -1, -1, -1, -1])
        weights = np.array([0.5300, 0.1175, 0.1175, 0.1175, 0.1175])

        output = [1.0, 0.797, 0.9078, 0.7243, 0.8537, 0.6898]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestCOPRAS2(unittest.TestCase):
    """ Test output method with reference:
    [1] Zavadskas, E. K., Kaklauskas, A., Peldschus, F., & Turskis, Z. (2007).
    Multi-attribute assessment of road design solutions by using the COPRAS
    method. The Baltic journal of Road and Bridge engineering, 2(4), 195-203.
    """

    def test_output(self):
        body = methods.COPRAS()

        # The alternatives are in columns in the referenced paper,
        # so we transpose the matrix to fit the pymcdm input format.
        matrix = np.array([
                [30, 20, 27, 18, 24, 16],
                [12.487, 12.372, 11.096, 10.982, 11.017, 10.903],
                [6.261, 5.961, 6.262, 5.962, 6.283, 5.983],
                [10.880, 10.880, 9.920, 9.920, 9.980, 9.980],
                [7.610, 7.460, 6.690, 6.540, 7.000, 6.850]
            ]).T

        types = np.array([1, -1, -1, -1, -1])
        weights = np.array([0.075, 0.700, 0.075, 0.075, 0.075])

        output = [1.0, 0.9585, 0.8984, 0.86, 0.8886, 0.8532]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)

class TestEDAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Yazdani, M., Torkayesh, A. E., Santibanez-Gonzalez, E. D.,
    & Otaghsara, S. K. (2020). Evaluation of renewable energy resources using integrated Shannon Entropy—EDAS model.
    Sustainable Operations and Computers, 1, 35-42.
    """

    def test_output(self):
        body = methods.EDAS()
        matrix = np.array([[3873, 39.55, 0.27, 0.87, 150, 0.07, 12, 2130],
                           [5067, 67.26, 0.23, 0.23, 40, 0.02, 21, 2200],
                           [2213, 24.69, 0.08, 0.17, 200, 0.04, 35, 570],
                           [6243, 132, 0.07, 0.25, 100, 0.04, 16, 100],
                           [8312, 460.47, 0.05, 0.21, 25, 0.1, 25, 200]])

        weights = np.array([0.131, 0.113, 0.126, 0.125, 0.126, 0.129, 0.132, 0.117])
        types = np.array([-1, -1, -1, 1, 1, -1, 1, 1])

        output = [0.841, 0.632, 0.883, 0.457, 0.104]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestMABAC(unittest.TestCase):
    """ Test output method with reference:
    [1] Pamučar, D., & Ćirović, G. (2015). The selection of transport and
    handling resources in logistics centers using Multi-Attributive Border Approximation area Comparison (MABAC).
    Expert systems with applications, 42(6), 3016-3028.
    """

    def test_output(self):
        body = methods.MABAC()
        matrix = np.array([[22600, 3800, 2, 5, 1.06, 3.00, 3.5, 2.8, 24.5, 6.5],
                           [19500, 4200, 3, 2, 0.95, 3.00, 3.4, 2.2, 24, 7.0],
                           [21700, 4000, 1, 3, 1.25, 3.20, 3.3, 2.5, 24.5, 7.3],
                           [20600, 3800, 2, 5, 1.05, 3.25, 3.2, 2.0, 22.5, 11.0],
                           [22500, 3800, 4, 3, 1.35, 3.20, 3.7, 2.1, 23, 6.3],
                           [23250, 4210, 3, 5, 1.45, 3.60, 3.5, 2.8, 23.5, 7.0],
                           [20300, 3850, 2, 5, 0.90, 3.25, 3.0, 2.6, 21.5, 6.0]])

        weights = np.array([0.146, 0.144, 0.119, 0.121, 0.115, 0.101, 0.088, 0.068, 0.050, 0.048])
        types = np.array([-1, 1, 1, 1, -1, -1, 1, 1, 1, 1])

        output = [0.0826, 0.2183, -0.0488, 0.0246, -0.0704, 0.0465, 0.0464]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestMAIRCA(unittest.TestCase):
    """ Test output method with reference:
    [1] Aksoy, E. (2021). An Analysis on Turkey's Merger and Acquisition
    Activities: MAIRCA Method. Gümüşhane Üniversitesi Sosyal Bilimler Enstitüsü Elektronik Dergisi, 12(1), 1-11.
    """

    def test_output(self):
        body = methods.MAIRCA()
        matrix = np.array([[70, 245, 16.4, 19],
                           [52, 246, 7.3, 22],
                           [53, 295, 10.3, 25],
                           [63, 256, 12, 8],
                           [64, 233, 5.3, 17]])
        weights = np.array([0.04744, 0.02464, 0.51357, 0.41435])
        types = np.array([1, 1, 1, 1])

        output = [0.0332, 0.1122, 0.0654, 0.1304, 0.1498]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestMARCOS(unittest.TestCase):
    """ Test output method with reference:
    [1] Ulutaş, A., Karabasevic, D., Popovic, G., Stanujkic, D., Nguyen,
    P. T., & Karaköy, Ç. (2020). Development of a novel integrated CCSD-ITARA-MARCOS decision-making approach for
    stackers selection in a logistics system. Mathematics, 8(10), 1672.
    """

    def test_output(self):
        body = methods.MARCOS()
        matrix = np.array([[660, 1000, 1600, 18, 1200],
                           [800, 1000, 1600, 24, 900],
                           [980, 1000, 2500, 24, 900],
                           [920, 1500, 1600, 24, 900],
                           [1380, 1500, 1500, 24, 1150],
                           [1230, 1000, 1600, 24, 1150],
                           [680, 1500, 1600, 18, 1100],
                           [960, 2000, 1600, 12, 1150]])

        weights = np.array([0.1061, 0.3476, 0.3330, 0.1185, 0.0949])
        types = np.array([-1, 1, 1, 1, 1])

        output = [0.5649, 0.5543, 0.6410, 0.6174, 0.6016, 0.5453, 0.6282, 0.6543]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


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


class TestOCRA(unittest.TestCase):
    """ Test output method with reference:
    [1] Işık, A. T., & Adalı, E. A. (2016). A new integrated decision making
    approach based on SWARA and OCRA methods for the hotel selection problem. International Journal of Advanced
    Operations Management, 8(2), 140-151.
    """

    def test_output(self):
        body = methods.OCRA()
        matrix = np.array([[7.7, 256, 7.2, 7.3, 7.3],
                           [8.1, 250, 7.9, 7.8, 7.7],
                           [8.7, 352, 8.6, 7.9, 8.0],
                           [8.1, 262, 7.0, 8.1, 7.2],
                           [6.5, 271, 6.3, 6.4, 6.1],
                           [6.8, 228, 7.1, 7.2, 6.5]])

        weights = np.array([0.239, 0.225, 0.197, 0.186, 0.153])
        types = np.array([1, -1, 1, 1, 1])

        output = [0.143, 0.210, 0.164, 0.167, 0, 0.112]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestPROMETHEE_II(unittest.TestCase):
    """ Test output method with reference:
    [1] Zhao, H., Peng, Y., & Li, W. (2013). Revised PROMETHEE II for improving efficiency in emergency response.
    Procedia Computer Science, 17, 181-188.
    """

    def test_output(self):
        body = methods.PROMETHEE_II('usual')
        matrix = np.array([[4, 3, 2],
                           [3, 2, 4],
                           [5, 1, 3]])

        weights = np.array([0.5, 0.3, 0.2])
        types = np.ones(3)

        output = [0.1, -0.3, 0.2]
        output_method = [round(preference, 2) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestSPOTIS(unittest.TestCase):
    """ Test output method with reference:
    [1] Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The spotis rank reversal free method for
    multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION)
    (pp. 1-8). IEEE.
    """

    def test_output(self):
        matrix = np.array([[10.5, -3.1, 1.7],
                           [-4.7, 0, 3.4],
                           [8.1, 0.3, 1.3],
                           [3.2, 7.3, -5.3]])
        bounds = np.array([[-5, 12],
                           [-6, 10],
                           [-8, 5]], dtype=float)
        weights = np.array([0.2, 0.3, 0.5])

        types = np.array([1, -1, 1])

        body = methods.SPOTIS(bounds)
        output = [0.1989, 0.3705, 0.3063, 0.7491]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)

class TestSPOTIS2(unittest.TestCase):
    """ Test output method with reference:
    [1] Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The spotis rank reversal free method for
    multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION)
    (pp. 1-8). IEEE.
    """

    def test_output(self):
        matrix = np.array([
            [15000, 4.3, 99, 42, 737],
            [15290, 5.0, 116, 42, 892],
            [15350, 5.0, 114, 45, 952],
            [15490, 5.3, 123, 45, 1120],
            ], dtype='float')
        bounds = np.array([
            [14000, 16000],
            [3, 8],
            [80, 140],
            [35, 60],
            [650, 1300]
            ])
        weights = np.array([0.2941, 0.2353, 0.2353, 0.0588, 0.1765])

        types = np.array([-1, -1, -1, 1, 1])

        esp = np.array([15300, 4, 115, 50, 900])

        body = methods.SPOTIS(bounds, esp)
        output = [0.1841, 0.0734, 0.0842, 0.1920]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestTOPSIS(unittest.TestCase):
    """ Test output method with reference:
    [1] Opricovic, S., & Tzeng, G. H. (2004). Compromise solution by MCDM methods: A comparative analysis of VIKOR and
    TOPSIS. European journal of operational research, 156(2), 445-455.
    """

    def test_output(self):
        body = methods.TOPSIS()

        matrix = np.array([[1, 2, 5],
                           [3000, 3750, 4500]]).T

        weights = np.array([0.5, 0.5])

        types = np.array([-1, 1])

        output = [0.500, 0.617, 0.500]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)


class TestVIKOR(unittest.TestCase):
    """ Test output method with reference:
    [1] Yang, W., & Wu, Y. (2020). A new improvement method to avoid rank reversal in VIKOR.
    IEEE Access, 8, 21261-21271.
    [2] Opricovic, S., & Tzeng, G. H. (2004). Compromise solution by MCDM methods: A comparative analysis of VIKOR and
    TOPSIS. European journal of operational research, 156(2), 445-455.
    """

    def test_output_yang(self):
        body = methods.VIKOR()

        matrix = np.array([[78, 56, 34, 6],
                           [4, 45, 3, 97],
                           [18, 2, 50, 63],
                           [9, 14, 11, 92],
                           [85, 9, 100, 29]])

        types = np.array([1, 1, 1, 1])

        weights = np.array([0.25, 0.25, 0.25, 0.25])

        output = [0.5679, 0.7667, 1, 0.7493, 0]
        output_method = [round(preference, 4) for preference in body(matrix, weights, types)]

        self.assertListEqual(output, output_method)

    def test_output_opricovic(self):

        body = methods.VIKOR()

        matrix = np.array([[1, 2, 5],
                           [3000, 3750, 4500]]).T

        weights = np.array([0.5, 0.5])

        types = np.array([-1, 1])

        output = [1, 0, 1]
        output_method = list(body(matrix, weights, types))

        self.assertListEqual(output, output_method)


class TestRIM(unittest.TestCase):
    """ Test output method with reference:
    [1] Cables, E., Lamata, M. T., & Verdegay, J. L. (2016). RIM-reference ideal method in multicriteria decision
    making. Information Sciences, 337, 1-10.

    Note: The paper [1] which introduces the method has an error in the final results. The authors of the method confirm
    that result should be as the one we have obtained.
    """
    def test_output(self):
        matrix = np.array([
            [30,  0, 2, 3, 3, 2],
            [40,  9, 1, 3, 2, 2],
            [25,  0, 3, 1, 3, 2],
            [27,  0, 5, 3, 3, 1],
            [45, 15, 2, 2, 3, 4]
        ])

        weights = np.array([0.2262, 0.2143, 0.1786, 0.1429, 0.1190, 0.1190])

        range_t = np.array([
            [23, 60],
            [0, 15],
            [0, 10],
            [1, 3],
            [1, 3],
            [1, 5]
        ])

        ref_s = [
            [30, 35],
            [10, 15],
            [0, 0],
            [3, 3],
            [3, 3],
            [4, 5]
        ]

        pr = methods.RIM(range_t, ref_s)
        output_method = pr(matrix, weights, None, validation=False)

        output_method = list(np.round(output_method, 5))
        output = [0.58663, 0.75584, 0.37163, 0.46658, 0.74015]

        self.assertListEqual(output, output_method)


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



class TestERVD(unittest.TestCase):
    """ Test output method with reference:
    [1] Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method based on
    relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.
    """
    def test_output(self):
        matrix = np.array([
            [80, 70, 87, 77, 76, 80, 75],
            [85, 65, 76, 80, 75, 65, 75],
            [78, 90, 72, 80, 85, 90, 85],
            [75, 84, 69, 85, 65, 65, 70],
            [84, 67, 60, 75, 85, 75, 80],
            [85, 78, 82, 81, 79, 80, 80],
            [77, 83, 74, 70, 71, 65, 70],
            [78, 82, 72, 80, 78, 70, 60],
            [85, 90, 80, 88, 90, 80, 85],
            [89, 75, 79, 67, 77, 70, 75],
            [65, 55, 68, 62, 70, 50, 60],
            [70, 64, 65, 65, 60, 60, 65],
            [95, 80, 70, 75, 70, 75, 75],
            [70, 80, 79, 80, 85, 80, 70],
            [60, 78, 87, 70, 66, 70, 65],
            [92, 85, 88, 90, 85, 90, 95],
            [86, 87, 80, 70, 72, 80, 85]
        ])

        weights = np.array([0.066, 0.196, 0.066, 0.130, 0.130, 0.216, 0.196])
        types = np.ones(7)

        ref = np.ones(7) * 80

        ervd = methods.ERVD(ref_point=ref)
        output_method = list(np.round(ervd(matrix, weights, types), 3))
        output = [0.660, 0.503, 0.885, 0.521, 0.610, 0.796, 0.498, 0.549, 0.908, 0.565, 0.070, 0.199, 0.632, 0.716, 0.438, 0.972, 0.767]

        self.assertListEqual(output, output_method)


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


class TestWSM(unittest.TestCase):
    """ Test output method with reference:
    Self-reference
    """
    def test_output(self):
        body = methods.WSM()
        matrix = np.array([[96, 83, 75, 7],
                            [63, 5, 56, 9],
                            [72, 30, 32, 48],
                            [11, 4, 27, 9],
                            [77, 21, 17, 11]])
        weights = np.array([8 / 13, 5 / 13, 6 / 13, 7 / 13])
        types = np.array([1, 1, -1, -1])
        output_method = list(np.round(body(matrix, weights, types, validation=False), 3))
        output = [0.609, 0.313, 0.334, 0.265, 0.479]

        self.assertListEqual(output, output_method)


class TestWPM(unittest.TestCase):
    """ Test output method with reference:
    Self-reference
    """
    def test_output(self):
        body = methods.WPM()
        matrix = np.array([[96, 83, 75, 7],
                            [63, 5, 56, 9],
                            [72, 30, 32, 48],
                            [11, 4, 27, 9],
                            [77, 21, 17, 11]])
        weights = np.array([8 / 13, 5 / 13, 6 / 13, 7 / 13])
        types = np.array([1, 1, -1, -1])
        output_method = list(np.round(body(matrix, weights, types, validation=False), 3))
        output = [0.065, 0.017, 0.019, 0.007, 0.052]

        self.assertListEqual(output, output_method)


class TestWASPAS(unittest.TestCase):
    """ Test output method with reference:
    [1] Chakraborty, S., Zavadskas, E. K., & Antucheviciene, J. (2015). Applications of WASPAS method as a
    multi-criteria  decision-making tool. Economic Computation and Economic Cybernetics Studies and Research, 49(1),
    5-22.
    """
    def test_output(self):
        body = methods.WASPAS()
        matrix = np.array([[30, 23, 5, 0.745, 0.745, 1500, 5000],
                           [18, 13, 15, 0.745, 0.745, 1300, 6000],
                           [15, 12, 10, 0.500, 0.500, 950, 7000],
                           [25, 20, 13, 0.745, 0.745, 1200, 4000],
                           [14, 18, 14, 0.255, 0.745, 950, 3500],
                           [17, 15, 9, 0.745, 0.500, 1250, 5250],
                           [23, 18, 20, 0.500, 0.745, 1100, 3000],
                           [16, 8, 14, 0.255, 0.500, 1500, 3000]])
        weights = np.array([0.1181, 0.1181, 0.0445, 0.1181, 0.2861, 0.2861, 0.0445])
        types = np.array([1, 1, 1, 1, 1, -1, -1])
        output_method = list(np.round(body(matrix, weights, types, validation=False), 4))
        output = [0.8329, 0.7884, 0.6987, 0.8831, 0.7971, 0.7036, 0.8728, 0.5749]

        self.assertListEqual(output, output_method)

class TestLoPM(unittest.TestCase):
    """ Test output method with reference:
    [1] Farag, M. M. (2020). Materials and process selection for engineering design. CRC press.

    Output was slightly modified due to rounding errors.
    """
    def test_output(self):
        matrix = np.array([
            [14_820, 18, 0.0002, 2.1,  9.5, 4.5],
            [21_450, 18, 0.0012, 2.7, 14.4, 9.0],
            [78_000, 16, 0.0006, 2.6,  9.0, 8.5],
            [20_475, 17, 0.0006, 2.6,  6.5, 2.6],
            [16_575, 14, 0.0010, 3.1,  5.6, 3.5],
            [21_450, 16, 0.0005, 2.2,  8.6, 1.0]
        ])
        weights = np.array([0.20, 0.33, 0.13, 0.07, 0.07, 0.20])
        lopm = methods.LoPM([10_000, 14, 0.0015, 3.5, 2.3, 9.0], [1, 1, -1, -1, 0, -1])
        output_method = list(np.round(lopm(matrix, weights, None), 2))
        output = [0.77, 1.08, 0.81, 0.66, 0.78, 0.68]
        self.assertListEqual(output, output_method)
