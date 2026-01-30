# Copyright (c) 2020-2026 Andrii Shekhovtsov

import numpy as np
from warnings import warn

from .mcda_method import MCDA_method
from ..io import TableDesc


class LMAW(MCDA_method):
    """Logarithmic Methogology of Additive Weights (LMAW) method [#lmaw1]_.

    The implementation is based on [#lmaw1]_, with an assumption that the decision matrix and the weights are
    already aggregated if there were multiple decision makers. If needed, the class provides static methods
    for aggregating multiple decision matrices and weight vectors according to the LMAW aggregation formulas.

    Examples
    --------
    >>> import numpy as np
    >>> from pymcdm.methods import LMAW
    >>> matrix = np.array([[10.5, -3.1, 1.7],
    ...                    [-4.7, 0, 3.4],
    ...                    [8.1, 0.3, 1.3]])
    >>> weights = np.array([0.2, 0.3, 0.5])
    >>> types = np.array([1, -1, 1])
    >>> body = LMAW()
    >>> prefs = body(matrix, weights, types)
    >>> len(prefs)
    3

    References
    ----------
    .. [#lmaw1] Pamučar, D., Žižović, M., Biswas, S., & Božanić, D. (2021). A new logarithm methodology of additive weights (LMAW) for multi-criteria decision-making: Application in logistics. Facta universitatis, series: mechanical engineering, 19(3), 361-380.
    """
    _tables = [
        TableDesc(caption='Standarized decision matrix',
                  label='smatrix', symbol='$\\vartheta_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Phi matrix (log-normalized)',
                  label='phi', symbol='$\\phi_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted standarized decision matrix',
                  label='xi', symbol='$\\xi_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$Q_i$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        n_rows, n_cols = matrix.shape

        smatrix = np.empty_like(matrix, dtype='float')
        for j in range(n_cols):
            col = matrix[:, j]
            if types[j] == 1:
                m = np.max(col)
                smatrix[:, j] = (col + m) / m
            else:
                m = np.min(col)
                smatrix[:, j] = (col + m) / col

        phi_matrix = np.log(smatrix) / np.log(np.prod(smatrix, axis=0))

        xi_matrix = (2 * phi_matrix**weights) / ((2 - phi_matrix)**weights + phi_matrix**weights)

        q_values = np.sum(xi_matrix, axis=1)

        return smatrix, phi_matrix, xi_matrix, q_values

    @staticmethod
    def aggregate_matrices(matrices : np.ndarray | list[np.ndarray],
                           p : int = 1,
                           q : int = 1):
        """ Aggregate multiple matrices using the LMAW aggregation formula.

        Parameters
        ----------
            matrices : ndarray or list of ndarray
                A 3D numpy array or a list of 2D numpy arrays to be aggregated.

            p : int
                The exponent p in the aggregation formula. Default is 1.

            q : int
                The exponent q in the aggregation formula. Default is 1.

        Returns
        -------
            ndarray
                The aggregated 2D numpy array that can be used to calculate LMAW preferences.
        """
        k = len(matrices)
        matrices = np.asarray(matrices)
        shape = matrices[0].shape

        # Calculate sum from the formula ((1/k(k-1) * sum...)^(1/(p+q)))
        aggregated = np.empty(shape, dtype='float')
        for i, j in zip(range(shape[0]), range(shape[1])):
            v = matrices[:, i, j]
            aggregated[i, j] = sum(v[x]**p * sum(v[y]**q for y in range(k) if y != x)
                                   for x in range(k))

        aggregated = (aggregated / (k * (k - 1))) ** (1 / (p + q))
        return aggregated

    @staticmethod
    def aggregate_weights(weight_vectors : np.ndarray | list[np.ndarray],
                          aip : float = 0.5,
                          p : int = 1,
                          q : int = 1):
        """ Aggregate multiple weight vectors using the LMAW aggregation formula.

        Parameters
        ----------
            weight_vectors : ndarray or list of ndarray
                A 2D numpy array or a list of 1D numpy arrays to be aggregated.
                The original LMAW scale is as follows:
                1 - Absolutely low (AL), 1.5 - Very low (VL),
                2 - Low (L), 2.5 - Medium (M),
                3 - Equal (E), 3.5 - Medium high (MH),
                4 - High (H), 4.5 - Very high (VH) and 5 - Absolutely high (AH).

            aip : float
                The absolute anti-ideal point (AIP) value. Default is 0.5.
                This parameter is used to scale weights from linguistic terms if needed.

            p : int
                The exponent p in the aggregation formula. Default is 1.

            q : int
                The exponent q in the aggregation formula. Default is 1.

        Returns
        -------
            ndarray
                The aggregated 1D numpy array of weights.
        """
        k = len(weight_vectors)
        length = weight_vectors[0].shape[0]
        weight_vectors = np.asarray(weight_vectors, dtype='float')

        # Scale linguistic variables by AIP
        weight_vectors = weight_vectors / aip

        # Determine the weight coefficients
        weight_vectors = np.log(weight_vectors.T) / np.log(np.prod(weight_vectors, axis=1))
        weight_vectors = weight_vectors.T

        # Calculate sum from the formula ((1/k(k-1) * sum...)^(1/(p+q)))
        aggregated = np.empty(length, dtype='float')
        for i in range(length):
            v = weight_vectors[:, i]
            aggregated[i] = sum(v[x]**p * sum(v[y]**q for y in range(k) if y != x)
                                for x in range(k))

        aggregated = (aggregated / (k * (k - 1))) ** (1 / (p + q))
        return aggregated
