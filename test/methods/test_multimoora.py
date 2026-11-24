# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestMULTIMOORA(unittest.TestCase):
    """ Test output method with reference:
    [1] Brauers, W. K. M., & Zavadskas, E. K. (2010). Project management by MULTIMOORA as an instrument for
    transition economies. Technological and Economic Development of Economy, 16(1), 5-24.

    Project planning (Appendices C and D). The paper uses no weights; with equal weights 1/9 the scores of the
    ratio system and the reference point are divided by 9 and the full multiplicative form is raised to the power
    1/9, which does not change the rankings.
    """

    matrix = np.array([
        [1, 14, 9, 200, 600, 20, 20, 3.5, 2.5],
        [1.6, 16, 7, 150, 800, 13.5, 25, 4, 1.5],
        [2, 17, 5, 80, 1200, 10, 30, 3.8, 1.25],
    ])
    weights = np.ones(9) / 9
    types = np.array([1, 1, -1, 1, 1, 1, -1, 1, 1])

    def setUp(self):
        body = methods.MULTIMOORA()
        self.results = body(self.matrix, self.weights, self.types, verbose=True)
        self.nmatrix, self.ratio, self.refpoint, self.fmf, self.rankings, self.pref = [
            table.data for table in self.results.results]

    def test_normalized_matrix(self):
        """ Objectives divided by their square roots (Table 2c). """
        output = [[0.3637, 0.5143, 0.7229, 0.7619, 0.3841, 0.7657, 0.4558, 0.5357, 0.7881],
                  [0.5819, 0.5878, 0.5623, 0.5715, 0.5121, 0.5168, 0.5698, 0.6122, 0.4729],
                  [0.7274, 0.6245, 0.4016, 0.3048, 0.7682, 0.3828, 0.6838, 0.5816, 0.3941]]
        self.assertListEqual(output, np.round(self.nmatrix, 4).tolist())

    def test_ratio_system(self):
        """ Sums of the ratio system (Table 2c). """
        self.assertListEqual([2.9348, 2.7232, 2.698], np.round(9 * self.ratio, 4).tolist())

    def test_reference_point(self):
        """ Largest deviations from the reference point (Table 2e). """
        self.assertListEqual([0.38411, 0.31524, 0.45716], np.round(9 * self.refpoint, 5).tolist())

    def test_full_multiplicative_form(self):
        """ Results of the full multiplicative form (Table 3). """
        self.assertListEqual([1633333, 1421897, 1033600], np.round(self.fmf ** 9).astype(int).tolist())

    def test_output(self):
        """ Rankings of the three parts and the final MULTIMOORA ranking (Table 1). """
        self.assertListEqual([[1, 2, 1], [2, 1, 2], [3, 3, 3]], self.rankings.astype(int).tolist())
        body = methods.MULTIMOORA()
        self.assertListEqual([1, 2, 3], body.rank(body(self.matrix, self.weights, self.types)).astype(int).tolist())


class TestMULTIMOORABankLoan(unittest.TestCase):
    """ Test output method with reference:
    [1] Brauers, W. K. M., & Zavadskas, E. K. (2011). MULTIMOORA optimization used to decide on a bank loan to buy
    property. Technological and Economic Development of Economy, 17(1), 174-188.

    Three banks with four grouped cost criteria (Table 4bis). All criteria have the same importance; with equal
    weights 1/4 the scores of the ratio system and the reference point are divided by 4. The full multiplicative form
    is not compared: the Foreign Bank has zero values of two cost criteria, and Table 5bis replaces them and changes
    other values of the matrix.
    """

    matrix = np.array([
        [5952.38, 335.158333, 0, 0],
        [7171.72, 322.27, 69.26, 0.5],
        [7157.29, 351.13, 69.26, 1],
    ])
    weights = np.ones(4) / 4
    types = -np.ones(4)

    def setUp(self):
        body = methods.MULTIMOORA()
        with np.errstate(divide='ignore'):
            self.results = body(self.matrix, self.weights, self.types, verbose=True)
        self.nmatrix, self.ratio, self.refpoint, self.fmf, self.rankings, self.pref = [
            table.data for table in self.results.results]

    def test_normalized_matrix(self):
        """ Objectives divided by their square roots (Table 4c'). """
        output = [[0.5065329, 0.5752307, 0.0, 0.0],
                  [0.6102957, 0.5531105, 0.7071068, 0.4472136],
                  [0.6090678, 0.6026428, 0.7071068, 0.8944272]]
        self.assertListEqual(output, np.round(self.nmatrix, 7).tolist())

    def test_ratio_system(self):
        """ Sums of the ratio system, all criteria are minimized (Table 4c'). """
        self.assertListEqual([1.08176, 2.31773, 2.81324], np.round(-4 * self.ratio, 5).tolist())

    def test_reference_point(self):
        """ Largest deviations from the reference point (Table 4e'). """
        self.assertListEqual([0.0221202, 0.7071068, 0.8944272], np.round(4 * self.refpoint, 7).tolist())

    def test_dominance(self):
        """ Rankings of the three methods and the MULTIMOORA ranking (Table 3): the Foreign Bank shows absolute
            dominance, Bank A dominates Bank B in two of the three rankings.
        """
        rankings = np.array([[1, 1, 1], [2, 2, 3], [3, 3, 2]])
        body = methods.MULTIMOORA()
        self.assertListEqual([1, 2, 3], body.rank(body.dominance(rankings)).astype(int).tolist())

    def test_circular_reasoning(self):
        """ Circular reasoning (p. 182): A (11-20-14) dominates B (14-16-15), B dominates C (15-19-12) and
            C dominates A, so the three objects get the same ranking.
        """
        rankings = np.array([[11, 20, 14], [14, 16, 15], [15, 19, 12]])
        body = methods.MULTIMOORA()
        self.assertListEqual([2.0, 2.0, 2.0], body.rank(body.dominance(rankings)).tolist())


class TestMULTIMOORADominance(unittest.TestCase):
    """ Dominance theory: an alternative better in two of the three rankings dominates, dominance is transitive and
        alternatives in a circular dominance share a position.
    """

    def test_dominated_alternative_is_ranked_lower(self):
        """ A3 dominates A4 and A4 dominates A1, A1 dominates A3: all four are in one circle and share a position.
            Counting only directly dominated alternatives would rank A4 (two) above A3 (one).
        """
        rankings = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 1], [4, 1, 2]])
        body = methods.MULTIMOORA()
        self.assertListEqual([2.5, 2.5, 2.5, 2.5], body.rank(body.dominance(rankings)).tolist())

    def test_transitiveness(self):
        """ A1 dominates A2 and A2 dominates A3. A1 is better than A3 in one ranking only (partial equability), but
            dominates it through A2, so A3 is below A2.
        """
        rankings = np.array([[1, 1, 2], [3, 2, 1], [1, 3, 2]])
        body = methods.MULTIMOORA()
        self.assertListEqual([1, 2, 3], body.rank(body.dominance(rankings)).astype(int).tolist())

    def test_benefit_criteria_only(self):
        """ Unlike MOORA, cost criteria are not required. The balanced alternative is the best in all three parts,
            the two symmetric alternatives are tied in all of them and share a position.
        """
        matrix = np.array([[4, 1], [1, 4], [3, 3]])
        body = methods.MULTIMOORA()
        self.assertListEqual([2.5, 2.5, 1], body.rank(body(matrix, np.ones(2) / 2, np.ones(2))).tolist())
