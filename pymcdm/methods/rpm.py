# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc
from ..validators import matrix_validator, types_validator, bounds_validator, matrix_bounds_validator


class RPM(MCDA_method):
    """ Reference Point Method (RPM) with objective ranking [#rpm1]_ [#rpm2]_.

        Every criterion value is transformed by a piecewise linear partial achievement function into a satisfaction
        level from 0 to 10: from 0 to `alpha` between the worst bound and the reservation level, from `alpha` to
        `beta` between the reservation and the aspiration level, and from `beta` to 10 between the aspiration level
        and the best bound. The partial achievements are aggregated by the overall achievement function, which is
        determined mostly by the worst partial achievement, or by an equitable aggregation (Lorenz quantile or
        OWA).

        The method does not use weights: the importance of criteria is expressed by `alpha` and `beta`, e.g.
        (5, 9) very low, (4, 8) low, (3, 7) normal, (2, 6) high and (1, 5) very high importance.

        Read more in the User Guide.

        Parameters
        ----------
            bounds : ndarray | None
                Lower and upper bounds of every criterion, `[[lower, upper], ...]`. None (default) means the minimum
                and the maximum of the decision matrix.
            aspiration : ndarray | None
                Aspiration levels. None (default) means the statistical (objective) aspiration levels, the average
                of the mean criterion value and the best bound (Eq. 4).
            reservation : ndarray | None
                Reservation levels. None (default) means the statistical (objective) reservation levels, the average
                of the mean criterion value and the worst bound (Eq. 4).
            alpha : float | ndarray
                Partial achievement at the reservation level, for all criteria or for each of them. Default is 3.
            beta : float | ndarray
                Partial achievement at the aspiration level, for all criteria or for each of them, with
                0 < alpha < beta < 10. Default is 7.
            epsilon : float
                Regularizing coefficient of the overall achievement function (Eq. 3). Default is 0.4.
            aggregation : str
                'achievement' (default) for the overall achievement function (Eq. 3), 'lorenz' for the Lorenz
                quantile (Eq. 5) or 'owa' for the ordered weighted average with weights 2^-i (Eq. 6).
            quantile : int | None
                Number of the worst partial achievements averaged by the Lorenz quantile. None (default) means
                one third of the number of criteria (at least 1).

        References
        ----------
        .. [#rpm1] Wierzbicki, A. P., Granat, J., & Makowski, M. (2007). Discrete decision problems with large
               number of criteria. IIASA Interim Report IR-07-025. International Institute for Applied Systems
               Analysis, Laxenburg.

        .. [#rpm2] Wierzbicki, A. P. (2007). Reference point approaches and objective ranking. In Practical
               Approaches to Multi-Objective Optimization, Dagstuhl Seminar Proceedings 06501.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import RPM
        >>> matrix = np.array([[11, 8, 10, 40],
        ...                    [23, 40, 34, 60],
        ...                    [16, 50, 45, 70],
        ...                    [35, 20, 20, 44],
        ...                    [18, 30, 20, 80],
        ...                    [12, 8, 9, 30]])
        >>> types = np.ones(4)
        >>> body = RPM()
        >>> preferences = body(matrix, types=types)
        >>> np.round(preferences, 2).tolist()
        [0.29, 8.24, 6.41, 5.4, 6.22, 0.07]
        >>> body.rank(preferences).tolist()
        [5.0, 1.0, 2.0, 4.0, 3.0, 6.0]
    """
    _tables = [
        TableDesc(caption='Partial achievements',
                  label='achievements', symbol=r'$\sigma_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Final preference values',
                  label='pref', symbol=r'$\sigma_{i}$', rows='A', cols=None),
    ]

    def __init__(self, bounds=None, aspiration=None, reservation=None, alpha=3, beta=7, epsilon=0.4,
                 aggregation='achievement', quantile=None):
        self.bounds = None if bounds is None else np.asarray(bounds, dtype=float)
        if self.bounds is not None:
            bounds_validator(self.bounds)
        self.aspiration = None if aspiration is None else np.asarray(aspiration, dtype=float)
        self.reservation = None if reservation is None else np.asarray(reservation, dtype=float)
        self.alpha = np.asarray(alpha, dtype=float)
        self.beta = np.asarray(beta, dtype=float)
        if np.any(self.alpha <= 0) or np.any(self.beta >= 10) or np.any(self.alpha >= self.beta):
            raise ValueError('alpha and beta should satisfy 0 < alpha < beta < 10.')
        if epsilon < 0:
            raise ValueError(f'epsilon should be non-negative, but is {epsilon}.')
        self.epsilon = epsilon
        if aggregation not in ('achievement', 'lorenz', 'owa'):
            raise ValueError(f"aggregation should be 'achievement', 'lorenz' or 'owa', but is {aggregation!r}.")
        self.aggregation = aggregation
        if quantile is not None and quantile < 1:
            raise ValueError(f'quantile should be a positive integer, but is {quantile}.')
        self.quantile = quantile

    def __call__(self, matrix, weights=None, types=None, validation=True, verbose=False):
        """ Rank alternatives from decision matrix `matrix` with criteria types `types`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : None
                    Not used in the RPM method, see `alpha` and `beta`.

                types : ndarray | None
                    Array with definitions of criteria types: 1 if criteria is profit and -1 if criteria is cost
                    for each criteria in `matrix`. None means that all criteria are profit criteria.

                validation : bool
                    Enable (True) or disable (False) validation of the input data. Default is True.

                verbose : bool
                    Explain the MCDA, i.e. provide matrices and vectors from all the steps of the method, instead
                    of return just the preference vector. Default is False.
        """
        matrix = np.asarray(matrix, dtype='float')
        types = np.ones(matrix.shape[1]) if types is None else np.asarray(types)

        if validation:
            matrix_validator(matrix, types, check_dominance=False)
            types_validator(matrix, types)
            self._additional_validation(matrix, weights, types)

        if verbose:
            return self._method_explained(matrix, weights, types)
        else:
            return self._method(matrix, weights, types)[-1]

    def _levels(self, matrix, types):
        if self.bounds is None:
            lower, upper = np.min(matrix, axis=0), np.max(matrix, axis=0)
        else:
            lower, upper = self.bounds[:, 0], self.bounds[:, 1]
        worst = np.where(types == 1, lower, upper)
        best = np.where(types == 1, upper, lower)

        # Statistical reservation and aspiration levels (Eq. 4)
        mean = np.mean(matrix, axis=0)
        reservation = 0.5 * (worst + mean) if self.reservation is None else self.reservation
        aspiration = 0.5 * (best + mean) if self.aspiration is None else self.aspiration
        return worst, reservation, aspiration, best

    def _method(self, matrix, weights, types):
        worst, reservation, aspiration, best = self._levels(matrix, types)
        alpha = np.broadcast_to(self.alpha, worst.shape)
        beta = np.broadcast_to(self.beta, worst.shape)

        # Progress of the values from the worst bound, in the direction of improvement of every criterion
        q = (matrix - worst) * types
        r = (reservation - worst) * types
        a = (aspiration - worst) * types
        b = (best - worst) * types

        def segment(start, stop, low, high):
            span = np.where(stop > start, stop - start, 1)
            return low + (high - low) * (q - start) / span

        # Partial achievement functions (Eq. 2)
        achievements = np.where(q < r, segment(0, r, 0, alpha),
                                np.where(q < a, segment(r, a, alpha, beta), segment(a, b, beta, 10)))

        theta = np.sort(achievements, axis=1)
        n = matrix.shape[1]
        if self.aggregation == 'achievement':
            # Overall achievement function (Eq. 3)
            pref = theta[:, 0] + self.epsilon / n * np.sum(achievements, axis=1)
        elif self.aggregation == 'lorenz':
            # Lorenz quantile (Eq. 5)
            k = max(1, n // 3) if self.quantile is None else self.quantile
            pref = np.sum(theta[:, :k], axis=1) / k
        else:
            # Ordered weighted average (Eq. 6)
            pref = np.sum(theta * 2.0 ** -np.arange(1, n + 1), axis=1)

        return achievements, pref

    def _additional_validation(self, matrix, weights, types):
        n = matrix.shape[1]
        if self.bounds is not None:
            if self.bounds.shape[0] != n:
                raise ValueError(f'Number of bounds ({self.bounds.shape[0]}) should be equal '
                                 f'to the number of criteria ({n}).')
            matrix_bounds_validator(matrix, self.bounds)
        for name, value in (('aspiration', self.aspiration), ('reservation', self.reservation),
                            ('alpha', self.alpha), ('beta', self.beta)):
            if value is not None and value.ndim > 0 and value.shape != (n,):
                raise ValueError(f'{name} should have {n} values, but has shape {value.shape}.')
        if self.quantile is not None and self.quantile > n:
            raise ValueError(f'quantile ({self.quantile}) should not exceed the number of criteria ({n}).')
        worst, reservation, aspiration, best = self._levels(matrix, types)
        progress = np.array([worst, reservation, aspiration, best]) * types
        if np.any(np.diff(progress, axis=0) < 0):
            raise ValueError('The worst bound, the reservation level, the aspiration level and the best bound '
                             'should be ordered in the direction of improvement of every criterion.')
