# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np
from scipy.stats import rankdata

from pymcdm import methods


class TestDARP(unittest.TestCase):
    """ Test output method with reference:
    [1] Roszkowska, E., Filipowicz-Chomko, M., & Wachowicz, T. (2020). Using individual and common reference points
    to measure the performance of alternatives in multiple criteria evaluation. Operations Research and Decisions,
    30(3), 77-96.
    """

    # Table 2: smart growth indicators of the EU countries in 2017 (Austria, ..., Sweden in alphabetical order):
    # C1 - GERD (% of GDP), C2 - early leavers from education and training (%), C3 - tertiary educational
    # attainment (%), and the national targets for them.
    data = np.array([
        [3.16, 3.76, 7.4, 9.5, 40.8, 38], [2.58, 3, 8.9, 9.5, 45.9, 47], [0.75, 1.5, 12.7, 11, 32.8, 36],
        [0.86, 1.4, 3.1, 4, 28.7, 35], [0.56, 0.5, 8.5, 10, 55.9, 46], [1.79, 1, 6.7, 5.5, 34.2, 32],
        [3.05, 3, 8.8, 10, 48.8, 40], [1.29, 3, 10.8, 9.5, 48.4, 40], [2.76, 4, 8.2, 8, 44.6, 42],
        [2.19, 3, 8.9, 9.5, 44.3, 50], [3.02, 3, 10.1, 10, 34, 42], [1.13, 1.2, 6, 10, 43.7, 32],
        [1.35, 1.8, 12.5, 10, 32.1, 34], [1.05, 2, 5, 8, 54.5, 60], [1.35, 1.53, 14, 16, 26.9, 26],
        [0.51, 1.5, 8.6, 10, 43.8, 34], [0.89, 1.9, 5.4, 9, 58, 48.7], [1.26, 2.3, 7.3, 10, 52.7, 66],
        [0.54, 2, 17.7, 10, 33.5, 33], [1.99, 2.5, 7.1, 8, 47.9, 40], [1.03, 1.7, 5, 4.5, 45.7, 45],
        [1.33, 2.7, 12.6, 10, 33.5, 40], [0.5, 2, 18.1, 11.3, 26.3, 26.7], [0.88, 1.2, 9.3, 6, 34.3, 40],
        [1.86, 3, 4.3, 5, 46.4, 40], [1.2, 2, 18.3, 15, 41.2, 44], [3.4, 4, 7.7, 7, 51.3, 45]])
    matrix = data[:, [0, 2, 4]]
    national = data[:, [1, 3, 5]]
    weights = np.ones(3) / 3
    types = np.array([1, -1, 1])

    def _check(self, body, values, ranks):
        """ The paper gives tied alternatives the best of their ranks. """
        pref = body(self.matrix, self.weights, self.types)
        self.assertListEqual(values, np.round(pref, 3).tolist())
        self.assertListEqual(ranks, rankdata(-np.round(pref, 10), method='min').astype(int).tolist())

    def test_best_performance(self):
        """ Table 3, D1: internal common reference point, the best performance of the countries. """
        self._check(methods.DARP(),
                    [0.643, 0.648, 0.211, 0.265, 0.397, 0.444, 0.717, 0.459, 0.663, 0.589, 0.483, 0.467, 0.281,
                     0.522, 0.188, 0.335, 0.493, 0.535, 0.088, 0.632, 0.473, 0.293, 0.004, 0.298, 0.625, 0.213, 0.787],
                    [5, 4, 24, 22, 17, 16, 2, 15, 3, 8, 12, 14, 21, 10, 25, 18, 11, 9, 26, 6, 13, 20, 27, 19, 7, 23,
                     1])

    def test_eu_targets(self):
        """ Table 3, D2: external common reference point, the EU targets [3, 10, 40]. Austria, Denmark and Sweden
            reach all targets and share the first place.
        """
        self._check(methods.DARP(reference=[3, 10, 40]),
                    [1.0, 0.903, 0.37, 0.314, 0.437, 0.629, 1.0, 0.601, 0.945, 0.813, 0.747, 0.568, 0.465, 0.55,
                     0.274, 0.425, 0.513, 0.598, 0.173, 0.767, 0.545, 0.494, 0.008, 0.455, 0.737, 0.289, 1.0],
                    [1, 5, 22, 23, 20, 10, 1, 11, 4, 6, 8, 13, 18, 14, 25, 21, 16, 12, 26, 7, 15, 17, 27, 19, 9, 24,
                     1])

    def test_national_targets(self):
        """ Table 3, D3: external individual reference points, the national targets. The target of Cyprus for C1 is
            the worst performance and the target of Italy for C3 is below it, so they are reached (Eq. 4).
        """
        self._check(methods.DARP(reference=self.national),
                    [0.894, 0.898, 0.508, 0.457, 1.0, 0.946, 1.0, 0.596, 0.795, 0.767, 0.706, 0.942, 0.699, 0.622,
                     0.899, 0.428, 0.583, 0.614, 0.224, 0.853, 0.677, 0.513, 0.009, 0.611, 0.737, 0.339, 0.895],
                    [8, 6, 22, 23, 1, 3, 1, 19, 10, 11, 13, 4, 14, 16, 5, 24, 20, 17, 26, 9, 15, 21, 27, 18, 12, 25,
                     7])

    def test_observation_2(self):
        """ Observation 2: less demanding reference points do not decrease the measure, so D1 <= D2. """
        d1 = methods.DARP()(self.matrix, self.weights, self.types)
        d2 = methods.DARP(reference=[3, 10, 40])(self.matrix, self.weights, self.types)
        self.assertTrue(np.all(d1 <= d2))

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.DARP(reference=[3, 10])(self.matrix, self.weights, self.types)
        with self.assertRaises(ValueError):
            methods.DARP(reference=self.national[:5])(self.matrix, self.weights, self.types)
