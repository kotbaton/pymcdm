# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .. import helpers
from .. import normalizations

from .mcda_method import MCDA_method
from ..io import TableDesc


class ERVD(MCDA_method):
    """ Election based on Relative Value Distances method [#ervd1]_.

    References
    ----------
    .. [#ervd1] Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method
                based on relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.

    Examples
    --------
    >>> matrix = np.array([
    ...     [80, 70, 87, 77, 76, 80, 75],
    ...     [85, 65, 76, 80, 75, 65, 75],
    ...     [78, 90, 72, 80, 85, 90, 85],
    ...     [75, 84, 69, 85, 65, 65, 70],
    ...     [84, 67, 60, 75, 85, 75, 80],
    ...     [85, 78, 82, 81, 79, 80, 80],
    ...     [77, 83, 74, 70, 71, 65, 70],
    ...     [78, 82, 72, 80, 78, 70, 60],
    ...     [85, 90, 80, 88, 90, 80, 85],
    ...     [89, 75, 79, 67, 77, 70, 75],
    ...     [65, 55, 68, 62, 70, 50, 60],
    ...     [70, 64, 65, 65, 60, 60, 65],
    ...     [95, 80, 70, 75, 70, 75, 75],
    ...     [70, 80, 79, 80, 85, 80, 70],
    ...     [60, 78, 87, 70, 66, 70, 65],
    ...     [92, 85, 88, 90, 85, 90, 95],
    ...     [86, 87, 80, 70, 72, 80, 85]
    ... ])
    >>> weights = np.array([0.066, 0.196, 0.066, 0.130, 0.130, 0.216, 0.196])
    >>> types = np.ones(7)
    >>> ref = np.ones(7) * 80
    >>> ervd = ERVD(ref_point=ref)
    >>> pref = ervd(matrix, weights, types)
    >>> rank = ervd.rank(pref)
    >>> print(pref)
    [0.66  0.503 0.885 0.521 0.61  0.796 0.498 0.549 0.908 0.565 0.07  0.199 0.632 0.716 0.438 0.972 0.767]
    >>> print(rank)
    [ 7. 13.  3. 12.  9.  4. 14. 11.  2. 10. 17. 16.  8.  6. 15.  1.  5.]
    """
    _tables = [
        TableDesc(caption='Reference point for alternatives evaluation',
                  label='ref_point', symbol='$\\mu_j$', rows='C', cols=None),
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Normalized reference point',
                  label='norm_ref_point', symbol='$\\varphi_j$', rows='C', cols=None),
        TableDesc(caption='Matrix of relative performance of alternatives',
                  label='rp_matrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Positive ideal solution',
                  label='pis', symbol='$A^{+}_j$', rows='C', cols=None),
        TableDesc(caption='Negative ideal solution',
                  label='nis', symbol='$A^{-}_j$', rows='C', cols=None),
        TableDesc(caption='Individual separation measures from the PIS',
                  label='ind_sep_pis', symbol='$S^{+}_i$', rows='A', cols=None),
        TableDesc(caption='Individual separation measures from the NIS',
                  label='ind_sep_nis', symbol='$S^{-}_i$', rows='A', cols=None),
        TableDesc(caption='Final preference values (relative closeness)',
                  label='pref', symbol='$\\phi_i$', rows='A', cols=None),
    ]

    def __init__(self, ref_point, lambd=2.25, alpha=0.88):
        """ Create ERVD method object.

        Parameters
        ----------
            ref_point : ndarray or None
                Reference point for alternatives evaluation. Should be one dimension array with reference
                value for each criterion.

            lam : float
                Lambda parameter. See [1] for detailed description. Default is 2.25.

            alpha : float
                Alpha parameter. See [1] for detailed description. Default is 2.25.

        References
        ----------
        .. [1] Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method
               based on relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.
        """
        self.lambd = lambd
        self.alpha = alpha
        self.ref_point = np.asarray(ref_point)

    def _method(self, matrix, weights, types):
        ref = self.ref_point
        lambd = self.lambd
        alpha = self.alpha

        nmatrix = helpers.normalize_matrix(matrix, normalizations.sum_normalization, None)
        nref = ref / matrix.sum(axis=0)

        vnmatrix = nmatrix.copy()
        for j in range(nmatrix.shape[1]):
            if types[j] == 1:
                ind = (nmatrix[:, j] > nref[j])
                vnmatrix[ind, j] = (nmatrix[ind, j] - nref[j]) ** alpha
                vnmatrix[~ind, j] = - lambd * (nref[j] - nmatrix[~ind, j]) ** alpha
            else:
                ind = (nmatrix[:, j] < nref[j])
                vnmatrix[ind, j] = (nref[j] - nmatrix[ind, j]) ** alpha
                vnmatrix[~ind, j] = - lambd * (nmatrix[~ind, j] - nref[j]) ** alpha

        v_plus = np.max(vnmatrix, axis=0)
        v_minus = np.min(vnmatrix, axis=0)

        S_plus = np.sum(weights * np.abs(vnmatrix - v_plus), axis=1)
        S_minus = np.sum(weights * np.abs(vnmatrix - v_minus), axis=1)

        p = S_minus / (S_plus + S_minus)
        return ref, nmatrix, nref, vnmatrix, v_plus, v_minus, S_plus, S_minus, p
