# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm.methods.partial import PROMETHEE_I


def promethee_i_relation(F_plus, F_minus, a, b):
    """ PROMETHEE I relation of a to b: 'P' (a outranks b), 'P-' (b outranks a), 'I' or 'R' (incomparable). """
    def outranks(x, y):
        return ((F_plus[x] > F_plus[y] and F_minus[x] <= F_minus[y])
                or (F_plus[x] >= F_plus[y] and F_minus[x] < F_minus[y]))
    if outranks(a, b):
        return 'P'
    if outranks(b, a):
        return 'P-'
    if np.isclose(F_plus[a], F_plus[b]) and np.isclose(F_minus[a], F_minus[b]):
        return 'I'
    return 'R'


class TestPROMETHEE_I(unittest.TestCase):
    """ Test output method with reference:
    [1] Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects: The PROMETHEE method.
    European Journal of Operational Research, 24(2), 228-238.
    """

    # Location of hydroelectric power stations (Table 2): types II, III, V, IV, I and VI of generalized criteria
    matrix = np.array([
        [80, 90, 6, 5.4, 8, 5],
        [65, 58, 2, 9.7, 1, 1],
        [83, 60, 4, 7.2, 4, 7],
        [40, 80, 10, 7.5, 7, 10],
        [52, 72, 6, 2.0, 3, 8],
        [94, 96, 7, 3.6, 5, 6],
    ])
    weights = np.ones(6) / 6
    types = np.array([-1, 1, -1, -1, -1, 1])
    kwargs = dict(preference_function=['ushape', 'vshape', 'vshape_2', 'level', 'usual', 'gaussian'],
                  q=[10, None, 0.5, 1, None, None],
                  p=[None, 30, 5, 6, None, None],
                  s=[None, None, None, None, None, 5])

    def test_preference_indices(self):
        """ Preference indices from Table 3. The paper rounds the values of the preference functions before
            averaging them, hence the differences up to 0.001.
        """
        body = PROMETHEE_I(**self.kwargs)
        _, pi_table, _ = body._method(self.matrix, self.weights, self.types)

        output = np.array([
            [0, 0.296, 0.250, 0.268, 0.100, 0.185],
            [0.462, 0, 0.389, 0.333, 0.296, 0.500],
            [0.236, 0.180, 0, 0.333, 0.056, 0.429],
            [0.399, 0.505, 0.305, 0, 0.223, 0.212],
            [0.444, 0.515, 0.487, 0.380, 0, 0.448],
            [0.286, 0.399, 0.250, 0.432, 0.133, 0],
        ])
        np.testing.assert_allclose(pi_table, output, atol=0.001)

    def test_output(self):
        """ Leaving and entering flows from Table 3. The paper gives sums of the preference indices, pymcdm divides
            them by m - 1 = 5. Each sum has five indices rounded in the paper up to 0.001, hence atol = 0.005.
        """
        F_plus, F_minus = PROMETHEE_I(**self.kwargs)(self.matrix, self.weights, self.types)

        np.testing.assert_allclose(5 * F_plus, [1.099, 1.980, 1.234, 1.644, 2.274, 1.500], atol=0.005)
        np.testing.assert_allclose(5 * F_minus, [1.827, 1.895, 1.681, 1.746, 0.808, 1.774], atol=0.005)

    def test_partial_preorder(self):
        """ Second example (Table 5): x1 and x2 are incomparable with x3 and x5, and x3 outranks x5, which
            outranks x4 (Fig. 14). Fig. 14 also draws an arc from x1 to x2, but the flows of the paper's model give
            phi+(x1) > phi+(x2) and phi-(x1) > phi-(x2), i.e. incomparability; the text does not discuss this pair.
        """
        matrix = np.array([
            [16, 6, 22, 7],
            [11, 14, 19, 12],
            [15, 11, 16, 10],
            [7, 19, 10, 8],
            [13, 12, 16, 11],
        ])
        body = PROMETHEE_I(['vshape_2', 'usual', 'gaussian', 'vshape'],
                           q=[2, None, None, None], p=[10, None, None, 6], s=[None, None, 7, None])
        F_plus, F_minus = body(matrix, np.ones(4) / 4, np.array([-1, -1, 1, 1]))

        for a in (0, 1):
            for b in (2, 4):
                self.assertEqual(promethee_i_relation(F_plus, F_minus, a, b), 'R')
        for a, b in ((2, 4), (4, 3), (0, 3), (1, 3), (2, 3)):
            self.assertEqual(promethee_i_relation(F_plus, F_minus, a, b), 'P')

    def test_same_function_for_all_criteria(self):
        """ A single preference function with per-criterion thresholds is equivalent to a list of functions. """
        matrix = self.matrix
        single = PROMETHEE_I('vshape_2', q=[1, 2, 0.5, 1, 1, 1], p=[20, 30, 5, 6, 5, 5])
        listed = PROMETHEE_I(['vshape_2'] * 6, q=[1, 2, 0.5, 1, 1, 1], p=[20, 30, 5, 6, 5, 5])
        for a, b in zip(single(matrix, self.weights, self.types), listed(matrix, self.weights, self.types)):
            np.testing.assert_allclose(a, b)

    def test_validation(self):
        with self.assertRaises(ValueError):
            PROMETHEE_I('cubic')
        with self.assertRaises(ValueError):
            PROMETHEE_I(['usual', 'ushape'], q=[None, None])
        with self.assertRaises(ValueError):
            PROMETHEE_I('gaussian', p=[1, 1])
        with self.assertRaises(ValueError):
            PROMETHEE_I(['usual', 'vshape', 'usual'], p=[None, 1])
        with self.assertRaises(ValueError):
            PROMETHEE_I(['usual', 'usual'])(self.matrix, self.weights, self.types)
