import numpy as np

from pymcdm import helpers
from pymcdm import normalizations

from pymcdm.methods.mcda_method import MCDA_method

class PROBID(MCDA_method):
    def __call__(self, matrix, weights, types, *args, **kwargs):
        PROBID._validate_input_data(matrix, weights, types)
        return PROBID._probid(matrix, weights, types)

    @staticmethod
    def _probid(matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, normalizations.vector_normalization, None)

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

        m = (wnmatrix.shape[0] + 1) // 2

        Si_pos_ideal = np.zeros(wnmatrix.shape[0])
        for i in range(1, m + 1):
            Si_pos_ideal += Si[:, i - 1] / i

        Si_neg_ideal = np.zeros(wnmatrix.shape[0])
        for i in range(m, wnmatrix.shape[0] + 1):
            Si_neg_ideal += Si[:, i - 1] / (wnmatrix.shape[0] - i + 1)

        Ri = Si_pos_ideal / Si_neg_ideal

        Pi = 1 / (1 + Ri**2) + Si_average

        return Pi


def main():
    np.set_printoptions(suppress=True, precision=4)

    matrix = np.array([
        [1.679 * 10**6, 1.525 * 10**(-7), 3.747 * 10**(-5), 0.251, 2.917],
        [2.213 * 10**6, 1.304 * 10**(-7), 3.250 * 10**(-5), 0.218, 6.633],
        [2.461 * 10**6, 1.445 * 10**(-7), 3.854 * 10**(-5), 0.259, 0.553],
        [2.854 * 10**6, 1.540 * 10**(-7), 3.970 * 10**(-5), 0.266, 1.597],
        [3.107 * 10**6, 1.522 * 10**(-7), 3.779 * 10**(-5), 0.254, 2.905],
        [3.574 * 10**6, 1.469 * 10**(-7), 3.297 * 10**(-5), 0.221, 6.378],
        [3.932 * 10**6, 1.977 * 10**(-7), 3.129 * 10**(-5), 0.210, 11.381],
        [4.383 * 10**6, 1.292 * 10**(-7), 3.142 * 10**(-5), 0.211, 9.929],
        [4.988 * 10**6, 1.690 * 10**(-7), 3.767 * 10**(-5), 0.253, 8.459],
        [5.497 * 10**6, 5.703 * 10**(-7), 3.012 * 10**(-5), 0.200, 18.918],
        [5.751 * 10**6, 4.653 * 10**(-7), 3.017 * 10**(-5), 0.201, 17.517],
    ])

    weights = np.array([0.1819, 0.2131, 0.1838, 0.1832, 0.2379])
    types = np.array([1, -1, -1, -1, -1])

    pr = PROBID()
    pref = pr(matrix, weights, types)
    rank = pr.rank(pref)

    print(pref, rank)


if __name__=='__main__':
    main()
