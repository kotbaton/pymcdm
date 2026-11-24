# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods


class TestRVIKOR(unittest.TestCase):
    """ Test output method with reference:
    [1] Yang, W., & Wu, Y. (2020). A new improvement method to avoid rank reversal in VIKOR. IEEE Access, 8,
    21261-21271.
    """

    def test_output_vikor_undefined(self):
        """ Example 1 (Tables 1 and 2): classical VIKOR divides by zero, as R is equal for all alternatives.
            Equal weights, domain [1, 100] for all benefit criteria.
        """
        matrix = np.array([[7, 15, 44, 37, 68],
                           [93, 14, 7, 35, 100],
                           [11, 85, 24, 85, 27]])
        body = methods.RVIKOR(np.array([[1, 100]] * 5))
        nmatrix, S, R, NQ = [table.data for table in
                             body(matrix, np.ones(5) / 5, np.ones(5), verbose=True).results]

        self.assertListEqual([[0.0606, 0.1414, 0.4343, 0.3636, 0.6768],
                              [0.9293, 0.1313, 0.0606, 0.3434, 1.0],
                              [0.101, 0.8485, 0.2323, 0.8485, 0.2626]], np.round(nmatrix, 4).tolist())
        self.assertListEqual([0.6646, 0.5071, 0.5414], np.round(S, 4).tolist())
        self.assertListEqual([0.1879, 0.1879, 0.1798], np.round(R, 4).tolist())
        self.assertListEqual([0.802, 0.7232, 0.7202], np.round(NQ, 4).tolist())
        self.assertListEqual([3, 2, 1], body.rank(NQ).astype(int).tolist())

    matrix = np.array([[78, 56, 34, 6],
                       [4, 45, 3, 97],
                       [18, 2, 50, 63],
                       [9, 14, 11, 92],
                       [85, 9, 100, 29]])
    weights = np.ones(4) / 4
    types = np.ones(4)
    bounds = np.array([[0, 100]] * 4)

    def test_output(self):
        """ Example 2 (Table 3): equal weights, domain [0, 100]. The paper rounds NQ values ending with 5 at the
            fifth decimal place down (e.g. 0.79875 to 0.7987), so they are compared with five decimal places.
        """
        body = methods.RVIKOR(self.bounds)
        _, S, R, NQ = [table.data for table in body(self.matrix, self.weights, self.types, verbose=True).results]

        self.assertListEqual([0.565, 0.6275, 0.6675, 0.685, 0.4425], np.round(S, 4).tolist())
        self.assertListEqual([0.235, 0.2425, 0.245, 0.2275, 0.2275], np.round(R, 4).tolist())
        self.assertListEqual([0.7525, 0.79875, 0.82375, 0.7975, 0.67625], np.round(NQ, 5).tolist())
        self.assertListEqual([2, 4, 5, 3, 1], body.rank(NQ).astype(int).tolist())

    def test_rank_preservation(self):
        """ Deleting A3 (Table 4) and adding A+ or A- (Eqs. 28-31) does not change the scores of the other
            alternatives.
        """
        body = methods.RVIKOR(self.bounds)
        scores = body(self.matrix, self.weights, self.types)

        deleted = body(np.delete(self.matrix, 2, axis=0), self.weights, self.types)
        np.testing.assert_allclose(np.delete(scores, 2), deleted)
        self.assertListEqual([2, 4, 3, 1], body.rank(deleted).astype(int).tolist())

        for added, position in (([100, 100, 100, 100], 1), ([0, 0, 0, 0], 6)):
            with self.subTest(added=added):
                extended = body(np.vstack([self.matrix, added]), self.weights, self.types)
                np.testing.assert_allclose(scores, extended[:-1])
                self.assertEqual(position, body.rank(extended)[-1])

    def test_cost_criteria(self):
        """ Cost criteria are normalized as (M - f) / (M - m) (Eq. 10). """
        types = np.array([1, 1, 1, -1])
        matrix = self.matrix.copy()
        matrix[:, 3] = 100 - matrix[:, 3]
        np.testing.assert_allclose(methods.RVIKOR(self.bounds)(self.matrix, self.weights, self.types),
                                   methods.RVIKOR(self.bounds)(matrix, self.weights, types))

    def test_validation(self):
        with self.assertRaises(ValueError):
            methods.RVIKOR(self.bounds, v=1.5)
        with self.assertRaises(ValueError):
            methods.RVIKOR(np.array([[0, 50]] * 4))(self.matrix, self.weights, self.types)
        clipped = methods.RVIKOR(np.array([[0, 50]] * 4), clip=True)(self.matrix, self.weights, self.types)
        self.assertEqual(len(clipped), 5)
