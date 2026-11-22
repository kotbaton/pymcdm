# Copyright (c) 2026 Bartlomiej Kizielewicz

import numpy as np

from ..mcda_method import MCDA_method
from ..partial.promethee_i import PROMETHEE_I
from ...io import TableDesc


class FLOWSORT(MCDA_method):
    """ FlowSort sorting method.

        FlowSort assigns alternatives to predefined, ordered categories with the flows of PROMETHEE
        [#flowsort1]_. Each alternative is compared with the reference profiles only: the positive, negative and net
        flows are computed in the set of the profiles and that alternative, and the alternative is assigned to the
        category whose profiles have similar flows. The category of an alternative therefore does not depend on the
        other alternatives.

        Categories are numbered from 1 (the worst) to K (the best). With limiting profiles (K + 1 profiles), profile
        r_h is the lower limit of category h + 1 and the upper limit of category h, counting the profiles from 0.
        With central profiles (K profiles), profile r_h is the centroid of category h.

        The positive and negative flows can give two different categories; the net flow gives one category between
        them [#flowsort1]_. The returned category is selected with `rule`, and all three assignments are available
        with ``verbose=True``.

        Parameters
        ----------
            profiles : ndarray
                Reference profiles in rows and criteria in columns, ordered from the worst category to the best one.
                Each profile should be at least as good as the previous one on every criterion and strictly
                preferred to it (Conditions 1 and 6 of [#flowsort1]_).

            preference_function : str or list of str
                Preference function of PROMETHEE, one for all criteria or one for each criterion. See
                :class:`pymcdm.methods.partial.PROMETHEE_I`. Default is 'usual'.

            p, q, s : list, optional
                Thresholds of the preference functions, one value for each criterion, as in PROMETHEE.

            profiles_type : str, optional
                'limiting' (default) or 'central'.

            rule : str, optional
                Flow used for the returned category: 'net' (default), 'positive' or 'negative'.

        References
        ----------
            .. [#flowsort1] Nemery, P., & Lamboray, C. (2008). FlowSort: a flow-based sorting method with limiting
                   or central profiles. TOP, 16(1), 90-113.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods.sorting import FLOWSORT
        >>> profiles = np.array([[0, 0, 0, 0, 0],
        ...                      [25, 25, 25, 25, 25],
        ...                      [50, 50, 50, 50, 50],
        ...                      [75, 75, 75, 75, 75],
        ...                      [100, 100, 100, 100, 100]])
        >>> matrix = np.array([[54, 17, 71, 45, 63],
        ...                    [15, 5, 19, 9, 23],
        ...                    [25, 25, 50, 75, 75]])
        >>> weights = np.ones(5) / 5
        >>> types = np.ones(5)
        >>> FLOWSORT(profiles)(matrix, weights, types)
        array([2, 1, 2])
        >>> FLOWSORT(profiles, rule='negative')(matrix, weights, types)
        array([3, 1, 3])
    """
    _tables = [
        TableDesc(caption='Positive flows of the profiles',
                  label='phi_plus_r', symbol=r'$\phi^+(r_h)$', rows='A', cols='r'),
        TableDesc(caption='Negative flows of the profiles',
                  label='phi_minus_r', symbol=r'$\phi^-(r_h)$', rows='A', cols='r'),
        TableDesc(caption='Net flows of the profiles',
                  label='phi_r', symbol=r'$\phi(r_h)$', rows='A', cols='r'),
        TableDesc(caption='Flows of the alternatives',
                  label='phi_a', symbol=None, rows='A',
                  cols=(r'$\phi^+(a_i)$', r'$\phi^-(a_i)$', r'$\phi(a_i)$')),
        TableDesc(caption='Categories from the positive, negative and net flows',
                  label='categories_all', symbol=None, rows='A',
                  cols=(r'$C_{\phi^+}(a_i)$', r'$C_{\phi^-}(a_i)$', r'$C_{\phi}(a_i)$')),
        TableDesc(caption='Assigned categories',
                  label='categories', symbol='$C(a)$', rows='A', cols=None),
    ]

    PROFILES_TYPES = ('limiting', 'central')
    RULES = ('positive', 'negative', 'net')
    # Results are category numbers, not preferences to rank
    _produces_ranking = False
    # Alternatives are compared with the profiles, not with each other, so dominance does not matter
    _check_dominance = False

    def __init__(self, profiles, preference_function='usual', p=None, q=None, s=None, profiles_type='limiting',
                 rule='net'):
        self.profiles = np.atleast_2d(np.asarray(profiles, dtype=float))
        if profiles_type not in self.PROFILES_TYPES:
            raise ValueError(f'Unknown profiles type {profiles_type!r}. '
                             f'Available profiles types: {", ".join(self.PROFILES_TYPES)}.')
        if rule not in self.RULES:
            raise ValueError(f'Unknown rule {rule!r}. Available rules: {", ".join(self.RULES)}.')
        minimum = 3 if profiles_type == 'limiting' else 2
        if self.profiles.shape[0] < minimum:
            raise ValueError(f'At least {minimum} {profiles_type} profiles are required for two categories.')
        self.profiles_type = profiles_type
        self.rule = rule
        # Preference degrees are computed as in PROMETHEE
        self._promethee = PROMETHEE_I(preference_function, p=p, q=q, s=s)

    def _flows(self, matrix, weights, types):
        """ Positive and negative flows (Eqs. 1-2) of the rows of `matrix`. """
        _, _, (phi_plus, phi_minus) = self._promethee._method(matrix, weights, types)
        return phi_plus, phi_minus

    def _additional_validation(self, matrix, weights, types):
        if self.profiles.shape[1] != matrix.shape[1]:
            raise ValueError(f'Number of criteria in profiles ({self.profiles.shape[1]}) should be equal '
                             f'to the number of criteria ({matrix.shape[1]}).')
        self._promethee._additional_validation(matrix, weights, types)
        oriented = self.profiles * types
        if np.any(np.diff(oriented, axis=0) < 0):
            raise ValueError('Each profile should be at least as good as the previous one on every criterion '
                             '(Condition 1).')
        # Condition 6: a better profile is preferred to a worse one, which is not preferred to it
        _, pi, _ = self._promethee._method(self.profiles, weights, types)
        n = len(pi)
        if np.any(pi[np.tril_indices(n, -1)] <= 0) or np.any(pi[np.triu_indices(n, 1)] > 0):
            raise ValueError('Each profile should be strictly preferred to every worse profile (Condition 6); '
                             'check the profiles and the preference thresholds.')

    def rank(self, a):
        raise NotImplementedError('FlowSort assigns alternatives to categories and does not rank them; '
                                  'the returned values are category numbers.')

    def _assign(self, value, profiles, increasing):
        """ Category of a flow value compared with the flows of the profiles (ordered from the worst one). """
        if self.profiles_type == 'limiting':
            # Category h lies between the profiles r_{h-1} and r_h
            bounds = profiles[:-1]
        else:
            # Category h lies between the midpoints of its centroid and the neighbouring ones
            bounds = (profiles[1:] + profiles[:-1]) / 2
        # Flows equal up to rounding errors are treated as equal, e.g. for an alternative equal to a profile
        tolerance = 1e-9
        if increasing:
            # Positive and net flows: phi(r_{h-1}) < phi(a) <= phi(r_h)
            category = int(np.sum(value > bounds + tolerance))
        else:
            # Negative flow: phi(r_h) < phi(a) <= phi(r_{h-1})
            category = int(np.sum(value <= bounds + tolerance))
        if self.profiles_type == 'limiting':
            # Alternatives outside the profiles go to the worst or the best category
            return max(category, 1)
        return category + 1

    def _method(self, matrix, weights, types):
        n_profiles = self.profiles.shape[0]
        phi_plus_r = np.zeros((matrix.shape[0], n_profiles))
        phi_minus_r = np.zeros((matrix.shape[0], n_profiles))
        phi_a = np.zeros((matrix.shape[0], 3))
        categories_all = np.zeros((matrix.shape[0], 3), dtype=int)

        for i, alternative in enumerate(matrix):
            # Flows in the set of the profiles and the alternative (Eqs. 1-3)
            phi_plus, phi_minus = self._flows(np.vstack([self.profiles, alternative]), weights, types)
            phi = phi_plus - phi_minus
            phi_plus_r[i], phi_minus_r[i] = phi_plus[:-1], phi_minus[:-1]
            phi_a[i] = phi_plus[-1], phi_minus[-1], phi[-1]
            categories_all[i] = (self._assign(phi_plus[-1], phi_plus[:-1], True),
                                 self._assign(phi_minus[-1], phi_minus[:-1], False),
                                 self._assign(phi[-1], phi[:-1], True))

        categories = categories_all[:, self.RULES.index(self.rule)]
        return phi_plus_r, phi_minus_r, phi_plus_r - phi_minus_r, phi_a, categories_all, categories
