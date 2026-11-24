# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestRTOPSIS(unittest.TestCase):
    """ Test output method with reference:
    [1] de Farias Aires, R. F., & Ferreira, L. (2019). A new approach to avoid rank reversal cases in the TOPSIS
    method. Computers & Industrial Engineering, 132, 84-97.

    Case study from Appendix C: decision matrix and weights from Table B.4, domains from Table C.11.
    """
    # Alternatives A1, A2, A5, A8, A12, A13, A54, A55, A56, A59, A61, A67, A71, A72, A76, A83, A87, A88, A90, A91
    matrix = np.array([
        [8.5218, 1.0000, 1.0000],
        [7.0455, 1.0000, 1.0000],
        [7.9625, 0.9821, 1.0000],
        [8.4073, 0.9649, 1.0000],
        [8.5000, 1.0000, 1.0000],
        [7.0291, 1.0000, 1.0000],
        [8.3702, 0.9649, 1.0000],
        [6.7018, 1.0000, 1.0000],
        [7.8455, 1.0000, 1.0000],
        [8.2291, 1.0000, 1.0000],
        [7.7618, 1.0000, 1.0000],
        [7.5909, 1.0000, 1.0000],
        [7.6564, 1.0000, 1.0000],
        [7.5273, 1.0000, 1.0000],
        [8.6286, 0.9821, 1.0000],
        [7.7673, 1.0000, 1.0000],
        [8.3273, 1.0000, 1.0000],
        [7.0983, 0.9483, 1.0000],
        [7.4224, 0.9483, 1.0000],
        [8.3304, 0.9821, 1.0000],
    ])
    weights = np.array([0.3633, 0.3298, 0.3069])
    types = np.array([1, 1, 1])
    bounds = np.array([[0, 10], [0, 1], [0, 1]], dtype=float)

    def test_output(self):
        """ Closeness coefficients and ordering from Table C.11 (Max normalization). """
        body = methods.RTOPSIS(self.bounds)
        preferences = body(self.matrix, self.weights, self.types)

        output = [0.9105, 0.8284, 0.8775, 0.9011, 0.9093, 0.8275, 0.8989, 0.8104, 0.8720, 0.8937,
                  0.8673, 0.8579, 0.8615, 0.8544, 0.9157, 0.8676, 0.8993, 0.8264, 0.8439, 0.8984]
        output_method = [round(preference, 4) for preference in preferences]
        self.assertListEqual(output, output_method)

        output = [2, 17, 9, 4, 3, 18, 6, 20, 10, 8, 12, 14, 13, 15, 1, 11, 5, 19, 16, 7]
        output_method = [int(r) for r in body.rank(preferences)]
        self.assertListEqual(output, output_method)

    def test_addition_of_alternative(self):
        """ Adding a copy of A12 (alternative AA, Table C.12) does not change the other evaluations. """
        body = methods.RTOPSIS(self.bounds)
        preferences = body(self.matrix, self.weights, self.types)
        extended = np.vstack((self.matrix, self.matrix[4]))
        preferences_extended = body(extended, self.weights, self.types)

        np.testing.assert_array_equal(preferences, preferences_extended[:-1])
        self.assertEqual(round(preferences_extended[-1], 4), 0.9093)

    def test_values_outside_domain(self):
        body = methods.RTOPSIS(self.bounds)
        matrix = self.matrix.copy()
        matrix[1, 1] = 1.2
        with self.assertRaises(ValueError):
            body(matrix, self.weights, self.types)

    def test_minmax_normalization(self):
        """ With domains starting at zero, Max and Max-Min normalizations (Steps 5.1 and 5.2) coincide. """
        preferences_max = methods.RTOPSIS(self.bounds, normalization='max')(self.matrix, self.weights, self.types)
        preferences_minmax = methods.RTOPSIS(self.bounds, normalization='minmax')(self.matrix, self.weights,
                                                                                   self.types)
        np.testing.assert_allclose(preferences_max, preferences_minmax)


class TestRTOPSISExpandBounds(unittest.TestCase):
    """ Test output method with reference:
    [1] Yang, B., Zhao, J., & Zhao, H. (2022). A robust method for avoiding rank reversal in the TOPSIS.
    Computers & Industrial Engineering, 174, 108776.
    """

    def test_output(self):
        """ Extended extremes of Case study I (Section 5.1, alpha = 6). """
        matrix = np.array([[36, 42, 43, 70],
                           [25, 50, 45, 80],
                           [28, 45, 50, 75]])
        bounds = methods.RTOPSIS.expand_bounds(matrix, alpha=6)

        self.assertListEqual([0.0, 17.75, 21.37, 40.0], [round(b, 2) for b in bounds[:, 0]])
        self.assertListEqual([70.12, 74.25, 71.63, 110.0], [round(b, 2) for b in bounds[:, 1]])

    def test_output_case_2(self):
        """ Extended extremes of Case study II (Section 5.2, Table 6, alpha = 6). """
        matrix = np.array([[4184.3, 2.41, 407.2, 251, 195, 244, 15, 2914],
                           [5211.9, 1.41, 501.7, 308.3, 282, 346, 21, 3630],
                           [5021.3, 4.42, 504, 278.6, 12, 56, 3, 3920.5],
                           [5566.1, 3.36, 559.5, 335.3, 167, 268, 16, 3957.5],
                           [5060.5, 4.04, 514.1, 284.2, 69, 90, 7, 3293.5]])
        bounds = methods.RTOPSIS.expand_bounds(matrix, alpha=6)

        output = [1133.04, 0.0, 74.03, 59.83, 0.0, 0.0, 0.0, 264.85]
        self.assertListEqual(output, [round(b, 2) for b in bounds[:, 0]])
        # The paper reports 1085.18 for the sixth criterion, the exact value is 1085.1747
        output = [8617.36, 11.78, 892.67, 526.47, 919.94, 1085.17, 64.60, 6606.65]
        self.assertListEqual(output, [round(b, 2) for b in bounds[:, 1]])


