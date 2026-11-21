# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

class TestBalancedSPOTIS(unittest.TestCase):
    """ Test output method with reference:

        Shekhovtsov, A., Dezert, J. and Sałabun, W. (2025). Enhancing Personalized Decision-Making
        with the Balanced SPOTIS Algorithm. In Proceedings of the 17th International Conference
        on Agents and Artificial Intelligence - Volume 3: ICAART; ISBN 978-989-758-737-5;
        ISSN 2184-433X, SciTePress, pages 264-271. DOI: 10.5220/0013119800003890
    """
    def setUp(self):
        self.matrix = np.array([
            [94.0, 69.9, 2017.0],
            [297.0, 42.0, 2013.0],
            [205.0, 68.9, 2015.0],
            [360.0, 36.9, 2014.0],
            [86.0, 59.9, 2017.0],
            [79.6, 63.8, 2017.0],
            [113.0, 56.9, 2015.0],
            [171.0, 58.0, 2016.0]])

        self.bounds = np.array([
            [70, 360],
            [35, 70],
            [2013, 2018]], dtype=float)

        self.weights = np.array([0.33, 0.56, 0.11])
        self.types = np.array([-1, -1, 1])
        self.esp = np.array([110, 45, 2018], dtype=float)

    def test_output_balanced(self):
        matrix, bounds, weights, types, esp = \
            self.matrix, self.bounds, self.weights, self.types, self.esp

        bspotis = methods.BalancedSPOTIS(bounds, esp, alpha=0.5)
        results = list(np.round(bspotis(matrix, weights, types), 4))
        expected = [0.5232, 0.4256, 0.6593, 0.4752, 0.3632, 0.4256, 0.3626, 0.4242]
        self.assertListEqual(results, expected)

    def test_output_ideal(self):
        matrix, bounds, weights, types, esp = \
            self.matrix, self.bounds, self.weights, self.types, self.esp

        spotis_ideal = methods.SPOTIS(bounds)
        expected_ideal = list(np.round(spotis_ideal(matrix, weights, types), 4))
        bspotis = methods.BalancedSPOTIS(bounds, esp, alpha=0)
        results = list(np.round(bspotis(matrix, weights, types), 4))
        self.assertListEqual(results, expected_ideal)

    def test_output_expected(self):
        matrix, bounds, weights, types, esp = \
            self.matrix, self.bounds, self.weights, self.types, self.esp

        spotis_expected = methods.SPOTIS(bounds, esp)
        expected_expected = list(np.round(spotis_expected(matrix, weights, types), 4))
        bspotis = methods.BalancedSPOTIS(bounds, esp, alpha=1)
        results = list(np.round(bspotis(matrix, weights, types), 4))
        self.assertListEqual(results, expected_expected)
