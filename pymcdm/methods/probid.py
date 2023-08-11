import numpy as np

from pymcdm import helpers
from pymcdm import normalizations

from pymcdm.methods.mcda_method import MCDA_method

class PROBID(MCDA_method):
    """ Preference Ranking on the Basis of Ideal-Average Distance Method.

    References
    ----------
    .. [1] Wang, Z., Rangaiah, G. P., & Wang, X. (2021). Preference ranking on the basis of ideal-average distance method for multi-criteria decision-making. Industrial & Engineering Chemistry Research, 60(30), 11216-11230.

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

    def __init__(self, sPROBID=False):
        """ Creates a PROBID method object.

        Parameters
        ----------
            sPROBID : bool
                Determine if sPROBID variation should be used. Default is False, therefore the full procedure of the PROBID method is used.
        """
        self.sPROBID = sPROBID

    def __call__(self, matrix, weights, types, *args, **kwargs):
        """ Rank alternatives from decision matrix `matrix`, with criteria weights `weights` and criteria types `types`.

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
        PROBID._validate_input_data(matrix, weights, types)
        return PROBID._probid(matrix, weights, types, self.sPROBID)

    @staticmethod
    def _probid(matrix, weights, types, sPROBID):
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

        m = wnmatrix.shape[0]

        Si_pos_ideal = np.zeros(m)
        Si_neg_ideal = np.zeros(m)
        if not sPROBID:
            if m % 2 == 1:
                lim = (m + 1) // 2
            else:
                lim = m // 2

            for k in range(1, lim + 1):
                Si_pos_ideal += Si[:, k - 1] / k

            for k in range(lim, m + 1):
                Si_neg_ideal += Si[:, k - 1] / (m - k + 1)

            Ri = Si_pos_ideal / Si_neg_ideal
            return 1 / (1 + Ri**2) + Si_average

        else:
            if m >= 4:
                for k in range(1, m // 4 + 1):
                    Si_pos_ideal += Si[:, k - 1] / k

                for k in range(m + 1 - (m // 4), m + 1):
                    Si_neg_ideal += Si[:, k - 1] / (m - k + 1)

            else:
                Si_pos_ideal = Si[0]
                Si_neg_ideal = Si[-1]

            return Si_neg_ideal / Si_pos_ideal
