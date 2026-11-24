# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm import methods

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

    def test_repeated_call_with_thresholds(self):
        matrix = np.array([[4, 3, 2],
                           [3, 2, 4],
                           [5, 1, 3]])
        weights = np.array([0.5, 0.3, 0.2])
        types = np.ones(3)

        bodies = [
            methods.PROMETHEE_II('vshape', p=[1, 1, 1]),
            methods.PROMETHEE_II('ushape', q=[1, 1, 1]),
            methods.PROMETHEE_II('vshape_2', p=[2, 2, 2], q=[1, 1, 1]),
        ]
        for body in bodies:
            first = body(matrix, weights, types)
            second = body(matrix, weights, types)
            np.testing.assert_array_equal(first, second)

    def test_thresholds_length(self):
        matrix = np.array([[4, 3, 2],
                           [3, 2, 4],
                           [5, 1, 3]])
        weights = np.array([0.5, 0.3, 0.2])
        types = np.ones(3)

        with self.assertRaises(ValueError):
            methods.PROMETHEE_II('vshape', p=[1, 1])(matrix, weights, types)
        with self.assertRaises(ValueError):
            methods.PROMETHEE_II('vshape_2', p=[2, 2, 2], q=[1, 1])

    def test_missing_thresholds(self):
        """ A preference function which needs thresholds cannot be used without them. """
        for name in ('ushape', 'vshape', 'level', 'vshape_2', 'gaussian'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                methods.PROMETHEE_II(name)


class TestPROMETHEE_IIBrans(unittest.TestCase):
    """ Test output method with reference:
    [1] Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects: The PROMETHEE method.
    European Journal of Operational Research, 24(2), 228-238.
    """

    def test_output(self):
        """ Net flows from Table 4 (sums of the preference indices, pymcdm divides them by m - 1 = 5) and the
            complete preorder of Fig. 13. The paper rounds the preference indices to 0.001, hence atol = 0.01 for
            the difference of two sums of five indices.
        """
        matrix = np.array([
            [80, 90, 6, 5.4, 8, 5],
            [65, 58, 2, 9.7, 1, 1],
            [83, 60, 4, 7.2, 4, 7],
            [40, 80, 10, 7.5, 7, 10],
            [52, 72, 6, 2.0, 3, 8],
            [94, 96, 7, 3.6, 5, 6],
        ])
        types = np.array([-1, 1, -1, -1, -1, 1])
        body = methods.PROMETHEE_II(['ushape', 'vshape', 'vshape_2', 'level', 'usual', 'gaussian'],
                                    q=[10, None, 0.5, 1, None, None],
                                    p=[None, 30, 5, 6, None, None],
                                    s=[None, None, None, None, None, 5])
        preferences = body(matrix, np.ones(6) / 6, types)

        np.testing.assert_allclose(5 * preferences, [-0.728, 0.085, -0.447, -0.102, 1.466, -0.274], atol=0.01)
        self.assertListEqual([6, 2, 5, 3, 1, 4], body.rank(preferences).astype(int).tolist())

    def test_output_second_example(self):
        """ Complete preorder x1 > x3 > x2 > x5 > x4 of the second example (Table 5, Fig. 15). """
        matrix = np.array([
            [16, 6, 22, 7],
            [11, 14, 19, 12],
            [15, 11, 16, 10],
            [7, 19, 10, 8],
            [13, 12, 16, 11],
        ])
        body = methods.PROMETHEE_II(['vshape_2', 'usual', 'gaussian', 'vshape'],
                                    q=[2, None, None, None], p=[10, None, None, 6], s=[None, None, 7, None])
        preferences = body(matrix, np.ones(4) / 4, np.array([-1, -1, 1, 1]))

        self.assertListEqual([1, 3, 2, 5, 4], body.rank(preferences).astype(int).tolist())
