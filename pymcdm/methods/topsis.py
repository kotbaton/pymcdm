# Copyright (c) 2020 Andrii Shekhovtsov

import numpy as np
from .. import normalizations
from .. import helpers
from .mcda_method import MCDA_method


class TOPSIS(MCDA_method):
    """ Technique for Order of Preference by Similarity to
        Ideal Solution (TOPSIS).

        The TOPSIS method is based on an approach in which it evaluates alternatives to a positive ideal solution and a
        negative ideal solution [#topsis1]_.

        Parameters
        ----------
           normalization_function : Callable
               Function which should be used to normalize `matrix` columns.
               It should match signature `foo(x, cost)`, where `x` is a vector
               which should be normalized and `cost` is a bool variable which
               says if `x` is a cost or profit criterion.

        References
        ----------
        .. [#topsis1] Hwang, C. L., & Yoon, K. (1981). Methods for multiple attribute decision making. In Multiple attribute
           decision making (pp. 58-191). Springer, Berlin, Heidelberg.

        Examples
        --------
        >>> from pymcdm.methods import TOPSIS
        >>> import numpy as np
        >>> body = TOPSIS()
        >>> matrix = np.array([[1, 2, 5],
        ...                     3000, 3750, 4500]]).T
        >>> weights = np.array([0.5, 0.5])
        >>> types = np.array([-1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.500, 0.617, 0.500]
   """

    def __init__(self, normalization_function=normalizations.minmax_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)

        # Every row of nmatrix is multiplayed by weights
        weighted_matrix = nmatrix * weights

        # Vectors of PIS and NIS
        pis = np.max(weighted_matrix, axis=0)
        nis = np.min(weighted_matrix, axis=0)

        # PIS and NIS are substracted from every row of weighted matrix
        Dp = np.sqrt(np.sum((weighted_matrix - pis) ** 2, axis=1))
        Dm = np.sqrt(np.sum((weighted_matrix - nis) ** 2, axis=1))

        p = Dm / (Dm + Dp)

        return (nmatrix, weighted_matrix, pis, nis, Dp, Dm, p)

    def _method_explained(self, matrix, weights, types):
        return [
            (
                'Normalized decision matrix.',
                (nmatrix := helpers.normalize_matrix(matrix, self.normalization, types))
            ),
            (
                'Weighted normalized decision matrix.',
                (wnmatrix := nmatrix * weights)
            ),
            (
                'Positive Ideal Solution',
                (pis := np.max(wnmatrix, axis=0))
            ),
            (
                'Negative Ideal Solution',
                (nis := np.min(wnmatrix, axis=0))
            ),
            (
                '?? Chuj wie jak to szło $D^+$',
                (Dp := np.sqrt(np.sum((wnmatrix - pis) ** 2, axis=1)))
            ),
            (
                '?? Chuj wie jak to szło $D^-$',
                (Dm := np.sqrt(np.sum((wnmatrix - nis) ** 2, axis=1)))
            ),
            (
                'Final preference values ($P_i$).',
                Dm / (Dm + Dp)
            )
        ]

    def _method_explained(self, matrix, weights, types):
        nmatrix = helpers.normalize_matrix(matrix, self.normalization, types)
        wnmatrix = nmatrix * weights

        pis = np.max(wnmatrix, axis=0)
        nis = np.min(wnmatrix, axis=0)

        Dp = np.sqrt(np.sum((wnmatrix - pis) ** 2, axis=1))
        Dm = np.sqrt(np.sum((wnmatrix - nis) ** 2, axis=1))

        p = Dm / (Dm + Dp)

        return (
                ('Normalized decision matrix.', nmatrix),
                ('Weighted normalized decision matrix.', wnmatrix),
                ('Positive Ideal Solution', pis),
                ('Negative Ideal Solution', nis),
                ('?? Chuj wie jak to szło $D^+$', Dp),
                ('?? Chuj wie jak to szło $D^-$', Dm),
                ('Final preference values ($P_i$).', p)
                )

    def _method_explained(self, matrix, weights, types):
        captions = [
                'Normalized decision matrix.',
                'Weighted normalized decision matrix.',
                'Positive Ideal Solution',
                'Negative Ideal Solution',
                '?? Chuj wie jak to szło $D^+$',
                '?? Chuj wie jak to szło $D^-$',
                'Final preference values ($P_i$).'
                ]
        return tuple(zip(
            self._method(matrix, weights, types),
            captions
            ))