class TestRTOPSISBoxplotBounds(unittest.TestCase):
    """ Test output method with reference:
    [1] Yang, W., Pang, X., Kong, D., & Shang, H. (2026). BP-TOPSIS: A Boxplot-Based Approach to Reducing Rank
    Reversal in the TOPSIS Method. International Journal of Information Technology & Decision Making, 25(10),
    3509-3538.

    BP-TOPSIS is R-TOPSIS with the boxplot fences (e = 3) of the original decision matrix as the domain and the
    Max-Min normalization. The domain is computed once and kept for the modified sets of alternatives. The paper
    gives only the rankings.
    """

    @staticmethod
    def ranks(bounds, matrix, weights, types):
        body = methods.RTOPSIS(bounds, 'minmax', clip=True)
        return body.rank(body(matrix, weights, types)).astype(int).tolist()

    def test_case_1(self):
        """ Case one (Table 6): rankings of the original, delete, add and replace sets. """
        matrix = np.array([[36, 42, 43, 70],
                           [25, 50, 45, 80],
                           [28, 45, 50, 75],
                           [24, 40, 47, 100]])
        weights = np.array([1/6, 1/3, 1/3, 1/6])
        types = np.ones(4)
        bounds = methods.RTOPSIS.boxplot_bounds(matrix)

        self.assertListEqual([4, 2, 1, 3], self.ranks(bounds, matrix, weights, types))
        self.assertListEqual([3, 2, 1], self.ranks(bounds, matrix[:3], weights, types))
        added = np.vstack([matrix, [21, 46, 42, 97]])
        self.assertListEqual([5, 2, 1, 3, 4], self.ranks(bounds, added, weights, types))
        replaced = np.vstack([matrix[:3], [29, 48, 43, 86]])
        self.assertListEqual([4, 2, 1, 3], self.ranks(bounds, replaced, weights, types))

    def test_case_2(self):
        """ Case two (Table 7). Table 7 marks C5-C8 as cost criteria, but its rankings of all three methods are
            reproduced only when all eight criteria are treated as benefit criteria: VIKOR, for instance, gives the
            paper's rankings (5, 2, 4, 1, 3 for the original set) with benefit criteria and 5, 4, 2, 3, 1 with
            C5-C8 as cost criteria. The test therefore uses benefit criteria. The added alternative E6 exceeds the
            upper fence of C2 (13.94 > 11.19), which is clipped.
        """
        matrix = np.array([[4184.3, 2.41, 407.2, 251, 195, 244, 15, 2914],
                           [5211.9, 1.41, 501.7, 308.3, 282, 346, 21, 3630],
                           [5021.3, 4.42, 504, 278.6, 12, 56, 3, 3920.5],
                           [5566.1, 3.36, 559.5, 335.3, 167, 268, 16, 3957.5],
                           [5060.5, 4.04, 514.1, 284.2, 69, 90, 7, 3293.5]])
        weights = np.ones(8) / 8
        types = np.ones(8)
        bounds = methods.RTOPSIS.boxplot_bounds(matrix)

        self.assertListEqual([5, 2, 4, 1, 3], self.ranks(bounds, matrix, weights, types))
        self.assertListEqual([4, 1, 3, 2], self.ranks(bounds, matrix[[0, 1, 2, 4]], weights, types))
        added = np.vstack([matrix, [5387.0, 13.94, 528.8, 279.37, 51.2, 108, 22.23, 3672.45]])
        self.assertListEqual([6, 3, 5, 2, 4, 1], self.ranks(bounds, added, weights, types))
        replaced = matrix.copy()
        replaced[3] = [4991.22, 5.45, 475.27, 332.14, 212.34, 223.60, 21.49, 2950.48]
        self.assertListEqual([5, 1, 4, 2, 3], self.ranks(bounds, replaced, weights, types))

    def test_quartiles(self):
        """ Quartiles of Eq. (6), (n + 1) p-th order statistic with linear interpolation. """
        values = np.array([[7.0], [1.0], [3.0], [5.0]])
        bounds = methods.RTOPSIS.boxplot_bounds(values, e=0)
        self.assertListEqual([[1.5, 6.5]], bounds.tolist())


