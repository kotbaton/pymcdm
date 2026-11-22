# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


def _standardization(x, cost=False):
    """ Standardization (z-score) with the population standard deviation, used in the original Hellwig's method. """
    return (x - np.mean(x)) / np.std(x)


def _normalize(matrix, normalization_function):
    """ Normalize every column regardless of its type; the type of a criterion only decides about the pattern. """
    function = _standardization if normalization_function is None else normalization_function
    return np.column_stack([function(matrix[:, j], cost=False) for j in range(matrix.shape[1])])


class HELLWIG(MCDA_method):
    """ Hellwig's method (taxonomic measure of development) [#hellwig1]_ with the Euclidean or the Mahalanobis
        distance [#hellwig2]_.

        The alternatives are ranked by their distance from the pattern of development (ideal solution), built from
        the best value of every criterion, relative to the critical distance :math:`d_0 = \\bar{d} + 2 S_d`.

        Read more in the User Guide.

        Parameters
        ----------
            normalization_function : callable | None
                Function used to normalize the columns of the matrix, with the signature `foo(x, cost)`; it is called
                with `cost=False` for all criteria, as the type of a criterion only decides whether its pattern is the
                largest or the smallest normalized value. None (default) means the standardization (z-score with the
                population standard deviation) of the original method. Not used with the Mahalanobis distance, which
                is computed on the decision matrix; by Property 2 of [#hellwig2]_ its result is the same for the linear
                normalizations considered there.
            distance : str
                'euclidean' (default) or 'mahalanobis'. The Mahalanobis distance uses the sample covariance matrix
                of the decision matrix and takes into account the correlations between criteria. The two distances
                weight the criteria differently, following Eqs. (11)-(12) of [#hellwig2]_: the Euclidean distance of
                the weighted values `w_j z_ij` weights the squared differences by `w_j^2`, the Mahalanobis distance
                with `W = diag(sqrt(w_j))` by `w_j`.

        References
        ----------
        .. [#hellwig1] Hellwig, Z. (1968). Zastosowanie metody taksonomicznej do typologicznego podziału krajów ze
               względu na poziom ich rozwoju oraz zasoby i strukturę wykwalifikowanych kadr. Przegląd Statystyczny,
               4, 307-326.

        .. [#hellwig2] Roszkowska, E. (2024). Modifying Hellwig's method for multi-criteria decision-making with
               Mahalanobis distance for addressing asymmetrical relationships. Symmetry, 16(1), 77.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import HELLWIG
        >>> from pymcdm.normalizations import vector_normalization
        >>> matrix = np.array([[1, 18, 7, 6],
        ...                    [3, 2, 10, 10],
        ...                    [5, 30, 15, 30],
        ...                    [3, 1, 15, 20],
        ...                    [8, 10, 20, 8],
        ...                    [2, 20, 10, 5],
        ...                    [10, 4, 6, 25],
        ...                    [12, 25, 10, 2],
        ...                    [5, 5, 15, 8],
        ...                    [6, 2, 5, 9]])
        >>> weights = np.ones(4) / 4
        >>> types = np.ones(4)
        >>> body = HELLWIG(vector_normalization)
        >>> np.round(body(matrix, weights, types), 3).tolist()
        [0.168, 0.141, 0.639, 0.235, 0.366, 0.225, 0.352, 0.363, 0.234, 0.144]
        >>> np.round(HELLWIG(distance='mahalanobis')(matrix, weights, types), 3).tolist()
        [0.096, 0.157, 0.565, 0.275, 0.387, 0.18, 0.296, 0.326, 0.272, 0.118]
    """
    _tables = [
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol=r'$\tilde{x}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Pattern of development',
                  label='pattern', symbol=r'$\tilde{x}^{+}_{j}$', rows='C', cols=None),
        TableDesc(caption='Distances from the pattern of development',
                  label='d', symbol='$d_i$', rows='A', cols=None),
        TableDesc(caption="Hellwig's measure",
                  label='pref', symbol='$H_i$', rows='A', cols=None),
    ]

    def __init__(self, normalization_function=None, distance='euclidean'):
        if distance not in ('euclidean', 'mahalanobis'):
            raise ValueError(f"distance should be 'euclidean' or 'mahalanobis', but is {distance!r}.")
        self.normalization = normalization_function
        self.distance = distance

    def _method(self, matrix, weights, types):
        if self.distance == 'euclidean':
            # Weighted normalized matrix and the pattern of development (Eqs. 3-10)
            wnmatrix = _normalize(matrix, self.normalization) * weights
            pattern = np.where(types == 1, np.max(wnmatrix, axis=0), np.min(wnmatrix, axis=0))
            # Euclidean distance (Eq. 11)
            d = np.sqrt(np.sum((wnmatrix - pattern) ** 2, axis=1))
        else:
            # Mahalanobis distance (Eq. 12), independent of the normalization
            wnmatrix = matrix
            pattern = np.where(types == 1, np.max(matrix, axis=0), np.min(matrix, axis=0))
            w = np.diag(np.sqrt(weights))
            metric = w @ np.linalg.inv(np.cov(matrix, rowvar=False)) @ w
            diff = matrix - pattern
            d = np.sqrt(np.einsum('ij,jk,ik->i', diff, metric, diff))

        # Critical distance and Hellwig's measure (Eqs. 13-14)
        d0 = np.mean(d) + 2 * np.std(d)
        pref = 1 - d / d0

        return wnmatrix, pattern, d, pref

    def _additional_validation(self, matrix, weights, types):
        if self.normalization is None and np.any(np.std(matrix, axis=0) == 0):
            raise ValueError('All criteria should have at least two different values.')
        if self.distance == 'mahalanobis':
            if matrix.shape[0] <= matrix.shape[1]:
                raise ValueError('The Mahalanobis distance requires more alternatives than criteria.')
            if np.linalg.matrix_rank(np.cov(matrix, rowvar=False)) < matrix.shape[1]:
                raise ValueError('The covariance matrix of the decision matrix is singular.')


