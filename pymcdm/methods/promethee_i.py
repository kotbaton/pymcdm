# Copyright (c) 2020-2023 Andrii Shekhovtsov

from itertools import repeat
from functools import partial, wraps
import numpy as np

from .. import normalizations
from .mcda_method import MCDA_method

def _preference_function_wrapper(f):
    @wraps(f)
    def wrapper(d, q, p):
        if callable(q):
            q = q(d)

        if callable(p):
            p = p(d)

        return f(d, q, p)
    return wrapper


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


class PROMETHEE_I(MCDA_method):
    """ Preference Ranking Organization Method for Enrichment of Evaluations I (PROMETHEE I) method.

        The PROMETHEE I method is based on a pairwise comparison of alternatives given a preference function [1].

        Parameters
        ----------
            preference_function: str
                Name of the preference function ('usual', 'ushape', 'vshape', 'level', 'vshape_2')

            p : ndarray or list
                p values for each criterion. Can be either float values or function. If function, p value will be calculated based on difference table.

            q : ndarray or list
                q values for each criterion. Can be either float values or function. If function, q value will be calculated based on difference table.


        References
        ----------
            .. [1] Mareschal, B., De Smet, Y., & Nemery, P. (2008, December). Rank reversal in the PROMETHEE II method:
                   some new results. In 2008 IEEE International Conference on Industrial Engineering and Engineering
                   Management (pp. 959-963). IEEE.

        Examples
        --------
        >>> from pymcdm.methods import PROMETHEE_I
        >>> import numpy as np
        >>> body = PROMETHEE_I('usual')
        >>> matrix =  np.array([[4, 3, 2],
        ...                     [3, 2, 4],
        ...                     [5, 1, 3]])
        >>> weights = np.array([0.5, 0.3, 0.2])
        >>> types = np.ones(3)
        >>> body(matrix, weights, types)
        (array([0.55, 0.35, 0.6 ]), array([0.45, 0.65, 0.4 ]))
    """
    _captions = [
        'Difference tables for each criterion.',
        'Aggregated preference indices.',
        'Positive and negative outranking flows.'
    ]

    def __init__(self, preference_function, p=None, q=None):
        pf  = getattr(_PreferenceFunctions, preference_function)
        # p and q can be provided as list of values or list of functions
        if p is None and q is None:
            pfs = repeat(partial(pf, p=None, q=None))
        elif p is None and q is not None:
            pfs = (partial(_preference_function_wrapper(pf), p=None, q=q_)
                   for q_ in q)
        elif p is not None and q is None:
            pfs = (partial(_preference_function_wrapper(pf), p=p_, q=None)
                   for p_ in p)
        else:
            pfs = (partial(_preference_function_wrapper(pf), p=p_, q=q_)
                   for p_, q_ in zip(p, q))

        self.pfs = pfs

    def _method(self, matrix, weights, types, save_results=False):
        pfs = self.pfs

        N, M = matrix.shape

        c_tables = (np.tile(crit.reshape(N, 1), (1, N)) for crit in matrix.T)

        diff_tables = ((c - crit if ct == 1 else crit - c)
                       for crit, c, ct in zip(matrix.T, c_tables, types))
        if save_results:
            diff_tables = list(diff_tables)

        pi_table = sum(w * pf(d)
                       for w, d, pf in zip(weights, diff_tables, pfs))

        F_plus = np.sum(pi_table, axis=1) / (N-1)
        F_minus = np.sum(pi_table, axis=0) / (N-1)

        return (diff_tables, pi_table, (F_plus, F_minus))

    def _method_explained(self, matrix, weights, types):
        return tuple(zip(
            self._captions,
            self._method(matrix, weights, types, save_results=True)
            ))
