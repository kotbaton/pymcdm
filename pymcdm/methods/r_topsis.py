# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..validators import bounds_validator, matrix_bounds_validator
from ..io import TableDesc


class RTOPSIS(MCDA_method):
    """ Robust TOPSIS (R-TOPSIS) method [#rtopsis1]_.

        R-TOPSIS removes the dependence of TOPSIS on the set of alternatives by normalizing every
        criterion on a domain given by the decision maker instead of on the values in the decision
        matrix, and by fixing the positive and negative ideal solutions at the ends of that domain.
        The evaluation of an alternative therefore does not change when other alternatives are
        added or removed.

        Read more in the User Guide.

        Parameters
        ----------
            bounds : ndarray
                Domain of every criterion. Should be two dimensional array with [min, max] value for
                each criterion in rows. Values in the decision matrix must lie within the domain.
            normalization : str
                Normalization procedure: 'max' (x / max, Step 5.1) or 'minmax'
                ((x - min) / (max - min), Step 5.2). Default is 'max'. The 'max' normalization
                requires a positive upper bound of every domain.

        Notes
        -----
        In [#rtopsis1]_ the ideal solutions (Step 7) are written for the Max normalization only.
        Here they are the weighted normalized ends of the domain, which gives exactly Step 7 for
        the Max normalization and 0 and the weight for the Max-Min normalization.

        References
        ----------
        .. [#rtopsis1] de Farias Aires, R. F., & Ferreira, L. (2019). A new approach to avoid rank reversal
            cases in the TOPSIS method. Computers & Industrial Engineering, 132, 84-97.

        Examples
        --------
        >>> from pymcdm.methods import RTOPSIS
        >>> import numpy as np
        >>> matrix = np.array([[8.5218, 1.0000, 1.0],
        ...                    [7.0455, 1.0000, 1.0],
        ...                    [7.9625, 0.9821, 1.0],
        ...                    [8.6286, 0.9821, 1.0]])
        >>> bounds = np.array([[0, 10], [0, 1], [0, 1]], dtype=float)
        >>> weights = np.array([0.3633, 0.3298, 0.3069])
        >>> types = np.array([1, 1, 1])
        >>> body = RTOPSIS(bounds)
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.9105, 0.8284, 0.8775, 0.9157]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$n_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Negative Ideal Solution',
                  label='nis', symbol='$r^{-}_{j}$', rows='C', cols=None),
        TableDesc(caption='Positive Ideal Solution',
                  label='pis', symbol='$r^{+}_{j}$', rows='C', cols=None),
        TableDesc(caption='Distance from NIS',
                  label='dnis', symbol='$S_i^-$', rows='A', cols=None),
        TableDesc(caption='Distance from PIS',
                  label='dpis', symbol='$S_i^+$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$CC_i$', rows='A', cols=None)
    ]

    _normalizations = ('max', 'minmax')

    def __init__(self, bounds, normalization='max'):
        """ Create R-TOPSIS method object.

        Parameters
        ----------
            bounds : ndarray
                Domain of every criterion. Should be two dimensional array with [min, max] value for
                each criterion in rows.
            normalization : str
                Normalization procedure, 'max' or 'minmax'. Default is 'max'.
        """
        self.bounds = np.asarray(bounds, dtype='float')
        bounds_validator(self.bounds)

        if normalization not in self._normalizations:
            raise ValueError(f'Unknown normalization {normalization!r}. '
                             f'Available normalizations: {", ".join(self._normalizations)}.')
        if normalization == 'max' and np.any(self.bounds[:, 1] <= 0):
            raise ValueError('The max normalization requires a positive upper bound of every domain.')
        self.normalization = normalization

    def _normalize(self, x):
        """ Normalize values with respect to the domain (Step 5). """
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]
        if self.normalization == 'max':
            return x / upper
        return (x - lower) / (upper - lower)

    def _method(self, matrix, weights, types):
        nmatrix = self._normalize(matrix)

        # Every row of nmatrix is multiplied by weights
        weighted_matrix = nmatrix * weights

        # Ideal solutions are fixed at the weighted normalized ends of the domain (Step 7)
        lower = self._normalize(self.bounds[:, 0]) * weights
        upper = self._normalize(self.bounds[:, 1]) * weights
        pis = np.where(types == 1, upper, lower)
        nis = np.where(types == 1, lower, upper)

        Dp = np.sqrt(np.sum((weighted_matrix - pis) ** 2, axis=1))
        Dm = np.sqrt(np.sum((weighted_matrix - nis) ** 2, axis=1))

        p = Dm / (Dm + Dp)

        return nmatrix, weighted_matrix, nis, pis, Dm, Dp, p

    def _additional_validation(self, matrix, weights, types):
        if self.bounds.shape[0] != matrix.shape[1]:
            raise ValueError(f'Number of domains ({self.bounds.shape[0]}) should be equal '
                             f'to the number of criteria ({matrix.shape[1]}).')
        matrix_bounds_validator(matrix, self.bounds)
