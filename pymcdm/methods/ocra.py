# Copyright (c) 2021 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


def _ocra_normalization(x, cost=False):
    if cost:
        return (np.max(x) - x) / np.min(x)
    return (x - np.min(x)) / np.min(x)


class OCRA(MCDA_method):
    """ Operational Competitiveness Rating (OCRA) method.

        The main idea of the OCRA method is toperform   independent evaluation ofalternatives  with  respect  to
        beneficial  andnon beneficial  criteria,  and  finally  tocombine these two sets of ratings to obtainthe
        operational competitiveness ratings [#ocra1]_.

        Parameters
        ----------
          normalization_function : callable
              Function which should be used to normalize `matrix` columns. It should match signature `foo(x, cost)`,
              where `x` is a vector which should be normalized and `cost` is a bool variable which says if `x` is a
              cost or profit criterion.

        References
        ----------
        .. [#ocra1] Madić, M., Petković, D., & Radovanović, M. (2015). Selection of non-conventional machining processes using
             the OCRA method. Serbian Journal of Management, 10(1), 61-73.


        Examples
        --------
        >>> from pymcdm.methods import OCRA
        >>> import numpy as np
        >>> body = OCRA()
        >>> matrix = np.array([[7.7, 256, 7.2, 7.3, 7.3],
        ...                    [8.1, 250, 7.9, 7.8, 7.7],
        ...                    [8.7, 352, 8.6, 7.9, 8.0],
        ...                    [8.1, 262, 7.0, 8.1, 7.2],
        ...                    [6.5, 271, 6.3, 6.4, 6.1],
        ...                    [6.8, 228, 7.1, 7.2, 6.5]])
        >>> weights = np.array([0.239, 0.225, 0.197, 0.186, 0.153])
        >>> types = np.array([1, -1, 1, 1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.143, 0.210, 0.164, 0.167, 0, 0.112]
    """
    _tables = [
        TableDesc(caption='The aggregate performance of $i^{th}$ alternative with respect'
                          ' to all non-beneficial criteria',
                  label='non-benef', symbol='$\\bar{I}_{i}$', rows='A', cols=None),
        TableDesc(caption='Linear preference rating for the non-beneficial criteria',
                  label='non-benef_rating', symbol='$\\bar{\\bar{I}}_{i}$', rows='A', cols=None),
        TableDesc(caption='The preference ratings with respect to the beneficial criteria',
                  label='benef', symbol='$\\bar{O}_{i}$', rows='A', cols=None),
        TableDesc(caption='Linear preference rating for the beneficial criteria',
                  label='benef_rating', symbol='$\\bar{\\bar{O}}_{i}$', rows='A', cols=None),
        TableDesc(caption='Overall preference rating',
                  label='pref', symbol='$P_i$', rows='A', cols=None)
    ]

    def __init__(self, normalization_function=_ocra_normalization):
        self.normalization = normalization_function

    def _method(self, matrix, weights, types):
        n, m = matrix.shape

        # Calculate preference ratings for cost and profit criteria
        I = np.zeros(n)
        O = np.zeros(n)
        for j in range(m):
            if types[j] == -1:
                I += weights[j] * self.normalization(matrix[:, j], cost=True)
            else:
                O += weights[j] * self.normalization(matrix[:, j], cost=False)

        # Calculate linear preference ratings for cost and profit criteria
        Il = I - np.min(I)
        Ol = O - np.min(O)

        # Calculate overall preference rating
        P = (Il + Ol) - np.min(Il + Ol)
        return I, Il, O, Ol, P