class TestRTOPSISHistoricalBounds(unittest.TestCase):
    """ Test output method with reference:
    [1] Yang, W. (2020). Ingenious solution for the rank reversal problem of TOPSIS method. Mathematical
    Problems in Engineering, 2020, 9676518.

    NR-TOPSIS: historical extremes as the domain and the Max-Min normalization (Example 1).
    """
    matrix = np.array([[36, 42, 43, 70],
                       [25, 50, 45, 80],
                       [28, 45, 50, 75],
                       [24, 40, 47, 100]])
    weights = np.array([1/6, 1/3, 1/3, 1/6])
    types = np.ones(4)

    def test_output(self):
        """ Weighted normalized matrix from Eq. (19) and the ranking A3, A2, A4, A1. """
        body = methods.RTOPSIS(methods.RTOPSIS.make_bounds(self.matrix), normalization='minmax')
        weighted_matrix = body(self.matrix, self.weights, self.types, verbose=True).results[1].data

        output = [[0.1667, 0.0667, 0.0, 0.0],
                  [0.0139, 0.3333, 0.0952, 0.0556],
                  [0.0556, 0.1667, 0.3333, 0.0278],
                  [0.0, 0.0, 0.1905, 0.1667]]
        output_method = [[round(v, 4) for v in row] for row in weighted_matrix]
        self.assertListEqual(output, output_method)

        ranking = body.rank(body(self.matrix, self.weights, self.types))
        self.assertListEqual([4, 2, 1, 3], [int(r) for r in ranking])

    def test_addition_of_alternative(self):
        """ Adding A5 = (36, 50, 45, 70) gives A3, A5, A2, A4, A1, Eq. (21). """
        body = methods.RTOPSIS(methods.RTOPSIS.make_bounds(self.matrix), normalization='minmax')
        matrix = np.vstack((self.matrix, [36, 50, 45, 70]))
        ranking = body.rank(body(matrix, self.weights, self.types))
        self.assertListEqual([5, 3, 1, 4, 2], [int(r) for r in ranking])


class TestRTOPSISAbsoluteMode(unittest.TestCase):
    """ Test output method with reference:
    [1] García-Cascales, M. S., & Lamata, M. T. (2012). On rank reversal and TOPSIS method. Mathematical and
    Computer Modelling, 56, 123-132.

    Absolute mode: one common scale S = [0, 5] for all criteria and the Max normalization (Table 6).
    """

    def test_output(self):
        matrix = np.array([[1, 5],
                           [4, 2],
                           [3, 3],
                           [5, 1]])
        weights = np.array([0.5, 0.5])
        types = np.ones(2)
        body = methods.RTOPSIS(np.array([[0, 5], [0, 5]]))

        output = [0.560, 0.586, 0.600, 0.560]
        output_method = [round(preference, 3) for preference in body(matrix, weights, types)]
        self.assertListEqual(output, output_method)


class TestRTOPSISDesiredLevels(unittest.TestCase):
    """ Test output method with reference:
    [1] Costa, L. F., Costa, H. G., Lima, D., & Rodrigues, B. (2026). TOPSIS-RAD: Ranking According to
    Desires. arXiv preprint arXiv:2606.07253.

    TOPSIS-RAD: vetoed and desired performance levels as the domain, the Max-Min normalization and
    clipping above the desired levels. Decision matrix from Table 3.
    """
    matrix = np.array([[68, 72, 74, 78],
                       [62, 76, 78, 80],
                       [58, 70, 150, 76],
                       [80, 72, 99, 90],
                       [90, 88, 47, 118],
                       [80, 64, 66, 70],
                       [76, 68, 98, 105],
                       [80, 50, 5, 41],
                       [70, 74, 78, 75],
                       [60, 68, 82, 81]])
    weights = np.full(4, 0.25)
    types = np.ones(4)

    def test_output_veto(self):
        """ Toy Example B (Table 9): VPL = 20, DPL = maxima of the criteria; A8 is vetoed and removed. """
        bounds = np.array([[20, 90], [20, 88], [20, 150], [20, 118]])
        body = methods.RTOPSIS(bounds, normalization='minmax', clip=True)
        matrix = np.delete(self.matrix, 7, axis=0)

        output = [0.6068, 0.6119, 0.6837, 0.7266, 0.6877, 0.5807, 0.7312, 0.6197, 0.5916]
        output_method = [round(preference, 4) for preference in body(matrix, self.weights, self.types)]
        self.assertListEqual(output, output_method)

    def test_output_desired_levels(self):
        """ Toy Example C (Tables 11 and 13): VPL = (58, 50, 5, 41), DPL = 80, values above DPL clipped. """
        bounds = np.array([[58, 80], [50, 80], [5, 80], [41, 80]])
        body = methods.RTOPSIS(bounds, normalization='minmax', clip=True)

        output = [0.7197, 0.6659, 0.5861, 0.8758, 0.8053, 0.7154, 0.7984, 0.3660, 0.7600, 0.6078]
        output_method = [round(preference, 4) for preference in body(self.matrix, self.weights, self.types)]
        self.assertListEqual(output, output_method)
