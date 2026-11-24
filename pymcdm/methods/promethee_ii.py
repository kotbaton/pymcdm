# Copyright (c) 2023-2026 Andrii Shekhovtsov

from .partial import PROMETHEE_I
from ..io import TableDesc, MCDA_results


class PROMETHEE_II(PROMETHEE_I):
    """ Preference Ranking Organization Method for Enrichment of Evaluations II (PROMETHEE II) method.

        The PROMETHEE II method is based on a pairwise comparison of alternatives given a preference function [#promethee2]_.

        Parameters
        ----------
            preference_function: str or list of str
                Name of the preference function ('usual', 'ushape', 'vshape', 'level', 'vshape_2', 'gaussian'),
                used for all criteria, or a list with the name of the preference function for each criterion
                (generalized criteria of types I-VI from [#promethee2b]_).

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
            .. [#promethee2] Mareschal, B., De Smet, Y., & Nemery, P. (2008, December). Rank reversal in the PROMETHEE II method:
                   some new results. In 2008 IEEE International Conference on Industrial Engineering and Engineering
                   Management (pp. 959-963). IEEE.
            .. [#promethee2b] Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects:
                   The PROMETHEE method. European Journal of Operational Research, 24(2), 228-238.

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
        >>> np.round(body(matrix, weights, types), 2).tolist()
        [0.1, -0.3, 0.2]

        Different preference function for each criterion:

        >>> body = PROMETHEE_II(['ushape', 'vshape', 'gaussian'], q=[1, None, None], p=[None, 2, None], s=[None, None, 1])
        >>> np.round(body(matrix, weights, types), 4).tolist()
        [0.0992, -0.1242, 0.025]
    """
    _tables = PROMETHEE_I._tables[:-1] + [
        TableDesc(caption='Positive outrankig flows',
                  label='pos_flow', symbol='$\\phi^+(A_i)$', rows='A', cols=None),
        TableDesc(caption='Negative outrankig flows',
                  label='neg_flow', symbol='$\\phi^-(A_i)$', rows='A', cols=None),
        TableDesc(caption='Global preference net flows',
                  label='net_flow', symbol='$$\\phi(A_i)$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types, save_results=False):
        *other, (F_plus, F_minus) = super()._method(matrix, weights, types,
                                                    save_results=True)

        FI = F_plus - F_minus

        return *other, F_plus, F_minus, FI

    def _method_explained(self, matrix, weights, types):
        diff_tables, *other_tables = self._method(matrix, weights, types, save_results=True)

        tables = self._generate_diff_tables(diff_tables)
        tables.extend([t.create_table(data)
                       for t, data in zip(self._tables, other_tables)])

        return MCDA_results(
            method=self,
            matrix=matrix,
            results=tables
        )