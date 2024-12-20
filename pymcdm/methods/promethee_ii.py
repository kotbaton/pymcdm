# Copyright (c) 2023-2024 Andrii Shekhovtsov

from .partial import PROMETHEE_I
from ..io import TableDesc, MCDA_results


class PROMETHEE_II(PROMETHEE_I):
    """ Preference Ranking Organization Method for Enrichment of Evaluations II (PROMETHEE II) method.

        The PROMETHEE II method is based on a pairwise comparison of alternatives given a preference function [#promethee2]_.

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
            .. [#promethee2] Mareschal, B., De Smet, Y., & Nemery, P. (2008, December). Rank reversal in the PROMETHEE II method:
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