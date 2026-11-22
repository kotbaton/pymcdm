# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from .spotis import SPOTIS
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
                each criterion in rows. Values in the decision matrix must lie within the domain,
                unless `clip` is True.
            normalization : str
                Normalization procedure: 'max' (x / max, Step 5.1) or 'minmax'
                ((x - min) / (max - min), Step 5.2). Default is 'max'. The 'max' normalization
                requires a positive upper bound of every domain.
            clip : bool
                If True, values outside the domain are clipped to its ends before normalization,
                so that performance beyond the domain brings no further gain. If False, such values
                raise an error. Default is False.

        Notes
        -----
        In [#rtopsis1]_ the ideal solutions (Step 7) are written for the Max normalization only.
        Here they are the weighted normalized ends of the domain, which gives exactly Step 7 for
        the Max normalization and 0 and the weight for the Max-Min normalization.

        Several other rank-reversal-free variants of TOPSIS differ from R-TOPSIS only in the source
        of the domain and are obtained with suitable parameters:

        - NR-TOPSIS [#rtopsis2]_: historical minimum and maximum of every criterion as the domain
          and the 'minmax' normalization, e.g. ``RTOPSIS(RTOPSIS.make_bounds(history), 'minmax')``.
        - The absolute mode of García-Cascales and Lamata [#rtopsis3]_: one common scale
          [Z0, Zt] for all criteria and the 'max' normalization.
        - The domain of IE-TOPSIS [#rtopsis4]_: the observed extremes extended by `alpha`
          standard deviations, see :meth:`expand_bounds`, with the 'minmax' normalization.
          IE-TOPSIS itself ranks the alternatives by the PRC index, which depends on the whole
          set of alternatives; the closeness coefficient is used here.
        - TOPSIS-RAD [#rtopsis5]_: vetoed and desired performance levels as the domain, the
          'minmax' normalization and ``clip=True``. Alternatives below the vetoed levels have to be
          removed from the decision matrix beforehand.
        - BP-TOPSIS [#rtopsis6]_: the boxplot fences of every criterion as the domain, see
          :meth:`boxplot_bounds`, with the 'minmax' normalization.

        References
        ----------
        .. [#rtopsis1] de Farias Aires, R. F., & Ferreira, L. (2019). A new approach to avoid rank reversal
            cases in the TOPSIS method. Computers & Industrial Engineering, 132, 84-97.
        .. [#rtopsis2] Yang, W. (2020). Ingenious solution for the rank reversal problem of TOPSIS method.
            Mathematical Problems in Engineering, 2020, 9676518.
        .. [#rtopsis3] García-Cascales, M. S., & Lamata, M. T. (2012). On rank reversal and TOPSIS method.
            Mathematical and Computer Modelling, 56, 123-132.
        .. [#rtopsis4] Yang, B., Zhao, J., & Zhao, H. (2022). A robust method for avoiding rank reversal in the
            TOPSIS. Computers & Industrial Engineering, 174, 108776.
        .. [#rtopsis5] Costa, L. F., Costa, H. G., Lima, D., & Rodrigues, B. (2026). TOPSIS-RAD: Ranking
            According to Desires. arXiv preprint arXiv:2606.07253.
        .. [#rtopsis6] Yang, W., Pang, X., Kong, D., & Shang, H. (2026). BP-TOPSIS: A Boxplot-Based Approach to
            Reducing Rank Reversal in the TOPSIS Method. International Journal of Information Technology &
            Decision Making, 25(10), 3509-3538.

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
        >>> np.round(body(matrix, weights, types), 4).tolist()
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

    def __init__(self, bounds, normalization='max', clip=False):
        """ Create R-TOPSIS method object.

        Parameters
        ----------
            bounds : ndarray
                Domain of every criterion. Should be two dimensional array with [min, max] value for
                each criterion in rows.
            normalization : str
                Normalization procedure, 'max' or 'minmax'. Default is 'max'.
            clip : bool
                Clip values outside the domain to its ends instead of raising an error.
                Default is False.
        """
        self.bounds = np.asarray(bounds, dtype='float')
        bounds_validator(self.bounds)

        if normalization not in self._normalizations:
            raise ValueError(f'Unknown normalization {normalization!r}. '
                             f'Available normalizations: {", ".join(self._normalizations)}.')
        if normalization == 'max' and np.any(self.bounds[:, 1] <= 0):
            raise ValueError('The max normalization requires a positive upper bound of every domain.')
        self.normalization = normalization
        self.clip = clip

    def _normalize(self, x):
        """ Normalize values with respect to the domain (Step 5). """
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]
        if self.normalization == 'max':
            return x / upper
        return (x - lower) / (upper - lower)

    def _method(self, matrix, weights, types):
        if self.clip:
            matrix = np.clip(matrix, self.bounds[:, 0], self.bounds[:, 1])
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
        if not self.clip:
            matrix_bounds_validator(matrix, self.bounds)

    @staticmethod
    def make_bounds(matrix):
        """ Returns the minimum and maximum of every criterion as a domain, e.g. from historical data
            as in NR-TOPSIS.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix or historical data.
                    Alternatives are in rows and Criteria are in columns.

            Returns
            -------
                bounds : ndarray
                    Min and max values (bounds) for each criterion.
        """
        return SPOTIS.make_bounds(matrix)

    @staticmethod
    def expand_bounds(matrix, alpha=3, floor=0.0):
        """ Returns a domain obtained by extending the observed extremes of every criterion by `alpha`
            sample standard deviations (Algorithm 1 of IE-TOPSIS [#rtopsis4]_).

            The upper bound is ``max + alpha * std``. The lower bound is ``min - alpha * std``, but not
            lower than `floor`, as in [#rtopsis4]_ where it is set to zero when ``min <= alpha * std``.
            The bounds should be computed once, e.g. on the initial set of alternatives, and kept fixed
            for later sets; recomputing them for every set brings rank reversal back.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix used to calibrate the domain.
                    Alternatives are in rows and Criteria are in columns.
                alpha : float
                    Number of standard deviations, at least 3 according to [#rtopsis4]_. Default is 3.
                floor : float or None
                    Lowest admissible lower bound. Default is 0, as in [#rtopsis4]_; use None for
                    criteria that can take negative values.

            Returns
            -------
                bounds : ndarray
                    Extended min and max values (bounds) for each criterion.

            Examples
            --------
            >>> import numpy as np
            >>> from pymcdm.methods import RTOPSIS
            >>> matrix = np.array([[36, 42, 43, 70],
            ...                    [25, 50, 45, 80],
            ...                    [28, 45, 50, 75]])
            >>> np.round(RTOPSIS.expand_bounds(matrix, alpha=6), 2)
            array([[  0.  ,  70.12],
                   [ 17.75,  74.25],
                   [ 21.37,  71.63],
                   [ 40.  , 110.  ]])
        """
        matrix = np.asarray(matrix, dtype='float')
        std = np.std(matrix, axis=0, ddof=1)
        lower = np.min(matrix, axis=0) - alpha * std
        upper = np.max(matrix, axis=0) + alpha * std
        if floor is not None:
            lower = np.maximum(lower, floor)
        return np.column_stack((lower, upper))

    @staticmethod
    def boxplot_bounds(matrix, e=3):
        """ Returns a domain given by the boxplot fences of every criterion (Section 3.1 of BP-TOPSIS
            [#rtopsis6]_).

            The bounds are ``Q1 - e * IQR`` and ``Q3 + e * IQR``, where ``IQR = Q3 - Q1`` and the quartiles
            are computed from the sorted values ``T(1) <= ... <= T(n)`` of the criterion as
            ``T(k) + (T(k+1) - T(k)) * ((n + 1) p - k)`` with ``k = floor((n + 1) p)`` (Eq. 6), clamped
            to ``T(1)`` and ``T(n)``. No distribution of the data is assumed. As with :meth:`expand_bounds`,
            the bounds should be computed once and kept fixed for later sets of alternatives.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix used to calibrate the domain.
                    Alternatives are in rows and Criteria are in columns.
                e : float
                    Expansion coefficient of the interquartile range. Default is 3, the value used in
                    BP-TOPSIS [#rtopsis6]_; 1.5 gives the usual fences for mild outliers.

            Returns
            -------
                bounds : ndarray
                    Lower and upper fences (bounds) for each criterion.

            Examples
            --------
            >>> import numpy as np
            >>> from pymcdm.methods import RTOPSIS
            >>> matrix = np.array([[36, 42, 43, 70],
            ...                    [25, 50, 45, 80],
            ...                    [28, 45, 50, 75],
            ...                    [24, 40, 47, 100]])
            >>> RTOPSIS.boxplot_bounds(matrix)
            array([[ -5.  ,  63.25],
                   [ 15.75,  73.5 ],
                   [ 26.25,  66.5 ],
                   [  0.  , 166.25]])
        """
        matrix = np.sort(np.asarray(matrix, dtype='float'), axis=0)
        n = matrix.shape[0]

        def quantile(p):
            position = (n + 1) * p
            k = int(np.floor(position))
            if k < 1:
                return matrix[0]
            if k >= n:
                return matrix[-1]
            return matrix[k - 1] + (matrix[k] - matrix[k - 1]) * (position - k)

        q1, q3 = quantile(0.25), quantile(0.75)
        iqr = q3 - q1
        return np.column_stack((q1 - e * iqr, q3 + e * iqr))
