# Copyright (c) 2020, 2024 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class COPRAS(MCDA_method):
    """ COmplex PRoportional ASsessment (COPRAS) method.

        COPRAS is used to assess the maximizing and minimizing index values, and the effect of maximizing and minimizing
        indexes of attributes on the results assessment is considered separately. See [#copras1]_ [#copras2]_.

        Read more in the User Guide.

        References
        ----------
        .. [#copras1] Zavadskas, E. K., Kaklauskas, A., & Sarka, V. (1994). The new method of multicriteria complex
               proportional assessment of projects. Technological and economic development of economy, 1(3), 131-139.
        .. [#copras2] Zavadskas, E. K., Kaklauskas, A., Peldschus, F., & Turskis,
               Z. (2007). Multi-attribute assessment of road design solutions by
               using the COPRAS method. The Baltic journal of Road and Bridge
               engineering, 2(4), 195-203.

        Examples
        --------
        >>> from pymcdm.methods import COPRAS
        >>> import numpy as np
        >>> body = COPRAS()
        >>> matrix = np.array([[1543, 2000, 39000, 15, 13.76, 3.86, 5, 3, 5000],
        ...                    [1496, 3600, 43000, 14, 14, 2.5, 4, 4, 4000],
        ...                    [1584, 3100, 24500, 10, 13.1, 3.7, 2, 2, 3500],
        ...                    [1560, 2700, 36000, 12, 13.2, 3.2, 3, 3, 3500],
        ...                    [1572, 2500, 31500, 13, 13.3, 3.4, 3, 2, 3500],
        ...                    [1580, 2400, 20000, 12, 12.8, 3.9, 2, 2, 3000]])
        >>> weights = np.array([0.2027, 0.1757, 0.1622, 0.1351, 0.1081, 0.0946, 0.0676, 0.0405, 0.0135])
        >>> types = np.array([-1, -1, -1, 1, 1, -1, 1, 1, 1])
        >>> [round(preference, 4) for preference in body(matrix, weights, types)]
        [0.9459, 1.0, 0.8192, 0.8839, 0.8556, 0.7789]
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$r_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Weighted normalized decision matrix',
                  label='wnmatrix', symbol='$v_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Sum of minimising indices',
                  label='smin', symbol='$S_{-i}$', rows='A', cols=None),
        TableDesc(caption='Sum of maximising indices',
                  label='smax', symbol='$S_{+i}$', rows='A', cols=None),
        TableDesc(caption='Related significance',
                  label='rel_sign', symbol='$Q_i$', rows='A', cols=None),
        TableDesc(caption='Final preference (utility degree)',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        if np.all(types == 1.0):
            raise ValueError('types array contains only profit criteria.'
                             ' COPRAS method requires at least one cost'
                             ' criterion.')

        nmatrix = matrix / np.sum(matrix, axis=0)

        # Weighted normalized decision-making matrix
        wmatrix = nmatrix * weights

        Sp = np.sum(wmatrix[:, types == 1], axis=1)
        Sm = np.sum(wmatrix[:, types == -1], axis=1)

        Q = Sp + ((np.min(Sm) * Sm) / (Sm * (np.min(Sm) / Sm)))

        return nmatrix, wmatrix, Sm, Sp, Q, Q / np.max(Q)