class MIDIA(MCDA_method):
    """ Multi-criteria method Integrating Distances to Ideal and Anti-ideal points (MIDIA) [#midia1]_.

        An extension of Hellwig's method, which combines the closeness to the ideal and to the anti-ideal solution,
        both related to the distance between them.

        Read more in the User Guide.

        Parameters
        ----------
            alpha : float
                Coefficient of importance of the distance to the ideal solution, in [0, 1]; 1 gives the pure
                aggressive (ideal-based) strategy and 0 the pure conservative (anti-ideal-based) strategy. Default is
                0.5.
            normalization_function : callable | None
                Function used to normalize the columns of the matrix, as in :class:`HELLWIG`. None (default) means
                the standardization (z-score with the population standard deviation).

        References
        ----------
        .. [#midia1] Roszkowska, E., & Filipowicz-Chomko, M. (2024). A multi-criteria method integrating distances
               to ideal and anti-ideal points. Symmetry, 16(8), 1025.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import MIDIA
        >>> matrix = np.array([[16, 50, 98, 20, 64],
        ...                    [11, 50, 97, 23, 68],
        ...                    [17, 29, 90, 23, 70],
        ...                    [8, 55, 98, 22, 54],
        ...                    [11, 43, 91, 18, 56],
        ...                    [9, 58, 86, 10, 50],
        ...                    [18, 44, 82, 5, 49],
        ...                    [4, 25, 85, 14, 66],
        ...                    [6, 35, 80, 8, 59],
        ...                    [3, 38, 78, 5, 58]])
        >>> weights = np.ones(5) / 5
        >>> types = np.ones(5)
        >>> np.round(MIDIA(alpha=0.5)(matrix, weights, types), 3).tolist()
        [0.818, 0.793, 0.662, 0.641, 0.544, 0.458, 0.406, 0.356, 0.269, 0.217]
    """
    _tables = [
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol=r'$\tilde{x}_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Closeness to the ideal solution',
                  label='DI', symbol='$DI_i$', rows='A', cols=None),
        TableDesc(caption='Closeness to the anti-ideal solution',
                  label='DAI', symbol='$DAI_i$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol=r'$D(\alpha)_i$', rows='A', cols=None),
    ]

    def __init__(self, alpha=0.5, normalization_function=None):
        if not 0 <= alpha <= 1:
            raise ValueError(f'alpha should be in [0, 1], but is {alpha}.')
        self.alpha = alpha
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        # Weighted normalized matrix, ideal and anti-ideal solutions (Eqs. 3-10)
        wnmatrix = _normalize(matrix, self.normalization) * weights
        ideal = np.where(types == 1, np.max(wnmatrix, axis=0), np.min(wnmatrix, axis=0))
        anti_ideal = np.where(types == 1, np.min(wnmatrix, axis=0), np.max(wnmatrix, axis=0))

        # Distances (Eqs. 11-12) related to the distance between the ideal and anti-ideal solutions (Eqs. 13-14)
        d_ideal = np.sqrt(np.sum((wnmatrix - ideal) ** 2, axis=1))
        d_anti_ideal = np.sqrt(np.sum((wnmatrix - anti_ideal) ** 2, axis=1))
        d = np.sqrt(np.sum((ideal - anti_ideal) ** 2))
        DI = 1 - d_ideal / d
        DAI = d_anti_ideal / d

        # Final measure (Eq. 15)
        pref = self.alpha * DI + (1 - self.alpha) * DAI

        return wnmatrix, DI, DAI, pref

    def _additional_validation(self, matrix, weights, types):
        if np.any(np.max(matrix, axis=0) == np.min(matrix, axis=0)):
            raise ValueError('All criteria should have at least two different values.')
