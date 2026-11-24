# Copyright (c) 2023-2026 Andrii Shekhovtsov
# Copyright (c) 2022-2026 Bartlomiej Kizielewicz
import unittest

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pymcdm import visuals


class TestPolarPlots(unittest.TestCase):
    """ Polar plots create polar axes when no axes are given (plt.gca(projection=...) was removed in
        Matplotlib 3.6).
    """

    def tearDown(self):
        plt.close('all')

    def test_polar_plot(self):
        rankings = np.array([[1, 2, 3, 4], [2, 1, 3, 4], [1, 3, 2, 4]])
        ax = visuals.polar_plot(rankings)
        self.assertEqual(ax.name, 'polar')

    def test_polar_weights(self):
        weights = np.array([[0.2, 0.3, 0.5], [0.1, 0.4, 0.5]])
        ax = visuals.polar_weights(weights)
        self.assertEqual(ax.name, 'polar')

    def test_polar_plot_reuses_polar_axes(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='polar')
        self.assertIs(visuals.polar_plot(np.array([[1, 2, 3], [2, 1, 3]])), ax)

    def test_polar_plot_on_cartesian_figure(self):
        plt.figure()
        plt.plot([0, 1], [0, 1])
        ax = visuals.polar_plot(np.array([[1, 2, 3], [2, 1, 3]]))
        self.assertEqual(ax.name, 'polar')


class TestMIDIAPlane(unittest.TestCase):
    """ midia_plane draws the alternatives in the (DI, DAI) plane, coloured or with contour lines only. """

    def setUp(self):
        from pymcdm.methods import MIDIA
        matrix = np.array([[20, 3, 91, 50, 80], [16, 50, 100, 11, 62], [11, 50, 97, 25, 68],
                           [10, 100, 85, 10, 50], [2, 36, 76, 5, 53]])
        res = MIDIA(0.5)(matrix, np.ones(5) / 5, np.ones(5), verbose=True)
        self.DI, self.DAI = res.results[1].data, res.results[2].data

    def tearDown(self):
        plt.close('all')

    def test_fill_with_colorbar(self):
        fig, ax = plt.subplots()
        out = visuals.midia_plane(self.DI, self.DAI, ax=ax)
        self.assertEqual(len(out), 2)
        self.assertIs(out[0], ax)
        self.assertEqual(out[1].get_ylim(), (0.0, 1.0))
        self.assertEqual(len(ax.texts), 5)

    def test_fill_without_colorbar(self):
        fig, ax = plt.subplots()
        self.assertIs(visuals.midia_plane(self.DI, self.DAI, colorbar=False, ax=ax), ax)
        self.assertEqual(len(fig.axes), 1)

    def test_lines_only(self):
        fig, ax = plt.subplots()
        self.assertIs(visuals.midia_plane(self.DI, self.DAI, fill=False, ax=ax), ax)
        self.assertEqual(len(fig.axes), 1)
        # 5 alternatives and 4 labelled lines
        self.assertEqual(len(ax.texts), 9)

    def test_extreme_alpha(self):
        for alpha in (0, 1):
            for fill in (True, False):
                fig, ax = plt.subplots()
                visuals.midia_plane(self.DI, self.DAI, alpha=alpha, fill=fill, ax=ax)

    def test_invalid_alpha(self):
        with self.assertRaises(ValueError):
            visuals.midia_plane(self.DI, self.DAI, alpha=1.5)


class TestFlowSortFlows(unittest.TestCase):
    """ flowsort_flows draws the three flows of an alternative against the profiles. """

    def setUp(self):
        from pymcdm.methods.sorting import FLOWSORT
        self.FLOWSORT = FLOWSORT
        self.matrix = np.array([[54, 17, 71, 45, 63], [25, 25, 50, 75, 75]])
        self.profiles = np.array([[0] * 5, [25] * 5, [50] * 5, [75] * 5, [100] * 5])

    def tearDown(self):
        plt.close('all')

    def flows(self, **kwargs):
        res = self.FLOWSORT(self.profiles, **kwargs)(self.matrix, np.ones(5) / 5, np.ones(5), verbose=True)
        return [r.data for r in res.results[:4]]

    def test_limiting(self):
        fig, ax = plt.subplots()
        p, m, n, a = self.flows()
        self.assertIs(visuals.flowsort_flows(p[1], m[1], n[1], a[1], ax=ax), ax)
        # 3 flows x 4 categories
        self.assertEqual(len(ax.patches), 12)

    def test_central(self):
        fig, ax = plt.subplots()
        p, m, n, a = self.flows(profiles_type='central')
        visuals.flowsort_flows(p[0], m[0], n[0], a[0], profiles_type='central', ax=ax)
        # 3 flows x 5 categories
        self.assertEqual(len(ax.patches), 15)

    def test_invalid_profiles_type(self):
        p, m, n, a = self.flows()
        with self.assertRaises(ValueError):
            visuals.flowsort_flows(p[0], m[0], n[0], a[0], profiles_type='other')


