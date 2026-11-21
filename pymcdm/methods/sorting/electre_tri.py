# Copyright (c) 2026 Bartlomiej Kizielewicz

import numpy as np

from ..mcda_method import MCDA_method
from ...io import TableDesc


class ELECTRE_TRI(MCDA_method):
    """ ELimination Et Choix Traduisant la REalité TRI (ELECTRE TRI) method.

        ELECTRE TRI is a sorting method: it assigns each alternative to one of predefined, ordered categories by
        comparing it with the profiles which are the limits of the categories [#electretri1]_, [#electretri2]_.
        Unlike ranking methods, the category of an alternative does not depend on the other alternatives.

        Categories are numbered from 1 (the worst) to k + 1 (the best), where k is the number of profiles.
        Profile b_h is the upper limit of category h and the lower limit of category h + 1.

        Parameters
        ----------
            profiles : ndarray
                Profiles (limits of the categories) in rows and criteria in columns, ordered from the limit of the
                worst category to the limit of the best one. Each profile should be at least as good as the previous
                one on every criterion.

            q : ndarray or list, optional
                Indifference thresholds: one value for each criterion, used for all profiles, or one row for each
                profile. Default is 0 (no indifference zone).

            p : ndarray or list, optional
                Preference thresholds, given like `q`. Default is equal to `q`.

            v : ndarray or list, optional
                Veto thresholds, given like `q`. Use None (or np.inf) for criteria without veto. Default is None (no
                veto on any criterion).

            cutting_level : float, optional
                Cutting level (lambda) in [0.5, 1]: the outranking a S b is valid if its credibility is at least
                `cutting_level`. Default is 0.75.

            procedure : str, optional
                Assignment procedure: 'pessimistic' (conjunctive, default) or 'optimistic' (disjunctive).

        References
        ----------
            .. [#electretri1] Mousseau, V., Słowiński, R., & Zielniewicz, P. (2000). A user-oriented implementation of
                   the ELECTRE-TRI method integrating preference elicitation support. Computers & Operations Research,
                   27(7-8), 757-777.

            .. [#electretri2] Figueira, J. R., Mousseau, V., & Roy, B. (2016). ELECTRE methods. In S. Greco,
                   M. Ehrgott, & J. R. Figueira (Eds.), Multiple Criteria Decision Analysis: State of the Art Surveys
                   (pp. 155-185). Springer.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods.sorting import ELECTRE_TRI
        >>> matrix = np.array([[9, 8, 6],
        ...                    [7, 9, 9],
        ...                    [4, 6, 8]])
        >>> weights = np.array([0.5, 0.3, 0.2])
        >>> types = np.ones(3)
        >>> profiles = np.array([[5, 5, 5],
        ...                      [8, 7, 7]])
        >>> body = ELECTRE_TRI(profiles, cutting_level=0.7)
        >>> body(matrix, weights, types)
        array([3, 2, 1])
    """
    _tables = [
        TableDesc(caption='Concordance indices of alternatives over profiles',
                  label='c_ab', symbol='$c(a, b_h)$', rows='A', cols='b'),
        TableDesc(caption='Concordance indices of profiles over alternatives',
                  label='c_ba', symbol='$c(b_h, a)$', rows='A', cols='b'),
        TableDesc(caption='Credibility of the outranking of profiles by alternatives',
                  label='sigma_ab', symbol='$\\sigma(a, b_h)$', rows='A', cols='b'),
        TableDesc(caption='Credibility of the outranking of alternatives by profiles',
                  label='sigma_ba', symbol='$\\sigma(b_h, a)$', rows='A', cols='b'),
        TableDesc(caption='Assigned categories',
                  label='categories', symbol='$C(a)$', rows='A', cols=None),
    ]

    PROCEDURES = ('pessimistic', 'optimistic')
    # Results are category numbers, not preferences to rank
    _produces_ranking = False

    def __init__(self, profiles, q=None, p=None, v=None, cutting_level=0.75, procedure='pessimistic'):
        self.profiles = np.atleast_2d(np.asarray(profiles, dtype=float))
        if self.profiles.ndim != 2:
            raise ValueError('Profiles should be a two-dimensional array (profiles in rows, criteria in columns).')
        k, n = self.profiles.shape

        self.q = self._thresholds(q, 0.0, k, n, 'q')
        self.p = self._thresholds(p, self.q, k, n, 'p')
        self.v = self._thresholds(v, np.inf, k, n, 'v')

        if np.any(self.q < 0) or np.any(self.p < self.q) or np.any(self.v < self.p):
            raise ValueError('Thresholds should satisfy 0 <= q <= p <= v for every criterion and profile.')
        if not 0.5 <= cutting_level <= 1:
            raise ValueError(f'Cutting level should be in [0.5, 1], but is {cutting_level}.')
        if procedure not in self.PROCEDURES:
            raise ValueError(f'Unknown procedure {procedure!r}. Available procedures: {", ".join(self.PROCEDURES)}.')

        self.cutting_level = cutting_level
        self.procedure = procedure

    @staticmethod
    def _thresholds(values, default, k, n, name):
        if values is None:
            return np.broadcast_to(np.asarray(default, dtype=float), (k, n)).copy()
        values = np.array([[np.inf if x is None else x for x in row]
                           for row in np.atleast_2d(np.asarray(values, dtype=object))], dtype=float)
        if values.shape == (1, n):
            values = np.repeat(values, k, axis=0)
        if values.shape != (k, n):
            raise ValueError(f'{name} should have one value for each criterion or one row for each profile '
                             f'({k} x {n}), but has shape {values.shape}.')
        return values

    def _additional_validation(self, matrix, weights, types):
        if matrix.shape[1] != self.profiles.shape[1]:
            raise ValueError(f'Number of criteria in profiles ({self.profiles.shape[1]}) should be equal '
                             f'to the number of criteria in the matrix ({matrix.shape[1]}).')
        oriented = self.profiles * types
        if np.any(np.diff(oriented, axis=0) < 0):
            raise ValueError('Each profile should be at least as good as the previous one on every criterion.')

    def rank(self, a):
        raise NotImplementedError('ELECTRE TRI assigns alternatives to categories and does not rank them; '
                                  'the returned values are category numbers.')

    @staticmethod
    def _partial_concordance(x, y, q, p):
        """ c_j(x, y) for benefit criteria: degree to which x is at least as good as y. """
        diff = y - x  # how much x is worse than y
        width = p - q
        with np.errstate(divide='ignore', invalid='ignore'):
            partial = np.where(width > 0, (p - diff) / width, (diff <= q).astype(float))
        return np.clip(partial, 0, 1)

    @staticmethod
    def _partial_discordance(x, y, p, v):
        """ d_j(x, y) for benefit criteria: degree to which criterion j vetoes x S y. """
        diff = y - x
        width = v - p
        with np.errstate(divide='ignore', invalid='ignore'):
            partial = np.where(np.isinf(v), 0.0,
                               np.where(width > 0, (diff - p) / width, (diff > v).astype(float)))
        return np.clip(partial, 0, 1)

    @staticmethod
    def _credibility(c, d):
        """ sigma = c * prod over d_j > c of (1 - d_j) / (1 - c). """
        with np.errstate(divide='ignore', invalid='ignore'):
            factors = np.where(d > c[..., None], (1 - d) / (1 - c[..., None]), 1.0)
        return c * np.prod(factors, axis=-1)

    def _method(self, matrix, weights, types):
        # Orient all criteria as benefit criteria
        g = matrix * types
        b = self.profiles * types
        w = weights / weights.sum()
        q, p, v = self.q, self.p, self.v

        # Shapes: (alternatives, profiles, criteria)
        ga = g[:, None, :]
        gb = b[None, :, :]

        c_ab_j = self._partial_concordance(ga, gb, q, p)
        c_ba_j = self._partial_concordance(gb, ga, q, p)
        c_ab = c_ab_j @ w
        c_ba = c_ba_j @ w

        sigma_ab = self._credibility(c_ab, self._partial_discordance(ga, gb, p, v))
        sigma_ba = self._credibility(c_ba, self._partial_discordance(gb, ga, p, v))

        outranks = sigma_ab >= self.cutting_level        # a S b_h
        outranked = sigma_ba >= self.cutting_level       # b_h S a
        k = b.shape[0]
        if self.procedure == 'pessimistic':
            # Highest profile b_h such that a S b_h -> category h + 1
            categories = np.array([1 + max((h + 1 for h in range(k) if row[h]), default=0) for row in outranks])
        else:
            # Lowest profile b_h such that b_h > a (b_h S a and not a S b_h) -> category h
            preferred = outranked & ~outranks
            categories = np.array([min((h + 1 for h in range(k) if row[h]), default=k + 1) for row in preferred])

        return c_ab, c_ba, sigma_ab, sigma_ba, categories
