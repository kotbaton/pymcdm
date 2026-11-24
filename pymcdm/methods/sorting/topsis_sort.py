# Copyright (c) 2026 Bartlomiej Kizielewicz

import numpy as np

from ..mcda_method import MCDA_method
from ..r_topsis import RTOPSIS
from ...io import TableDesc


class TOPSIS_SORT(MCDA_method):
    """ TOPSIS-Sort-B and TOPSIS-Sort-C sorting methods.

        TOPSIS-Sort-B (boundary profiles) and TOPSIS-Sort-C (characteristic profiles) assign alternatives to
        predefined, ordered categories by comparing their closeness coefficients with the closeness coefficients of
        the profiles [#topsissort1]_. As in R-TOPSIS [#topsissort2]_, the ideal and anti-ideal solutions are fixed by
        the domain of the criteria, so the category of an alternative does not depend on the other alternatives.

        Categories are numbered from 1 (the worst) to q (the best). With boundary profiles (q - 1 profiles), profile
        b_h is the upper limit of category h and the lower limit of category h + 1. With characteristic profiles
        (q profiles), profile p_h is a typical alternative of category h.

        Parameters
        ----------
            profiles : ndarray
                Profiles in rows and criteria in columns, ordered from the worst category to the best one. Each
                profile should be at least as good as the previous one on every criterion.

            bounds : ndarray
                Domain of every criterion: [min, max] for each criterion in rows (Step 3), as in R-TOPSIS. The ends
                of the domain are the ideal and anti-ideal solutions.

            profiles_type : str, optional
                'boundary' for TOPSIS-Sort-B (default) or 'characteristic' for TOPSIS-Sort-C.

            normalization : str, optional
                Normalization of the decision matrix: 'max' (normalization by the maximum of the domain, default) or
                'minmax' (interval normalization), as in R-TOPSIS.

        References
        ----------
            .. [#topsissort1] de Lima Silva, D. F., & de Almeida Filho, A. T. (2020). Sorting with TOPSIS through
                   boundary and characteristic profiles. Computers & Industrial Engineering, 141, 106328.

            .. [#topsissort2] de Farias Aires, R. F., & Ferreira, L. (2019). A new approach to avoid rank reversal
                   cases in the TOPSIS method. Computers & Industrial Engineering, 132, 84-97.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods.sorting import TOPSIS_SORT
        >>> matrix = np.array([[85, 90, 70],
        ...                    [60, 75, 65],
        ...                    [30, 40, 55]])
        >>> weights = np.ones(3) / 3
        >>> types = np.ones(3)
        >>> bounds = np.array([[0, 100], [0, 100], [0, 100]])
        >>> profiles = np.array([[50, 50, 50],
        ...                      [75, 75, 75]])
        >>> body = TOPSIS_SORT(profiles, bounds)
        >>> body(matrix, weights, types)
        array([3, 2, 1])
    """
    _tables = [
        TableDesc(caption='Closeness coefficients of alternatives',
                  label='cl_a', symbol='$Cl(a)$', rows='A', cols=None),
        TableDesc(caption='Closeness coefficients of profiles',
                  label='cl_p', symbol='$Cl(P_h)$', rows='P', cols=None),
        TableDesc(caption='Assigned categories',
                  label='categories', symbol='$C(a)$', rows='A', cols=None),
    ]

    PROFILES_TYPES = ('boundary', 'characteristic')
    # Results are category numbers, not preferences to rank
    _produces_ranking = False
    # Alternatives are compared with the profiles, not with each other, so dominance does not matter
    _check_dominance = False

    def __init__(self, profiles, bounds, profiles_type='boundary', normalization='max'):
        self.profiles = np.atleast_2d(np.asarray(profiles, dtype=float))
        if profiles_type not in self.PROFILES_TYPES:
            raise ValueError(f'Unknown profiles type {profiles_type!r}. '
                             f'Available profiles types: {", ".join(self.PROFILES_TYPES)}.')
        self.profiles_type = profiles_type
        # Closeness coefficients are calculated with R-TOPSIS (Steps 3-8)
        self._rtopsis = RTOPSIS(bounds, normalization=normalization)
        if self.profiles.shape[1] != self._rtopsis.bounds.shape[0]:
            raise ValueError(f'Number of criteria in profiles ({self.profiles.shape[1]}) should be equal '
                             f'to the number of domains ({self._rtopsis.bounds.shape[0]}).')

    @property
    def bounds(self):
        return self._rtopsis.bounds

    @property
    def normalization(self):
        return self._rtopsis.normalization

    def _additional_validation(self, matrix, weights, types):
        self._rtopsis._additional_validation(matrix, weights, types)
        self._rtopsis._additional_validation(self.profiles, weights, types)
        oriented = self.profiles * types
        if np.any(np.diff(oriented, axis=0) < 0):
            raise ValueError('Each profile should be at least as good as the previous one on every criterion.')

    def rank(self, a):
        raise NotImplementedError('TOPSIS-Sort assigns alternatives to categories and does not rank them; '
                                  'the returned values are category numbers.')

    def _method(self, matrix, weights, types):
        cl_a = self._rtopsis._method(matrix, weights, types)[-1]
        cl_p = self._rtopsis._method(self.profiles, weights, types)[-1]

        if self.profiles_type == 'boundary':
            # Category above the highest boundary profile that the alternative reaches (Step 9 of Algorithm 3)
            categories = 1 + (cl_a[:, None] >= cl_p[None, :]).sum(axis=1)
        else:
            # Category of the profile with the closest coefficient; ties go to the better category
            # (Step 9 of Algorithm 4)
            distances = np.abs(cl_a[:, None] - cl_p[None, :])
            categories = len(cl_p) - np.argmin(distances[:, ::-1], axis=1)

        return cl_a, cl_p, categories
