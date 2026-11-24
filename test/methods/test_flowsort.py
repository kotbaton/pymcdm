# Copyright (c) 2026 Bartlomiej Kizielewicz
import unittest
import numpy as np

from pymcdm.methods.sorting import FLOWSORT


class TestFLOWSORT(unittest.TestCase):
    """ Test output method with reference:
    [1] Nemery, P., & Lamboray, C. (2008). FlowSort: a flow-based sorting method with limiting or central profiles.
    TOP, 16(1), 90-113.

    Illustrative example of Section 3.4: five criteria with equal weights (1/5, the paper uses 1 for each criterion
    and normalized preference degrees) and the actions of Table 3. The paper numbers the categories from 1 (the best)
    to 4 (the worst); here they are numbered from 1 (the worst), so the paper's category C_h is 5 - h.
    """

    matrix = np.array([[54, 17, 71, 45, 63],
                       [15, 5, 19, 9, 23],
                       [25, 25, 50, 75, 75]])
    weights = np.ones(5) / 5
    types = np.ones(5)

    def tables(self, body):
        return [table.data for table in body(self.matrix, self.weights, self.types, verbose=True).results]

    def test_limiting_profiles(self):
        """ Limiting profiles of Table 1 with the usual criterion (q = p = 0, Table 2): flows of Table 5 and
            assignments of Table 6. Table 6 and the text give the categories of the positive and of the negative
            flows of a1 and a3 the other way round (2 and 3 instead of 3 and 2) than the assignment rules of
            Section 3.1 with the flows of Table 5; the rules agree with Proposition 4, by which the category of the
            negative flow is at least as good as the category of the positive flow. Table 5 also gives the net
            flows of r3 and r4 in R1 as -0.14 and -0.48, while its positive and negative flows give -0.04 and
            -0.52.
        """
        profiles = np.array([[0] * 5, [25] * 5, [50] * 5, [75] * 5, [100] * 5])
        phi_plus_r, phi_minus_r, phi_r, phi_a, categories_all, categories = self.tables(FLOWSORT(profiles))

        # Flows of the profiles r5, ..., r1 and of the actions (Table 5)
        self.assertListEqual([[0, 0.24, 0.48, 0.8, 1], [0, 0.4, 0.6, 0.8, 1], [0, 0.2, 0.48, 0.72, 1]],
                             np.round(phi_plus_r, 2).tolist())
        self.assertListEqual([[1, 0.76, 0.52, 0.2, 0], [1, 0.6, 0.4, 0.2, 0], [1, 0.72, 0.48, 0.2, 0]],
                             np.round(phi_minus_r, 2).tolist())
        self.assertListEqual([[0.48, 0.52, -0.04], [0.2, 0.8, -0.6], [0.4, 0.4, 0.0]],
                             np.round(phi_a, 2).tolist())

        # Categories of the positive, negative and net flows: C3/C2/C3, C4/C4/C4 and C3/C2/C3 in the paper
        self.assertListEqual([[2, 3, 2], [1, 1, 1], [2, 3, 2]], categories_all.tolist())
        self.assertListEqual([2, 1, 2], categories.tolist())

    def test_central_profiles(self):
        """ Central profiles of Table 7 with the linear preference function and the thresholds of Table 8: flows
            of Table 10, a1 and a3 are assigned to C2 and a2 to C4 with all three rules. Table 9 gives 0.95 for the
            preference of r3 over a2, the exact value is 0.9556.
        """
        profiles = np.array([[10, 5, 10, 10, 15],
                             [40, 35, 35, 30, 33],
                             [56, 62, 58, 61, 52],
                             [80, 90, 90, 75, 82]])
        body = FLOWSORT(profiles, 'vshape_2', q=[4, 6, 0, 2, 3], p=[8, 13, 7, 5, 12], profiles_type='central')
        phi_plus_r, phi_minus_r, phi_r, phi_a, categories_all, categories = self.tables(body)

        self.assertListEqual([[0, 0.3, 0.6, 1], [0, 0.49, 0.75, 1], [0, 0.33, 0.65, 0.92]],
                             np.round(phi_plus_r, 2).tolist())
        self.assertListEqual([[0.99, 0.7, 0.34, 0], [0.84, 0.5, 0.25, 0], [1, 0.65, 0.35, 0]],
                             np.round(phi_minus_r, 2).tolist())
        self.assertListEqual([[0.54, 0.4, 0.14], [0.09, 0.74, -0.65], [0.5, 0.4, 0.1]],
                             np.round(phi_a, 2).tolist())
        self.assertListEqual([[3, 3, 3], [1, 1, 1], [3, 3, 3]], categories_all.tolist())
        self.assertListEqual([3, 1, 3], categories.tolist())

    def test_profiles_are_assigned_to_their_categories(self):
        """ An action with the same performances as a centroid is assigned to its category (Section 3.2). """
        profiles = np.array([[10, 5, 10, 10, 15],
                             [40, 35, 35, 30, 33],
                             [56, 62, 58, 61, 52],
                             [80, 90, 90, 75, 82]])
        body = FLOWSORT(profiles, 'vshape_2', q=[4, 6, 0, 2, 3], p=[8, 13, 7, 5, 12], profiles_type='central')
        self.assertListEqual([1, 2, 3, 4], body(profiles, self.weights, self.types).tolist())

    def test_independent_of_other_alternatives(self):
        """ Each action is compared with the profiles only. """
        profiles = np.array([[0] * 5, [25] * 5, [50] * 5, [75] * 5, [100] * 5])
        body = FLOWSORT(profiles)
        alone = [body(row[None, :], self.weights, self.types)[0] for row in self.matrix]
        self.assertListEqual(alone, body(self.matrix, self.weights, self.types).tolist())

    def test_profiles_validation(self):
        """ Profiles have to be ordered and strictly preferred (Conditions 1 and 6). """
        with self.assertRaises(ValueError):
            FLOWSORT(np.array([[0] * 5, [50] * 5, [25] * 5]))(self.matrix, self.weights, self.types)
        # An indifference threshold larger than the difference of the profiles violates Condition 6
        with self.assertRaises(ValueError):
            FLOWSORT(np.array([[0] * 5, [25] * 5, [50] * 5]), 'ushape', q=[30] * 5)(
                self.matrix, self.weights, self.types)
        with self.assertRaises(ValueError):
            FLOWSORT(np.array([[0] * 5, [25] * 5]))
        with self.assertRaises(ValueError):
            FLOWSORT(np.array([[0] * 5, [25] * 5, [50] * 5]), rule='mean')
        with self.assertRaises(NotImplementedError):
            FLOWSORT(np.array([[0] * 5, [25] * 5, [50] * 5])).rank(np.array([1, 2]))
