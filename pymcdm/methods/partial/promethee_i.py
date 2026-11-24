# Copyright (c) 2020-2026 Andrii Shekhovtsov

from itertools import repeat
from functools import partial, wraps
import numpy as np

from ..mcda_method import MCDA_method
from ...io import TableDesc, MCDA_results

def _preference_function_wrapper(f):
    @wraps(f)
    def wrapper(d, q, p, s=None):
        if callable(q):
            q = q(d)

        if callable(p):
            p = p(d)

        if callable(s):
            s = s(d)

        return f(d, q, p, s)
    return wrapper


class _PreferenceFunctions:
    # Thresholds required by each preference function (generalized criteria of Brans et al., 1986)
    PARAMETERS = {
        'usual': (),
        'ushape': ('q',),
        'vshape': ('p',),
        'level': ('q', 'p'),
        'vshape_2': ('q', 'p'),
        'gaussian': ('s',),
    }

    @staticmethod
    def usual(d, q, p, s=None):
        return (d > 0).astype(np.int8)

    @staticmethod
    def ushape(d, q, p, s=None):
        return (d > q).astype(np.int8)

    @staticmethod
    def vshape(d, q, p, s=None):
        d_ = d.copy()
        cond = np.logical_and(0 < d, d <= p)
        np.putmask(d_, cond, d/p)
        np.putmask(d_, np.logical_not(cond), d > p)
        return d_

    @staticmethod
    def level(d, q, p, s=None):
        d_ = d.copy()
        cond = np.logical_and(q < d, d <= p)
        np.putmask(d_, cond, 0.5)
        np.putmask(d_, np.logical_not(cond), d > p)
        return d_

    @staticmethod
    def vshape_2(d, q, p, s=None):
        d_ = d.copy()
        cond = np.logical_and(q < d, d <= p)
        np.putmask(d_, cond, (d-q)/(p-q))
        np.putmask(d_, np.logical_not(cond), d > p)
        return d_

    @staticmethod
    def gaussian(d, q, p, s):
        return np.where(d > 0, 1 - np.exp(-np.square(d) / (2 * s ** 2)), 0.0)


