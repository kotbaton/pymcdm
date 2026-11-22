# Copyright (c) 2026 Bartlomiej Kizielewicz
import numpy as np
from scipy.stats import rankdata

from .mcda_method import MCDA_method
from ..io import TableDesc


class MULTIMOORA(MCDA_method):
    """ MULTIMOORA (MOORA plus the full multiplicative form) method.

        MULTIMOORA combines three approaches on the matrix normalized with the square root of the sum of squares
        [#multimoora1]_: the ratio system and the reference point of MOORA [#multimoora2]_, and the full
        multiplicative form. Their rankings are aggregated with the dominance theory [#multimoora3]_: an alternative
        dominates another one if it is better in at least two of the three rankings (absolute dominance, better in all
        three, is a special case), and dominance is transitive. Alternatives in a circular dominance (A dominates B,
        B dominates C and C dominates A) get the same rank [#multimoora3]_.

        The method returns the number of alternatives minus the number of alternatives which dominate the given one,
        directly or through transitivity, outside its own circle (higher is better). An alternative is therefore always
        ranked above every alternative it dominates. Alternatives with the same value share a position; this happens
        in circular dominance and when neither of two alternatives is better in two rankings because of ties
        (equability).
        The scores of the three parts are available with ``verbose=True``.

        Weights are used as multipliers of the normalized values in the ratio system and the reference point, and as
        exponents in the full multiplicative form. The original method [#multimoora1]_ uses no weights; equal weights
        give the same rankings.

        References
        ----------
            .. [#multimoora1] Brauers, W. K. M., & Zavadskas, E. K. (2010). Project management by MULTIMOORA as an
                   instrument for transition economies. Technological and Economic Development of Economy, 16(1),
                   5-24.

            .. [#multimoora2] Brauers, W. K., & Zavadskas, E. K. (2006). The MOORA method and its application to
                   privatization in a transition economy. Control and Cybernetics, 35(2), 445-469.

            .. [#multimoora3] Brauers, W. K. M., & Zavadskas, E. K. (2011). MULTIMOORA optimization used to decide on
                   a bank loan to buy property. Technological and Economic Development of Economy, 17(1), 174-188.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import MULTIMOORA
        >>> matrix = np.array([[1, 14, 9, 200, 600, 20, 20, 3.5, 2.5],
        ...                    [1.6, 16, 7, 150, 800, 13.5, 25, 4, 1.5],
        ...                    [2, 17, 5, 80, 1200, 10, 30, 3.8, 1.25]])
        >>> weights = np.ones(9) / 9
        >>> types = np.array([1, 1, -1, 1, 1, 1, -1, 1, 1])
        >>> body = MULTIMOORA()
        >>> preferences = body(matrix, weights, types)
        >>> preferences
        array([3., 2., 1.])
        >>> body.rank(preferences)
        array([1., 2., 3.])
    """
    _tables = [
        TableDesc(caption='Normalized decision matrix',
                  label='nmatrix', symbol='$x^*_{ij}$', rows='A', cols='C'),
        TableDesc(caption='Ratio system',
                  label='ratio', symbol='$y^*_i$', rows='A', cols=None),
        TableDesc(caption='Reference point (largest weighted deviation)',
                  label='refpoint', symbol='$z_i$', rows='A', cols=None),
        TableDesc(caption='Full multiplicative form',
                  label='fmf', symbol='$U_i$', rows='A', cols=None),
        TableDesc(caption='Rankings of the three parts',
                  label='rankings', symbol='$R_{ik}$', rows='A', cols='R'),
        TableDesc(caption='Preference from the dominance theory',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        nmatrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))
        wmatrix = nmatrix * weights

        # Ratio system: sum of benefit minus sum of cost normalized responses (Eq. 5)
        ratio = wmatrix @ types

        # Reference point: maximal (benefit) or minimal (cost) normalized responses, Tchebycheff metric (Eq. 6)
        reference = np.where(types == 1, nmatrix.max(axis=0), nmatrix.min(axis=0))
        refpoint = np.max(weights * np.abs(reference - nmatrix), axis=1)

        # Full multiplicative form: product of benefit divided by product of cost responses
        fmf = np.prod(matrix ** (weights * types), axis=1)

        rankings = np.column_stack([
            rankdata(-ratio),
            rankdata(refpoint),
            rankdata(-fmf),
        ])

        pref = self.dominance(rankings)

        return nmatrix, ratio, refpoint, fmf, rankings, pref

    @staticmethod
    def dominance(rankings):
        """ Aggregate rankings with the dominance theory of Brauers and Zavadskas (2011).

            Parameters
            ----------
            rankings : ndarray
                Rankings of the alternatives (rows) in each method (columns), 1 is the best position.

            Returns
            -------
            ndarray
                Number of alternatives minus the number of alternatives which dominate the given one, directly or
                through transitivity, outside its circular dominance. Higher is better.

            Examples
            --------
            >>> import numpy as np
            >>> from pymcdm.methods import MULTIMOORA
            >>> MULTIMOORA.dominance(np.array([[1, 1, 1], [2, 2, 3], [3, 3, 2]]))
            array([3., 2., 1.])
        """
        rankings = np.asarray(rankings, dtype=float)
        n_methods = rankings.shape[1]
        better = (rankings[:, None, :] < rankings[None, :, :]).sum(axis=2)
        # General dominance: better in at least two of the three rankings (a majority for other numbers of methods)
        reach = better > n_methods / 2
        # Transitiveness: transitive closure of the dominance relation
        for k in range(len(rankings)):
            reach = reach | (reach[:, [k]] & reach[[k], :])
        # Circular reasoning: alternatives which dominate each other are in the same circle
        circle = reach & reach.T
        dominators = (reach & ~circle).sum(axis=0)
        return (len(rankings) - dominators).astype(float)