class TestSortingAssignments(unittest.TestCase):
    """ sorting_assignments draws the assigned categories and optional intervals. """

    def tearDown(self):
        plt.close('all')

    def test_categories(self):
        fig, ax = plt.subplots()
        self.assertIs(visuals.sorting_assignments([1, 3, 2], 4, ax=ax), ax)
        self.assertEqual([t.get_text() for t in ax.get_yticklabels()], ['$A_{3}$', '$A_{2}$', '$A_{1}$'])
        self.assertEqual(len(ax.get_xticks()), 4)

    def test_intervals(self):
        fig, ax = plt.subplots()
        visuals.sorting_assignments([1, 3, 2], 3, intervals=[[1, 2], [3, 3], [1, 3]], labels=['a', 'b', 'c'],
                                    ax=ax)
        from matplotlib.patches import FancyBboxPatch
        self.assertEqual(sum(isinstance(p, FancyBboxPatch) for p in ax.patches), 3)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            visuals.sorting_assignments([1, 5], 4)
        with self.assertRaises(ValueError):
            visuals.sorting_assignments([1, 2], 4, intervals=[[1, 2]])


class TestWeightsIntervals(unittest.TestCase):
    """ weights_intervals draws one bar for each interval and optional markers of the weights. """

    def tearDown(self):
        plt.close('all')

    def test_intervals_and_weights(self):
        from pymcdm.weights.subjective import BWM
        bwm = BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 4, 2, 1])
        lower, upper = bwm.get_weight_intervals()
        fig, ax = plt.subplots()
        self.assertIs(visuals.weights_intervals(lower, upper, bwm(), ax=ax), ax)
        self.assertEqual(len(ax.patches), 5)
        np.testing.assert_allclose([p.get_x() for p in ax.patches], lower)
        np.testing.assert_allclose([p.get_x() + p.get_width() for p in ax.patches], upper)
        # The first criterion is at the top
        self.assertEqual([t.get_text() for t in ax.get_yticklabels()], [f'$C_{{{j}}}$' for j in range(1, 6)])
        self.assertEqual(list(ax.get_yticks()), [4, 3, 2, 1, 0])
        self.assertEqual(len(ax.collections), 1)

    def test_without_weights(self):
        fig, ax = plt.subplots()
        visuals.weights_intervals([0.1, 0.2], [0.3, 0.2], labels=['a', 'b'], ax=ax)
        self.assertEqual(len(ax.collections), 0)
        # Both ends of every interval are drawn, also of the degenerate one
        self.assertEqual(len(ax.lines), 4)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            visuals.weights_intervals([0.3, 0.2], [0.2, 0.4])
        with self.assertRaises(ValueError):
            visuals.weights_intervals([0.1, 0.2], [0.2, 0.4, 0.5])
        with self.assertRaises(ValueError):
            visuals.weights_intervals([0.1, 0.2], [0.2, 0.4], weights=[0.5])


class TestSimosCards(unittest.TestCase):
    """ simos_cards draws a card for each criterion and each white card. """

    r = [[2, 6, 11], [3], [1, 5, 8, 9], [4], [0, 7], [10]]
    w_c = [0, 1, 0, 0, 0]

    def tearDown(self):
        plt.close('all')

    def test_cards(self):
        from pymcdm.weights.subjective import SRF
        weights = SRF(r=self.r, w_c=self.w_c, z=6.5, w=1)()
        fig, ax = plt.subplots()
        self.assertIs(visuals.simos_cards(self.r, self.w_c, weights=weights, ax=ax), ax)
        # 12 criteria and 1 white card
        self.assertEqual(len(ax.patches), 13)
        texts = [t.get_text() for t in ax.texts]
        self.assertIn('15.3%', texts)
        self.assertIn('$C_{11}$', texts)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            visuals.simos_cards(self.r, [0, 1])
        with self.assertRaises(ValueError):
            visuals.simos_cards(self.r, [0, 0.5, 0, 0, 0])


class TestPairwiseMatrix(unittest.TestCase):
    """ pairwise_matrix draws a heatmap of the comparisons with the Saaty scale fractions. """

    matrix = [[1, 3, 7, 5], [1 / 3, 1, 5, 3], [1 / 7, 1 / 5, 1, 1 / 3], [1 / 5, 1 / 3, 3, 1]]

    def tearDown(self):
        plt.close('all')

    def test_values(self):
        fig, ax = plt.subplots()
        self.assertIs(visuals.pairwise_matrix(self.matrix, ax=ax), ax)
        texts = [t.get_text() for t in ax.texts]
        self.assertEqual(texts[:4], ['1', '3', '7', '5'])
        self.assertEqual(texts[8:12], ['1/7', '1/5', '1', '1/3'])

    def test_decimals_and_colorbar(self):
        fig, ax = plt.subplots()
        out = visuals.pairwise_matrix([[1, 2.5], [0.4, 1]], fractions=False, colorbar=True, ax=ax)
        self.assertEqual(len(out), 2)
        self.assertEqual([t.get_text() for t in ax.texts], ['1', '2.50', '0.40', '1'])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            visuals.pairwise_matrix([[1, 2, 3], [0.5, 1, 2]])
        with self.assertRaises(ValueError):
            visuals.pairwise_matrix([[1, 0], [0, 1]])
