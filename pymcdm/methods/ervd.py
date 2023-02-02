import numpy as np

from pymcdm import helpers
from pymcdm import normalizations

from pymcdm.methods.mcda_method import MCDA_method

class ERVD(MCDA_method):
    """ Election based on Relative Value Distances method.

    References
    ----------
    .. [1] Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method based on relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.

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
    def __init__(self, ref_point=None, lam=2.25, alpha=0.88):
        """ Create ERVD method object.

        Parameters
        ----------
            ref_point : ndarray or None
                Reference point for alternatives evaluation. Should be one dimension array with reference value for each criterion. If None average value will be used.

            lam : float
                Lambda parameter. See [1] for detailed description. Default is 2.25.

            alpha : float
                Alpha parameter. See [1] for detailed description. Default is 2.25.

        References
        ----------
        .. [1] Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method based on relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.
        """
        self.ref_point = ref_point
        self.lam = lam
        self.alpha = alpha
        if ref_point is not None:
            self.ref_point = np.array(ref_point)

    def __call__(self, matrix, weights, types, *args, **kwargs):
        """Rank alternatives from decision matrix `matrix`, with criteria weights `weights` and criteria types `types`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : ndarray
                    Criteria weights. Sum of the weights should be 1. (e.g. sum(weights) == 1)

                types : ndarray
                    Array with definitions of criteria types:
                    1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.

                *args: is necessary for methods which reqiure some additional data.

                **kwargs: is necessary for methods which reqiure some additional data.

            Returns
            -------
                ndarray
                    Preference values for alternatives. Better alternatives have higher values.
        """
        ERVD._validate_input_data(matrix, weights, types)

        if self.ref_point is not None:
            if self.ref_point.shape[0] != matrix.shape[1]:
                raise ValueError(f'Len of the ref_point {self.ref_point.shape[0]} should be the same as number of the criteria {matrix.shape[1]}.')
        else:
            self.ref_point = np.mean(matrix, axis=0)

        return ERVD._ervd(matrix, weights, types, self.ref_point, self.lam, self.alpha)

    @staticmethod
    def _ervd(matrix, weights, types, ref, lambd, alpha):
        nmatrix = helpers.normalize_matrix(matrix, normalizations.sum_normalization, None)
        ref = ref / matrix.sum(axis=0)

        vnmatrix = nmatrix.copy()
        for j in range(nmatrix.shape[1]):
            if types[j] == 1:
                ind = (nmatrix[:, j] > ref[j])
                vnmatrix[ind, j] = (nmatrix[ind, j] - ref[j]) ** alpha
                vnmatrix[~ind, j] = - lambd * (ref[j] - nmatrix[~ind, j]) ** alpha
            else:
                ind = (nmatrix[:, j] < ref[j])
                vnmatrix[ind, j] = (ref[j] - nmatrix[ind, j]) ** alpha
                vnmatrix[~ind, j] = - lambd * (nmatrix[~ind, j] - ref[j]) ** alpha

        v_plus = np.max(vnmatrix, axis=0)
        v_minus = np.min(vnmatrix, axis=0)

        S_plus = np.sum(weights * np.abs(vnmatrix - v_plus), axis=1)
        S_minus = np.sum(weights * np.abs(vnmatrix - v_minus), axis=1)

        return S_minus / (S_plus + S_minus)
