# Copyright (c) 2023 Andrii Shekhovtsov

from .promethee_i import PROMETHEE_I

class PROMETHEE_II(PROMETHEE_I):
    """ Preference Ranking Organization Method for Enrichment of Evaluations II (PROMETHEE II) method.

        The PROMETHEE II method is based on a pairwise comparison of alternatives given a preference function [1].

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
    _captions = PROMETHEE_I._captions + [
        'Global preference net flows.'
    ]

    def _method(self, matrix, weights, types, save_results=False):
        *other, (F_plus, F_minus) = super()._method(matrix, weights, types,
                                                    save_results=True)

        FI = F_plus - F_minus

        return (*other, F_plus, F_minus, FI)
