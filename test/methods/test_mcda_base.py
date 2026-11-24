# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np
import warnings

from pymcdm import methods

class TestMCDA(unittest.TestCase):

    def test_validation(self):
        # Catch warning about dominated alternatives
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            with self.assertRaises(ValueError):
                body = methods.TOPSIS()
                matrix = np.array([[1, 2, 3], [1, 2, 3]])
                weights = np.array([0.5, 0.5])
                types = np.array([1, -1, -1])

                body(matrix=matrix, weights=weights, types=types)


class TestDominanceCheck(unittest.TestCase):
    """ Ranking methods warn about dominant and dominated alternatives; the check can be disabled. """

    matrix = np.array([[5, 10], [1, 2], [3, 4]])
    weights = np.array([0.5, 0.5])
    types = np.array([1, 1])

    def test_ranking_method_warns(self):
        with self.assertWarns(UserWarning):
            methods.TOPSIS()(self.matrix, self.weights, self.types)

    def test_disabled_check(self):
        from pymcdm.validators import validate_decision_problem
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            validate_decision_problem(self.matrix, self.weights, self.types, check_dominance=False)
