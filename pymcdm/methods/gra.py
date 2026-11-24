# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class GRA(MCDA_method):
    """ Grey Relational Analysis (GRA) method [#gra1]_.

        The performance values are translated into comparability sequences in [0, 1] (grey relational generating),
        which are compared with the reference sequence of ones by the grey relational coefficients. The grey
        relational grade, the weighted sum of the coefficients, measures the similarity of an alternative to the
        reference sequence.

        Read more in the User Guide.

        Parameters
        ----------
            zeta : float
                Distinguishing coefficient in (0, 1], which expands or compresses the range of the grey relational
                coefficients. Default is 0.5.
            targets : ndarray | None
                Desired values of the criteria for which the closer to the desired value, the better (Eq. 3). Use
                `np.nan` for the other criteria, which are generated as profit or cost criteria according to `types`.
                For the criteria with a desired value, `types` is ignored. Default is None (no such criteria).

        References
        ----------
        .. [#gra1] Kuo, Y., Yang, T., & Huang, G. W. (2008). The use of grey relational analysis in solving multiple
               attribute decision-making problems. Computers & Industrial Engineering, 55(1), 80-93.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import GRA
        >>> matrix = np.array([[185.95, 8, 8.28],
        ...                    [207.37, 9, 3.75],
        ...                    [264.07, 5, 2.07],
        ...                    [228.00, 8, 14.00],
        ...                    [170.14, 9, 8.28]])
        >>> weights = np.ones(3) / 3
        >>> types = np.array([-1, 1, -1])
        >>> body = GRA(targets=[np.nan, np.nan, 1])
        >>> preferences = body(matrix, weights, types)
        >>> np.round(preferences, 4).tolist()
        [0.6288, 0.7535, 0.5084, 0.4827, 0.8239]
        >>> body.rank(preferences).tolist()
        [3.0, 2.0, 4.0, 5.0, 1.0]
    """
    _tables = [
        TableDesc(caption='Comparability sequences (grey relational generating)',
                  label='nmatrix', symbol='$x_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Grey relational coefficients',
                  label='coefficients', symbol=r'$\gamma(x_{0j}, x_{ij})$', rows='A', cols='C'),
        TableDesc(caption='Grey relational grades',
                  label='grades', symbol=r'$\Gamma(X_0, X_i)$', rows='A', cols=None),
    ]

    def __init__(self, zeta=0.5, targets=None):
        if not 0 < zeta <= 1:
            raise ValueError(f'zeta should be in (0, 1], but is {zeta}.')
        self.zeta = zeta
        self.targets = None if targets is None else np.asarray(targets, dtype=float)

    def _method(self, matrix, weights, types):
        lower, upper = np.min(matrix, axis=0), np.max(matrix, axis=0)

        # Grey relational generating for the larger-the-better and the smaller-the-better criteria (Eqs. 1-2)
        nmatrix = np.where(types == 1, matrix - lower, upper - matrix) / (upper - lower)

        # The closer-to-the-desired-value-the-better criteria (Eq. 3)
        if self.targets is not None:
            target = ~np.isnan(self.targets)
            deviation = np.abs(matrix[:, target] - self.targets[target])
            scale = np.maximum(upper[target] - self.targets[target], self.targets[target] - lower[target])
            nmatrix[:, target] = 1 - deviation / scale

        # Grey relational coefficients with respect to the reference sequence of ones (Eq. 4)
        delta = 1 - nmatrix
        delta_min, delta_max = np.min(delta), np.max(delta)
        coefficients = (delta_min + self.zeta * delta_max) / (delta + self.zeta * delta_max)

        # Grey relational grades (Eq. 5)
        grades = np.sum(coefficients * weights, axis=1)

        return nmatrix, coefficients, grades

    def _additional_validation(self, matrix, weights, types):
        if np.any(np.max(matrix, axis=0) == np.min(matrix, axis=0)):
            raise ValueError('All criteria should have at least two different values.')
        if self.targets is not None and self.targets.shape != (matrix.shape[1],):
            raise ValueError(f'Number of targets ({self.targets.size}) should be equal '
                             f'to the number of criteria ({matrix.shape[1]}).')
