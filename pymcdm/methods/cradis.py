# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class CRADIS(MCDA_method):
    """ Compromise Ranking of Alternatives from Distance to Ideal Solution (CRADIS) method [#cradis1]_.

        CRADIS combines steps of the ARAS, MARCOS and TOPSIS methods. The weighted normalized decision matrix is
        compared element by element with one ideal and one anti-ideal value (the largest and the smallest element of
        the whole matrix), and the total deviations of every alternative are related to those of the optimal
        alternative, built from the best weighted normalized value of every criterion.

        Since the best normalized value of every criterion is 1, the optimal alternative reaches the ideal value on
        every criterion if all weights are equal. Its deviation from the ideal solution is then 0, and so is the
        utility K+ of every alternative (Eq. 11 of [#cradis1]_): with equal weights the ranking depends on the
        deviations from the anti-ideal solution only. An alternative with no deviation from the ideal solution
        obtains K+ = 1.

        Read more in the User Guide.

        References
        ----------
        .. [#cradis1] Puška, A., Stević, Ž., & Pamučar, D. (2022). Evaluation and selection of healthcare waste
               incinerators using extended sustainability criteria and multi-criteria analysis methods. Environment,
               Development and Sustainability, 24(9), 11195-11225.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import CRADIS
        >>> matrix = np.array([[0.36, 30, 10.0, 5.02],
        ...                    [0.54, 40, 11.5, 6.26],
        ...                    [0.75, 50, 12.5, 8.97],
        ...                    [0.57, 65, 17.5, 8.79],
        ...                    [1.35, 100, 16.5, 11.68],
        ...                    [1.20, 100, 15.5, 12.90]])
        >>> weights = np.array([0.3, 0.2, 0.25, 0.25])
        >>> types = np.array([1, 1, -1, -1])
        >>> body = CRADIS()
        >>> preferences = body(matrix, weights, types)
        >>> np.round(preferences, 4).tolist()
        [0.4417, 0.4204, 0.4097, 0.3509, 0.5682, 0.5299]
        >>> body.rank(preferences).tolist()
        [3.0, 4.0, 5.0, 6.0, 1.0, 2.0]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$n_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Deviation from the ideal solution',
                  label='s_plus', symbol='$s_i^+$', rows='A', cols=None),
        TableDesc(caption='Deviation from the anti-ideal solution',
                  label='s_minus', symbol='$s_i^-$', rows='A', cols=None),
        TableDesc(caption='Utility in relation to the ideal solution',
                  label='k_plus', symbol='$K_i^+$', rows='A', cols=None),
        TableDesc(caption='Utility in relation to the anti-ideal solution',
                  label='k_minus', symbol='$K_i^-$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$Q_i$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        # Normalization (Eqs. 2-3)
        nmatrix = np.where(types == 1, matrix / np.max(matrix, axis=0), np.min(matrix, axis=0) / matrix)

        # Weighted normalized ("aggravated") decision matrix (Eq. 4)
        wmatrix = nmatrix * weights

        # Ideal and anti-ideal solution: the largest and the smallest element of the whole matrix (Eqs. 5-6)
        ideal, anti_ideal = np.max(wmatrix), np.min(wmatrix)

        # Total deviations from the ideal and anti-ideal solution (Eqs. 7-10)
        s_plus = np.sum(ideal - wmatrix, axis=1)
        s_minus = np.sum(wmatrix - anti_ideal, axis=1)

        # Deviations of the optimal alternative, built from the best value of every criterion
        optimal = np.max(wmatrix, axis=0)
        s0_plus = np.sum(ideal - optimal)
        s0_minus = np.sum(optimal - anti_ideal)

        # Utility functions (Eqs. 11-12) and the final score (Eq. 13)
        # An alternative equal to the ideal solution on every criterion is as good as the optimal alternative
        with np.errstate(divide='ignore', invalid='ignore'):
            k_plus = np.where(s_plus > 0, s0_plus / s_plus, 1.0)
        k_minus = s_minus / s0_minus
        pref = (k_plus + k_minus) / 2

        return nmatrix, wmatrix, s_plus, s_minus, k_plus, k_minus, pref
