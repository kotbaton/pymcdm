# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestRPM(unittest.TestCase):
    """ Test output method with reference:
    [1] Wierzbicki, A. P., Granat, J., & Makowski, M. (2007). Discrete decision problems with large number of
    criteria. IIASA Interim Report IR-07-025. International Institute for Applied Systems Analysis, Laxenburg.
    """

    # Table 2: divisions A-F of an international corporation; profit, market share, internal trade and local social
    # image (all maximized).
    matrix = np.array([[11, 8, 10, 40],
                       [23, 40, 34, 60],
                       [16, 50, 45, 70],
                       [35, 20, 20, 44],
                       [18, 30, 20, 80],
                       [12, 8, 9, 30]])
    # Table 3: aspiration and reservation levels A, rounded as in the paper
    levels = dict(aspiration=[27.1, 38, 34, 67], reservation=[15.1, 17, 16, 42])
    # Table 4: importance factors normal, normal, much less important, much more important
    importance = dict(alpha=[3, 3, 5, 1], beta=[7, 7, 9, 5])

    def test_statistical_levels(self):
        """ Table 3, Eq. 4: bounds and levels computed from the data. """
        worst, reservation, aspiration, best = methods.RPM()._levels(self.matrix, np.ones(4))
        self.assertListEqual([11, 8, 9, 30], worst.tolist())
        self.assertListEqual([35, 50, 45, 80], best.tolist())
        self.assertListEqual([15.1, 17, 16, 42], np.round(reservation, 1).tolist())
        self.assertListEqual([27.1, 38, 34, 67], np.round(aspiration, 1).tolist())

    def test_objective_ranking(self):
        """ Table 3, ranking A (epsilon = 0.4). The paper gives 0.37 for sigma_3 of A and 7.62 for sigma_4 of C,
            while Eq. 2 gives 3 * (10 - 9) / (16 - 9) = 0.43 and 7 + 3 * (70 - 67) / (80 - 67) = 7.69 (Table 4
            agrees with Eq. 2 for these values); the overall achievement of E is 3.89 + 2.33 = 6.22, as the paper
            takes 3.97 instead of the minimum 3.89, and that of C is 6.40 instead of 6.39.
        """
        body = methods.RPM(**self.levels)
        achievements, pref = [table.data for table in body(self.matrix, verbose=True).results]
        self.assertListEqual([[0.0, 0.0, 0.43, 2.5],
                              [5.63, 7.5, 7.0, 5.88],
                              [3.3, 10.0, 10.0, 7.69],
                              [10.0, 3.57, 3.89, 3.32],
                              [3.97, 5.48, 3.89, 10.0],
                              [0.73, 0.0, 0.0, 0.0]], np.round(achievements, 2).tolist())
        self.assertListEqual([0.29, 8.23, 6.4, 5.4, 6.22, 0.07], np.round(pref, 2).tolist())
        self.assertListEqual([5, 1, 2, 4, 3, 6], body.rank(pref).astype(int).tolist())
        # The statistical levels computed from the data give the same ranking
        self.assertListEqual([5, 1, 2, 4, 3, 6], body.rank(methods.RPM()(self.matrix)).astype(int).tolist())

    def test_importance_factors(self):
        """ Table 4: importance factors expressed by alpha and beta. The overall achievement of A in the paper (0.29)
            is copied from Table 3; Eq. 3 gives 0 + 0.1 * (0.71 + 0.83) = 0.15.
        """
        body = methods.RPM(**self.levels, **self.importance)
        achievements, pref = [table.data for table in body(self.matrix, verbose=True).results]
        self.assertListEqual([[0.0, 0.0, 0.71, 0.83],
                              [5.63, 7.5, 9.0, 3.88],
                              [3.3, 10.0, 10.0, 6.15],
                              [10.0, 3.57, 5.89, 1.32],
                              [3.97, 5.48, 5.89, 10.0],
                              [0.73, 0.0, 0.0, 0.0]], np.round(achievements, 2).tolist())
        np.testing.assert_allclose([0.15, 6.48, 6.24, 3.4, 6.5, 0.07], pref, atol=0.006)
        self.assertListEqual([5, 2, 3, 4, 1, 6], body.rank(pref).astype(int).tolist())

    def test_equitable_aggregation(self):
        """ Table 5: Lorenz quantile L3 and OWA achievements. The paper gives 2.76 for L3 of D and 0.01 for OWA of F,
            while its partial achievements give (1.32 + 3.57 + 5.89) / 3 = 3.59 and 0.73 / 16 = 0.05; the rankings
            are the same.
        """
        lorenz = methods.RPM(**self.levels, **self.importance, aggregation='lorenz', quantile=3)
        owa = methods.RPM(**self.levels, **self.importance, aggregation='owa')
        l3, sigma_owa = lorenz(self.matrix), owa(self.matrix)
        np.testing.assert_allclose([0.24, 5.67, 6.48, 3.59, 5.11, 0.0], l3, atol=0.006)
        np.testing.assert_allclose([0.14, 4.85, 5.06, 2.91, 4.72, 0.05], sigma_owa, atol=0.011)
        self.assertListEqual([5, 2, 1, 4, 3, 6], lorenz.rank(l3).astype(int).tolist())
        self.assertListEqual([5, 2, 1, 4, 3, 6], owa.rank(sigma_owa).astype(int).tolist())

    def test_spectrum_management(self):
        """ Table 6: 4 plans and 15 criteria on the scale 0-100 with the given aspiration and reservation levels,
            epsilon = 0.75 and the Lorenz quantile L5. The paper gives 8.00 for sigma_12 of C, 6.52 for sigma_12
            of D and 9.54 for sigma_15 of D, while Eq. 2 gives 7.00, 6.44 and 9.77, so the values differ slightly;
            the rankings B > C > D > A of all three aggregations are the same.
        """
        matrix = np.array([[100, 62, 100, 17, 98, 96, 100, 96, 92, 0, 0, 100, 67, 0, 0],
                           [89, 100, 0, 23, 100, 100, 75, 99, 87, 18, 100, 98, 48, 99, 96],
                           [85, 88, 21, 0, 99, 97, 93, 100, 88, 2, 100, 98, 38, 99, 100],
                           [0, 75, 0, 0, 92, 86, 79, 99, 68, 100, 100, 91, 100, 92, 99]])
        levels = dict(bounds=np.array([[0, 100]] * 15),
                      reservation=[34, 40, 15, 5, 48, 47, 43, 49, 42, 15, 37, 48, 32, 36, 37],
                      aspiration=[84, 90, 65, 55, 98, 97, 93, 99, 92, 65, 87, 98, 82, 86, 87])
        achievements = methods.RPM(**levels)(matrix, verbose=True).results[0].data
        np.testing.assert_allclose([10.0, 4.76, 10.0, 3.96, 7.0, 6.92, 10.0, 6.76, 7.0, 0.0, 0.0, 10.0, 5.8, 0.0, 0.0],
                                   achievements[0], atol=0.006)
        np.testing.assert_allclose([7.94, 10.0, 0.0, 4.44, 10.0, 10.0, 5.56, 7.0, 6.6, 3.24, 10.0, 7.0, 4.28, 9.79,
                                    9.08], achievements[1], atol=0.006)
        for aggregation in ('achievement', 'lorenz', 'owa'):
            with self.subTest(aggregation=aggregation):
                body = methods.RPM(**levels, epsilon=0.75, aggregation=aggregation, quantile=5)
                self.assertListEqual([4, 1, 2, 3], body.rank(body(matrix)).astype(int).tolist())

    def test_cost_criteria(self):
        """ A cost criterion gives the same achievements as the mirrored profit criterion. """
        mirrored = self.matrix.copy()
        mirrored[:, 0] = 100 - self.matrix[:, 0]
        np.testing.assert_allclose(methods.RPM()(self.matrix),
                                   methods.RPM()(mirrored, types=np.array([-1, 1, 1, 1])))

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.RPM(alpha=7, beta=3)
        with self.assertRaises(ValueError):
            methods.RPM(aggregation='sum')
        with self.assertRaises(ValueError):
            methods.RPM(aspiration=[10, 10, 10, 10], reservation=[20, 20, 20, 20])(self.matrix)
        with self.assertRaises(ValueError):
            methods.RPM(bounds=np.array([[0, 20]] * 4))(self.matrix)
