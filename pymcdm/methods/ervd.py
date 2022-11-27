import numpy as np

from pymcdm import helpers
from pymcdm import normalizations

from pymcdm.methods.mcda_method import MCDA_method

class ERVD(MCDA_method):
    def __call__(self, matrix, weights, types, ref, *args, lambd=2.25, alpha=0.88, **kwargs):
        ERVD._validate_input_data(matrix, weights, types)
        return ERVD._ervd(matrix, weights, types, ref, lambd, alpha)

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

        phi = S_minus / (S_plus + S_minus)

        return phi


def main():
    np.set_printoptions(suppress=True, precision=3)

    matrix = np.array([
        [80, 70, 87, 77, 76, 80, 75],
        [85, 65, 76, 80, 75, 65, 75],
        [78, 90, 72, 80, 85, 90, 85],
        [75, 84, 69, 85, 65, 65, 70],
        [84, 67, 60, 75, 85, 75, 80],
        [85, 78, 82, 81, 79, 80, 80],
        [77, 83, 74, 70, 71, 65, 70],
        [78, 82, 72, 80, 78, 70, 60],
        [85, 90, 80, 88, 90, 80, 85],
        [89, 75, 79, 67, 77, 70, 75],
        [65, 55, 68, 62, 70, 50, 60],
        [70, 64, 65, 65, 60, 60, 65],
        [95, 80, 70, 75, 70, 75, 75],
        [70, 80, 79, 80, 85, 80, 70],
        [60, 78, 87, 70, 66, 70, 65],
        [92, 85, 88, 90, 85, 90, 95],
        [86, 87, 80, 70, 72, 80, 85]
    ])

    weights = np.array([0.066, 0.196, 0.066, 0.130, 0.130, 0.216, 0.196])
    types = np.ones(7)

    ref = np.ones(7) * 80

    ervd = ERVD()
    pref = ervd(matrix, weights, types, ref=ref)
    rank = ervd.rank(pref)

    print(pref, rank)


if __name__=='__main__':
    main()
