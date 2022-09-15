# Copyright (c) 2020 Andrii Shekhovtsov

from functools import partial
import numpy as np

from .. import normalizations
from .mcda_method import MCDA_method


class PROMETHEE_II(MCDA_method):
    """ Preference Ranking Organization Method for Enrichment of Evaluations II (PROMETHEE II) method.

        The PROMETHEE II method is based on a pairwise comparison of alternatives given a preference function [1].

        Parameters
        ----------
            preference_function: str
                Name of the preference function ('usual', 'ushape', 'vshape', 'level', 'vshape_2')

        References
        ----------
            .. [1] Mareschal, B., De Smet, Y., & Nemery, P. (2008, December). Rank reversal in the PROMETHEE II method:
                   some new results. In 2008 IEEE International Conference on Industrial Engineering and Engineering
                   Management (pp. 959-963). IEEE.

        Examples
        --------
        >>> from pymcdm.methods import PROMETHEE_II
        >>> import numpy as np
        >>> body = PROMETHEE_II('usual')
        >>> matrix =  np.array([[4, 3, 2],
        ...                     [3, 2, 4],
        ...                     [5, 1, 3]])
        >>> weights = np.array([0.5, 0.3, 0.2])
        >>> types = np.ones(3)
        >>> [round(preference, 2) for preference in body(matrix, weights, types)]
        [0.1, -0.3, 0.2]
    """

    def __init__(self, preference_function):
        self.pf = getattr(PROMETHEE_II._PreferenceFunctions, preference_function)

    def __call__(self, matrix, weights, types, *args, p=None, q=None, promethee_I=False, **kwargs):
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

                p : ndarray
                    p values for each criterion

                q : ndarray
                    q values for each criterion

                promethee_I : bool
                    If True then returns F+ and F- (like in promethee I).

                *args: is necessary for methods which reqiure some additional data.

                **kwargs: is necessary for methods which reqiure some additional data.

            Returns
            -------
                If `promethee_I` is True:
                ndarray
                    Positive flow

                ndarray
                    Negative flow

                If `promethee_I` is False:
                ndarray
                    Preference values of alternatives. Better alternatives have higher values.
        """
        pf = self.pf
        if p is None and q is None:
            pfs = (partial(pf, p=None, q=None) for i in range(matrix.shape[1]))
        elif p is None and q is not None:
            pfs = (partial(pf, p=None, q=q_) for q_ in q)
        elif p is not None and q is None:
            pfs = (partial(pf, p=p_, q=None) for p_ in p)
        else:
            pfs = (partial(pf, p=p_, q=q_) for p_, q_ in zip(p, q))

        Fp, Fm, FI = PROMETHEE_II._promethee(matrix, weights, types, pfs)
        if promethee_I:
            return Fp, Fm
        else:
            return FI

    @staticmethod
    def _promethee(matrix, weights, criteria_types, pref_functions):
        # N - number of alternatives
        # M - number of criteria
        N, M = matrix.shape

        c_tables = (np.tile(crit.reshape(N, 1), (1, N)) for crit in matrix.T)
        diff_tables = ((c - crit if ct == 1 else crit - c)
                       for crit, c, ct in zip(matrix.T, c_tables, criteria_types))

        pi_table = sum(w * pf(d) for w, d, pf in zip(weights, diff_tables, pref_functions))

        F_plus = np.sum(pi_table, axis=1) / (N-1)
        F_minus = np.sum(pi_table, axis=0) / (N-1)

        FI = F_plus - F_minus

        return F_plus, F_minus, FI


    class _PreferenceFunctions:
        @staticmethod
        def usual(d, q, p):
            return (d > 0).astype(np.int8)

        @staticmethod
        def ushape(d, q, p):
            return (d > q).astype(np.int8)

        @staticmethod
        def vshape(d, q, p):
            d_ = d.copy()
            cond = np.logical_and(0 < d, d <= p)
            np.putmask(d_, cond, d/p)
            np.putmask(d_, np.logical_not(cond), d > p)
            return d_

        @staticmethod
        def level(d, q, p):
            d_ = d.copy()
            cond = np.logical_and(q < d, d <= p)
            np.putmask(d_, cond, 0.5)
            np.putmask(d_, np.logical_not(cond), d > p)
            return d_

        @staticmethod
        def vshape_2(d, q, p):
            d_ = d.copy()
            cond = np.logical_and(q < d, d <= p)
            np.putmask(d_, cond, (d-q)/(p-q))
            np.putmask(d_, np.logical_not(cond), d > p)
            return d_
