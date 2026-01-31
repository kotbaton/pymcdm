# Copyright (c) 2026 Andrii Shekhovtsov

import numpy as np
from .spotis import SPOTIS
from ..io import TableDesc

class BalancedSPOTIS(SPOTIS):
    """ Balanced Stable Preference Ordering Towards Ideal Solution (Balanced SPOTIS) method.

        The Balanced SPOTIS method is an extension of the SPOTIS method that incorporates
        an ESP trust parameter, allowing for a balanced consideration of both the Ideal Solution Point (ISP)
        and the Expected Solution Point (ESP) in the evaluation of decision alternatives.
        [#balanced_spotis1]_.

        Parameters
        ----------
            bounds : ndarray
                Decision problem bounds / criteria bounds. Should be two-dimensional array with [min, max] value
                for in criterion in rows.

            esp : ndarray
                Expected Solution Point for alternatives evaluation. Should be an array with ideal (expected) value
                for each criterion.

            alpha : float
                ESP trust parameter, ranging from 0 to 1. A value of 0 means full trust in ISP,
                while a value of 1 mean full trust in ESP. Default is 0.5.

        References
        ----------
        .. [#balanced_spotis1] Shekhovtsov, A., Dezert, J. and Sałabun, W. (2025).
           Enhancing Personalized Decision-Making with the Balanced SPOTIS Algorithm.
           In Proceedings of the 17th International Conference on Agents and Artificial
           Intelligence - Volume 3: ICAART; ISBN 978-989-758-737-5; ISSN 2184-433X,
           SciTePress, pages 264-271. DOI: 10.5220/0013119800003890

    """
    _reverse_ranking = False
    _tables = [
        TableDesc(caption='Expected Solution Point (ESP)',
                  label='esp', symbol='$S^{+}$', rows='C', cols=None),
        TableDesc(caption='Ideal Solution Point (ISP)',
                  label='isp', symbol='$S^{*}$', rows='C', cols=None),
        TableDesc(caption='Normalized distances from ESP',
                  label='dij_esp', symbol='$d_{ij}(A_i, S^{+}_j)$', rows='A', cols='C'),
        TableDesc(caption='Normalized distances from ISP',
                  label='dij_isp', symbol='$d_{ij}(A_i, S^{*}_j)$', rows='A', cols='C'),
        TableDesc(caption='Weighted average distance from ESP',
                  label='Di_esp', symbol='$d_{i}(A_i, S^{+})$', rows='A', cols=None),
        TableDesc(caption='Weighted average distance from ISP',
                  label='Di_isp', symbol='$d_{i}(A_i, S^{*})$', rows='A', cols=None),
        TableDesc(caption='Balanced distance from ESP and ISP',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def __init__(self, bounds, esp, alpha=0.5):
        """ Create Balanced SPOTIS method object.

        Parameters
        ----------
            bounds : ndarray
                Decision problem bounds / criteria bounds. Should be two-dimensional array with [min, max] value
                for in criterion in rows.

            esp : ndarray
                Expected Solution Point for alternatives evaluation. Should be an array with ideal (expected) value
                for each criterion.

            alpha : float
                ESP trust parameter, ranging from 0 to 1. A value of 0 means full trust in ISP,
                while a value of 1 mean full trust in ESP. Default is 0.5.
        """
        super().__init__(bounds, esp)
        self.alpha = alpha


    def _method(self, matrix, weights, types):
        alpha = self.alpha
        bounds = self.bounds
        esp = self.esp
        isp = bounds[np.arange(bounds.shape[0]), ((types + 1) // 2).astype('int')]

        dij = matrix.astype(float)

        dij_esp = np.abs((dij - esp) /
                         (bounds[:, 0] - bounds[:, 1]))

        dij_isp = np.abs((dij - isp) /
                         (bounds[:, 0] - bounds[:, 1]))

        Di_esp = np.sum(dij_esp * weights, axis=1)
        D_isp = np.sum(dij_isp * weights, axis=1)

        P_i = (1 - alpha) * D_isp + alpha * Di_esp

        return esp, isp, dij_esp, dij_isp, Di_esp, D_isp, P_i