# Copyright (c) 2021 Bartłomiej Kizielewicz
# Copyright (c) 2024 Andrii Shekhovtsov

import numpy as np
from .mcda_method import MCDA_method
from ..io import TableDesc


class EDAS(MCDA_method):
    """ Evaluation based on Distance from Average Solution (EDAS) method.

        The EDAS method is based on an approach in which the decision alternatives are evaluated with respect to their
        distance from the mean solutions i.e. negative mean solution and positive mean solution [#edas1]_.

        Read more in the User Guide.

        References
        ----------
        .. [#edas1] Keshavarz Ghorabaee, M., Zavadskas, E. K., Olfat, L., & Turskis, Z. (2015). Multi-criteria inventory
               classification using a new method of evaluation based on distance from average solution (EDAS).
               Informatica, 26(3), 435-451.

        Examples
        --------
        >>> from pymcdm.methods import EDAS
        >>> import numpy as np
        >>> body = EDAS()
        >>> matrix = np.array([[3873, 39.55, 0.27, 0.87, 150, 0.07, 12, 2130],
        ...                    [5067, 67.26, 0.23, 0.23, 40, 0.02, 21, 2200],
        ...                    [2213, 24.69, 0.08, 0.17, 200, 0.04, 35, 570],
        ...                    [6243, 132, 0.07, 0.25, 100, 0.04, 16, 100],
        ...                    [8312, 460.47, 0.05, 0.21, 25, 0.1, 25, 200]])
        >>> weights = np.array([0.131, 0.113, 0.126, 0.125, 0.126, 0.129, 0.132, 0.117])
        >>> types = np.array([-1, -1, -1, 1, 1, -1, 1, 1])
        >>> [round(preference, 3) for preference in body(matrix, weights, types)]
        [0.841, 0.632, 0.883, 0.457, 0.104]
    """
    _tables = [
        TableDesc(caption='Average solution',
                  label='av_sol', symbol='$AV$', rows='C', cols=None),
        TableDesc(caption='Positive distance from Average solution',
                  label='pds', symbol='${PDA}_{i}$', rows='A', cols='C'),
        TableDesc(caption='Negative distance from Average solution',
                  label='nda', symbol='${NDA}_{i}$', rows='A', cols='C'),
        TableDesc(caption='Weighted sum of PDA values',
                  label='sp', symbol='${SP}_{i}$', rows='A', cols=None),
        TableDesc(caption='Weighted sum of NDA values',
                  label='sn', symbol='${SN}_{i}$', rows='A', cols=None),
        TableDesc(caption='Normalized values of SP',
                  label='nsp', symbol='${NSP}_{i}$', rows='A', cols=None),
        TableDesc(caption='Normalized values of SN',
                  label='nsn', symbol='${NSN}_{i}$', rows='A', cols=None),
        TableDesc(caption='Appraisal Score',
                  label='appr_score', symbol='${AS}_{i}$', rows='A', cols=None),
    ]

    def _method(self, matrix, weights, types):
        _, m = matrix.shape
        amatrix = np.mean(matrix, axis=0)

        pda = np.zeros(matrix.shape)
        nda = np.zeros(matrix.shape)

        for j in range(m):
            if types[j] == -1:
                pda[:, j] = (amatrix[j] - matrix[:, j]) / amatrix[j]
                nda[:, j] = (matrix[:, j] - amatrix[j]) / amatrix[j]

            else:
                pda[:, j] = (matrix[:, j] - amatrix[j]) / amatrix[j]
                nda[:, j] = (amatrix[j] - matrix[:, j]) / amatrix[j]

        pda = np.where(pda >= 0, pda, 0)
        nda = np.where(nda >= 0, nda, 0)

        sp = np.sum(weights * pda, axis=1)
        sn = np.sum(weights * nda, axis=1)

        nsp = sp / np.max(sp, axis=0)
        nsn = 1 - sn / np.max(sn, axis=0)

        score = (nsp + nsn) / 2

        return amatrix, pda, nda, sp, sn, nsp, nsn, score