class PROMETHEE_I(MCDA_method):
    """ Preference Ranking Organization Method for Enrichment of Evaluations I (PROMETHEE I) method.

        The PROMETHEE I method is based on a pairwise comparison of alternatives given a preference function [#promethee1]_.

        Parameters
        ----------
            preference_function: str or list of str
                Name of the preference function ('usual', 'ushape', 'vshape', 'level', 'vshape_2', 'gaussian'),
                used for all criteria, or a list with the name of the preference function for each criterion
                (generalized criteria of types I-VI from [#promethee1b]_).

            p : ndarray or list
                Preference thresholds for each criterion, required by 'vshape', 'level' and 'vshape_2'. Can be either
                float values or functions. If function, p value will be calculated based on difference table. Use None
                for criteria whose preference function does not need it.

            q : ndarray or list
                Indifference thresholds for each criterion, required by 'ushape', 'level' and 'vshape_2'. Can be either
                float values or functions. If function, q value will be calculated based on difference table. Use None
                for criteria whose preference function does not need it.

            s : ndarray or list
                Parameters of the Gaussian preference function (standard deviation) for each criterion, required by
                'gaussian'. Can be either float values or functions. Use None for other criteria.


        References
        ----------
            .. [#promethee1] Mareschal, B., De Smet, Y., & Nemery, P. (2008, December). Rank reversal in the PROMETHEE II method:
                   some new results. In 2008 IEEE International Conference on Industrial Engineering and Engineering
                   Management (pp. 959-963). IEEE.
            .. [#promethee1b] Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects:
                   The PROMETHEE method. European Journal of Operational Research, 24(2), 228-238.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods.partial import PROMETHEE_I
        >>> body = PROMETHEE_I('usual')
        >>> matrix =  np.array([[4, 3, 2],
        ...                     [3, 2, 4],
        ...                     [5, 1, 3]])
        >>> weights = np.array([0.5, 0.3, 0.2])
        >>> types = np.ones(3)
        >>> body(matrix, weights, types)
        (array([0.55, 0.35, 0.6 ]), array([0.45, 0.65, 0.4 ]))

        Different preference function for each criterion:

        >>> body = PROMETHEE_I(['ushape', 'vshape', 'gaussian'], q=[1, None, None], p=[None, 2, None], s=[None, None, 1])
        >>> F_plus, F_minus = body(matrix, weights, types)
        >>> print(np.round(F_plus, 4), np.round(F_minus, 4))
        [0.225  0.2008 0.2893] [0.1258 0.325  0.2643]
    """
    _tables = [
        # Additionally there will be a group of difference tables which will generated dynamically
        TableDesc(caption='Aggregated preference indices',
                  label='pi', symbol='$\\pi(A_i, A_j)$', rows='A', cols='A'),
        TableDesc(caption='Positive and negative outranking flows',
                  label='flows', symbol=None, rows='A', cols=('$\\phi^+(A_i)$', '$\\phi^-(A_i)$'))
    ]

    def __init__(self, preference_function, p=None, q=None, s=None):
        thresholds = {'p': p, 'q': q, 's': s}
        given = {name: list(values) for name, values in thresholds.items() if values is not None}
        lengths = {len(values) for values in given.values()}
        if isinstance(preference_function, str):
            names = None
        else:
            names = list(preference_function)
            lengths.add(len(names))
        if len(lengths) > 1:
            raise ValueError('Preference functions and p, q and s values should have the same length, '
                             f'but have lengths {sorted(lengths)}.')

        for name in ([preference_function] if names is None else names):
            if name not in _PreferenceFunctions.PARAMETERS:
                raise ValueError(f'Unknown preference function {name!r}. Available preference functions: '
                                 f'{", ".join(_PreferenceFunctions.PARAMETERS)}.')

        if not lengths:
            # The same preference function without thresholds for all criteria
            missing = _PreferenceFunctions.PARAMETERS[preference_function]
            if missing:
                raise ValueError(f'Preference function {preference_function!r} requires '
                                 f'{" and ".join(missing)} value.')
            pf = getattr(_PreferenceFunctions, preference_function)
            self.pfs = repeat(partial(pf, p=None, q=None))
            return

        n = lengths.pop()
        if names is None:
            names = [preference_function] * n

        # Per-criterion functions are stored in a list, not a generator,
        # so that the same object can be called more than once.
        pfs = []
        for i, name in enumerate(names):
            values = {key: given[key][i] if key in given else None for key in thresholds}
            missing = [key for key in _PreferenceFunctions.PARAMETERS[name] if values[key] is None]
            if missing:
                raise ValueError(f'Preference function {name!r} of criterion {i} requires '
                                 f'{" and ".join(missing)} value.')
            pf = _preference_function_wrapper(getattr(_PreferenceFunctions, name))
            pfs.append(partial(pf, **values))
        self.pfs = pfs

    def _additional_validation(self, matrix, weights, types):
        if isinstance(self.pfs, list) and len(self.pfs) != matrix.shape[1]:
            raise ValueError(f'Number of preference functions or p, q, s values ({len(self.pfs)}) should be equal '
                             f'to the number of criteria ({matrix.shape[1]}).')

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

        return diff_tables, pi_table, (F_plus, F_minus)

    def _method_explained(self, matrix, weights, types):
        diff_tables, pi_table, (F_plus, F_minus) = self._method(matrix, weights, types, save_results=True)

        tables = self._generate_diff_tables(diff_tables)
        tables.append(self._tables[0].create_table(pi_table))
        tables.append(self._tables[1].create_table(np.array((F_plus, F_minus)).T))

        return MCDA_results(
            method=self,
            matrix=matrix,
            results=tables
        )

    @staticmethod
    def _generate_diff_tables(diff_tables):
        return [
            TableDesc(caption=f'Difference table for criterion $C_{{{i}}}$',
                      label=f'diff_c{{{i}}}', symbol=f'$d_{{{i}}}(A_i, A_j)$',
                      rows='A', cols='A').create_table(t)
            for i, t in enumerate(diff_tables, 1)
        ]
