# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm.methods.sorting import ELECTRE_TRI


class TestELECTRE_TRI(unittest.TestCase):
    """ Test output method with reference:
    [1] Mousseau, V., Słowiński, R., & Zielniewicz, P. (2000). A user-oriented implementation of the ELECTRE-TRI
    method integrating preference elicitation support. Computers & Operations Research, 27(7-8), 757-777.
    """

    # Banking application of Section 4: seven cost criteria, three categories, parameters of Table 1
    weights = np.array([3, 1, 1, 1, 1, 1, 2]) / 10
    types = -np.ones(7)
    profiles = np.array([[17, 43, 43, 43, 43, 43, 40],
                         [14, 29, 29, 29, 29, 29, 27]])
    q = np.array([[0.67, 1.84, 1.84, 1.84, 1.84, 1.84, 2.56],
                  [0.64, 1.56, 1.56, 1.56, 1.56, 1.56, 2.04]])
    p = np.array([[1.34, 3.73, 3.73, 3.73, 3.73, 3.73, 5.19],
                  [1.28, 3.17, 3.17, 3.17, 3.17, 3.17, 4.15]])
    # Alternatives a19, a23, a41, a49, a68, a5, a27, a29, a55, a62, a66, a69, a84, a93 and a94 (Table 2)
    matrix = np.array([
        [13.02, 15.74, 18.02, 7.24, 79.21, 42.63, 79.32],
        [13.66, 11.01, 14.11, 70.55, 69.01, 18.77, 42.39],
        [13.04, 7.99, 22.44, 7.24, 31.40, 14.83, 58.65],
        [13.48, 1.05, 18.02, 6.45, 31.40, 18.77, 100.00],
        [9.91, 7.99, 14.11, 7.24, 12.92, 3.02, 58.65],
        [14.43, 11.01, 18.02, 29.25, 22.16, 31.73, 39.44],
        [13.51, 14.02, 18.02, 29.25, 22.16, 8.91, 39.44],
        [13.39, 11.01, 18.02, 17.36, 22.16, 8.91, 39.44],
        [12.14, 7.99, 18.02, 5.46, 22.16, 3.02, 39.44],
        [11.07, 7.99, 18.02, 5.46, 12.92, 3.02, 39.44],
        [10.25, 7.99, 14.11, 15.58, 12.92, 8.91, 20.24],
        [10.65, 11.01, 10.47, 3.69, 3.76, 8.91, 20.24],
        [8.26, 7.99, 10.47, 3.69, 3.76, 3.02, 20.24],
        [3.68, 1.96, 6.74, 15.58, 3.76, 3.02, 20.24],
        [3.86, 1.96, 3.02, 3.69, 3.76, 3.02, 20.24],
    ])

    def test_output(self):
        """ Pessimistic assignments for the parameters of Table 1 and cutting level 0.86. The paper states that the
            desired categories of Table 2 are the assignments of the pessimistic procedure, except a5, a27 and a93
            which are assigned to C2, C2 and C3, respectively.
        """
        body = ELECTRE_TRI(self.profiles, q=self.q, p=self.p, cutting_level=0.86)

        output = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        output_method = body(self.matrix, self.weights, self.types).tolist()
        self.assertListEqual(output, output_method)

    def test_optimistic_not_worse(self):
        """ The optimistic procedure never assigns an alternative to a worse category than the pessimistic one. """
        pessimistic = ELECTRE_TRI(self.profiles, q=self.q, p=self.p, cutting_level=0.86)
        optimistic = ELECTRE_TRI(self.profiles, q=self.q, p=self.p, cutting_level=0.86, procedure='optimistic')

        self.assertTrue(np.all(optimistic(self.matrix, self.weights, self.types)
                               >= pessimistic(self.matrix, self.weights, self.types)))

    def test_independence_of_alternatives(self):
        """ The category of an alternative does not depend on the other alternatives. """
        body = ELECTRE_TRI(self.profiles, q=self.q, p=self.p, cutting_level=0.86)
        categories = body(self.matrix, self.weights, self.types)

        for i in range(len(self.matrix)):
            self.assertEqual(categories[i], body(self.matrix[i:i + 1], self.weights, self.types)[0])

    def test_verbose(self):
        body = ELECTRE_TRI(self.profiles, q=self.q, p=self.p, cutting_level=0.86)
        results = body(self.matrix, self.weights, self.types, verbose=True)

        self.assertEqual(len(results.results), 5)
        self.assertListEqual(body(self.matrix, self.weights, self.types).tolist(),
                             results.results[-1].data.tolist())
        # Printing does not add a ranking table, as categories are not ranked
        self.assertNotIn('Final ranking', str(results))


class TestELECTRE_TRIRules(unittest.TestCase):
    """ Conjunctive and disjunctive rules for cutting level 1 and no thresholds, and the veto effect, as described
        in: Figueira, J. R., Mousseau, V., & Roy, B. (2016). ELECTRE methods. In Multiple Criteria Decision
        Analysis: State of the Art Surveys (pp. 155-185). Springer.
    """

    profiles = np.array([[5, 5, 5],
                         [8, 8, 8]])
    weights = np.ones(3) / 3
    types = np.ones(3)

    def test_conjunctive_rule(self):
        """ Pessimistic procedure with lambda = 1: a reaches a category only if it is at least as good as its lower
            limit on every criterion.
        """
        body = ELECTRE_TRI(self.profiles, cutting_level=1)
        matrix = np.array([[9, 9, 9], [9, 9, 7], [9, 9, 4], [5, 5, 5]])

        self.assertListEqual([3, 2, 1, 2], body(matrix, self.weights, self.types).tolist())

    def test_disjunctive_rule(self):
        """ Optimistic procedure with lambda = 1: a reaches a category if it is better than its lower limit on at
            least one criterion.
        """
        body = ELECTRE_TRI(self.profiles, cutting_level=1, procedure='optimistic')
        matrix = np.array([[9, 1, 1], [6, 1, 1], [1, 1, 1], [5, 5, 5]])

        self.assertListEqual([3, 2, 1, 2], body(matrix, self.weights, self.types).tolist())

    def test_veto(self):
        """ A very bad value on one criterion blocks the outranking regardless of the other criteria. """
        matrix = np.array([[10, 10, 2]])
        without_veto = ELECTRE_TRI(self.profiles, cutting_level=0.6)
        with_veto = ELECTRE_TRI(self.profiles, v=[None, None, 4], cutting_level=0.6)

        self.assertEqual(3, without_veto(matrix, self.weights, self.types)[0])
        self.assertEqual(1, with_veto(matrix, self.weights, self.types)[0])

    def test_validation(self):
        with self.assertRaises(ValueError):
            ELECTRE_TRI(self.profiles, q=[1, 1, 1], p=[0.5, 1, 1])
        with self.assertRaises(ValueError):
            ELECTRE_TRI(self.profiles, cutting_level=0.4)
        with self.assertRaises(ValueError):
            ELECTRE_TRI(self.profiles, procedure='median')
        with self.assertRaises(ValueError):
            ELECTRE_TRI(self.profiles, q=[1, 1])
        with self.assertRaises(ValueError):
            ELECTRE_TRI(self.profiles[::-1])(np.ones((2, 3)), self.weights, self.types)
        with self.assertRaises(NotImplementedError):
            ELECTRE_TRI(self.profiles).rank(np.array([1, 2]))
