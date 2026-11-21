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
