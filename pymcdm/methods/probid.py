# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .. import helpers
from .. import normalizations

from ..methods.mcda_method import MCDA_method
from ..io import TableDesc

class PROBID(MCDA_method):
    """ Preference Ranking on the Basis of Ideal-Average Distance Method [#probid1]_.

    References
    ----------
    .. [#probid1] Wang, Z., Rangaiah, G. P., & Wang, X. (2021). Preference ranking on the basis of ideal-average distance method for multi-criteria decision-making. Industrial & Engineering Chemistry Research, 60(30), 11216-11230.

    Examples
    --------
    >>> matrix = np.array([
    ...     [1.679 * 10**6, 1.525 * 10**(-7), 3.747 * 10**(-5), 0.251, 2.917],
    ...     [2.213 * 10**6, 1.304 * 10**(-7), 3.250 * 10**(-5), 0.218, 6.633],
    ...     [2.461 * 10**6, 1.445 * 10**(-7), 3.854 * 10**(-5), 0.259, 0.553],
    ...     [2.854 * 10**6, 1.540 * 10**(-7), 3.970 * 10**(-5), 0.266, 1.597],
    ...     [3.107 * 10**6, 1.522 * 10**(-7), 3.779 * 10**(-5), 0.254, 2.905],
    ...     [3.574 * 10**6, 1.469 * 10**(-7), 3.297 * 10**(-5), 0.221, 6.378],
    ...     [3.932 * 10**6, 1.977 * 10**(-7), 3.129 * 10**(-5), 0.210, 11.381],
    ...     [4.383 * 10**6, 1.292 * 10**(-7), 3.142 * 10**(-5), 0.211, 9.929],
    ...     [4.988 * 10**6, 1.690 * 10**(-7), 3.767 * 10**(-5), 0.253, 8.459],
    ...     [5.497 * 10**6, 5.703 * 10**(-7), 3.012 * 10**(-5), 0.200, 18.918],
    ...     [5.751 * 10**6, 4.653 * 10**(-7), 3.017 * 10**(-5), 0.201, 17.517],
    ... ])
    >>> weights = np.array([0.1819, 0.2131, 0.1838, 0.1832, 0.2379])
    >>> types = np.array([1, -1, -1, -1, -1])
    >>> pr = methods.PROBID()
    >>> pref = np.round(pr(matrix, weights, types), 4)
    >>> print(pref)
    [0.8568, 0.7826, 0.9362, 0.9369, 0.9379, 0.8716, 0.5489, 0.7231, 0.7792, 0.3331, 0.3387]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Matrix of ideal solutions',
                  label='imatrix', symbol='$A_{(k)}$', rows='A', cols='C'),
        TableDesc(caption='Average ideal solution',
                  label='av_sol', symbol='$\\bar{v}_{j}$', rows='C', cols=None),
        TableDesc(caption='Euclidean distances between ideal solutions and alternatives',
                  label='dist', symbol='$S_{i(k)}$', rows='A', cols='A'),
        TableDesc(caption='Average Euclidean distance',
                  label='av_dist', symbol='$S_{i(avg)}$', rows='A', cols=None),
        TableDesc(caption='Overall positive-ideal distance',
                  label='pi_dist', symbol='$S_{i(pos-ideal)}$', rows='A', cols=None),
        TableDesc(caption='Overall negative-ideal distance',
                  label='ni_dist', symbol='$S_{i(neg-ideal)}$', rows='A', cols=None),
        TableDesc(caption='Vector of pos-ideal/neg-ideal ratio',
                  label='pos_neg_ratio', symbol='$R_i$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix,
                                           normalizations.vector_normalization,
                                           None)

        wnmatrix = nmatrix * weights

        pis_matrix = wnmatrix.copy()
        for i in range(wnmatrix.shape[1]):
            if types[i] == 1:
                pis_matrix[:, i] = np.sort(wnmatrix[:, i])[::-1]
            else:
                pis_matrix[:, i] = np.sort(wnmatrix[:, i])

        average_pis = np.mean(pis_matrix, axis=0)

        Si = np.zeros((wnmatrix.shape[0], wnmatrix.shape[0]))
        for i, alt in enumerate(wnmatrix):
            Si[i] = np.sqrt(np.sum((alt - pis_matrix)**2, axis=1))

        Si_average = np.sqrt(np.sum((wnmatrix - average_pis)**2, axis=1))

        return (nmatrix,
                wnmatrix,
                pis_matrix,
                average_pis,
                Si,
                Si_average,
                *self._final_preference_calculation(Si, Si_average))

    def _final_preference_calculation(self, Si, Si_average):
        m = Si.shape[0]

        Si_pos_ideal = np.zeros(m)
        Si_neg_ideal = np.zeros(m)

        if m % 2 == 1:
            lim = (m + 1) // 2
        else:
            lim = m // 2

        for k in range(1, lim + 1):
            Si_pos_ideal += Si[:, k - 1] / k

        for k in range(lim, m + 1):
            Si_neg_ideal += Si[:, k - 1] / (m - k + 1)

        Ri = Si_pos_ideal / Si_neg_ideal

        p = 1 / (1 + Ri**2) + Si_average
        return Si_pos_ideal, Si_neg_ideal, Ri, p
