# Copyright (c) 2020-2023 Andrii Shekhovtsov

from itertools import product
from functools import reduce

import numpy as np

from .mcda_method import MCDA_method
from ..validators import cvalues_validator, matrix_cvalues_validator
from ..io import TableDesc


def _TFN(a, m, b):
    def tfn(x):
        res = np.zeros(x.shape)
        mask = x == m
        res[mask] = 1

        mask = np.logical_and(x > a, x < m)
        res[mask] = (x[mask] - a) / (m - a)

        mask = np.logical_and(x < b, x > m)
        res[mask] = (b - x[mask]) / (b - m)
        return res

    return tfn


class COMET(MCDA_method):
    """ Characteristic Objects METhod (COMET).

        COMET is a method based on characteristic objects on the basis of which preference of the deicision variants is
        calculated [#comet1]_. Due to this dependence the method is resistant to the phenomenon of ranking reversal paradox.

        Read more in the User Guide.

        Parameters
        ----------
           cvalues : ndarray or list of lists
               Each row represent characteristic values for each criteria.

           expert_function : callable
               Function to rate CO. Matrix with CO as rows is passed as
               an argument. Function should return vector which will be used 
               as SJ and the MEJ matrix.
               If MEJ was not build None should be returned.

               Signature of the function should be as followed:
                   rate_function(co: np.array) -> np.array, np.array or None

               Please, see the implementation of ManualExpert and MethodExpert
               in the pymcdm.comet_tools submodule if you want to create your
               own custom expert_function.

        References
        ----------
        .. [#comet1] Sałabun, W. (2015). The Characteristic Objects Method: A New Distance‐based Approach to Multicriteria
               Decision‐making Problems. Journal of Multi‐Criteria Decision Analysis, 22(1-2), 37-50.

        Examples
        --------
        >>> from pymcdm.methods import COMET, TOPSIS
        >>> from pymcdm.methods.comet_tools import MethodExpert
        >>> import numpy as np
        >>> matrix = np.array([[64, 128, 2.9, 4.3, 3.2, 280, 495, 24763, 3990],
        ...                    [28, 56, 3.1, 3.8, 3.8, 255, 417, 12975, 2999],
        ...                    [8, 16, 3.5, 5.3, 4.8, 125, 636, 5725, 539],
        ...                    [12, 24, 3.7, 4.8, 4.5, 105, 637, 8468, 549],
        ...                    [10, 20, 3.7, 5.3, 4.9, 125, 539, 6399, 499],
        ...                    [8, 16, 3.6, 4.4, 4.0, 65, 501, 4834, 329],
        ...                    [6, 12, 3.7, 4.6, 4.2, 65, 604, 4562, 299],
        ...                    [16, 32, 3.4, 4.9, 4.2, 105, 647, 10428, 799],
        ...                    [8, 16, 3.6, 5.0, 4.5, 125, 609, 5615, 399],
        ...                    [18, 36, 3.0, 4.8, 4.3, 165, 480, 8848, 979],
        ...                    [24, 48, 3.8, 4.5, 4.0, 280, 509, 13552, 1399],
        ...                    [28, 56, 2.5, 3.8, 2.8, 205, 376, 8585, 10000]])
        >>> cvalues = np.vstack((
        ...     np.min(matrix, axis=0),
        ...     np.max(matrix, axis=0)
        ... )).T
        >>> types = np.array([1, 1, 1, 1, 1, -1, 1, 1, -1])
        >>> weights = np.array([1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9])
        >>> body = COMET(cvalues, MethodExpert(TOPSIS(), weights, types))
        >>> [round(preference, 4) for preference in body(matrix)]
        [0.5433, 0.3447, 0.6115, 0.6168, 0.6060, 0.4842, 0.5516, 0.6100, 0.5719, 0.4711, 0.4979, 0.1452]
    """
    _tables = [
        TableDesc(caption='Final preference value',
                  label='pref', symbol='$P_i$', rows='A', cols=None)
    ]

    def __init__(self, cvalues, expert_function):
        cvalues_validator(cvalues)

        co = product(*cvalues)
        co = np.array(list(co))

        # Determine how MEJ and SJ is calculated
        sj, mej = expert_function(co)
        self.mej = mej
        if sj.shape[0] != co.shape[0] or (mej is not None and not mej.shape[0] == mej.shape[1] == co.shape[0]):
            raise ValueError(
                    'Expert function must returns vector with same length as number of characteristic objects. '
                    'And the None or MEJ matrix which is square matrix with same size as length of characteristic '
                    'objects.'
                    f'Expected length: {co.shape[0]}, but returned vector has length {sj.shape[0]}. '
                    f'Expected MEJ shape {(co.shape[0], co.shape[0])}, but returned matrix has shape {mej.shape}.'
                    )

        uniq, idx, counts = np.unique(sj, return_counts=True, return_inverse=True)
        k = uniq.shape[0]
        p = (np.arange(k) / (k - 1))[idx]

        self.criterion_number = len(cvalues)
        self.cvalues = cvalues
        self.expert_function = expert_function
        self.p = p
        self.tfns = [COMET._make_tfns(chv) for chv in cvalues]
        
    def __call__(self, matrix,
                 weights=None,
                 types=None,
                 validation=True,
                 verbose=False):
        """Rank alternatives from decision matrix `matrix`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : None
                    Not used in the COMET method.

                types : None
                    Not used in the COMET method.

                validation : bool
                    Enable (True) or disable (False) validation of the input data.
                    For the COMET method only matrix and cvalues are validated.
                    Default is True.

                verbose : bool
                    Explain the MCDA, i.e. provide matrices and vectors from
                    all the steps of the method, instead of return just the
                    preference vector. Default is False.
        """
        matrix = np.asarray(matrix, dtype='float')

        if validation:
            self._additional_validation(matrix, weights, types)

        if verbose:
            return self._method_explained(matrix, weights, types)
        else:
            return self._method(matrix, weights, types)[-1]

    def _method(self, matrix, weights, types):
        tfns = self.tfns

        pref_level_vectors = [[tfn(values) for tfn in tfns_icrit]
                              for values, tfns_icrit in zip(matrix.T, tfns)]

        tfns_values_product = product(*pref_level_vectors)
        multiplayed_co = (reduce(lambda a, b: a * b, co_values) * p
                          for p, co_values in zip(self.p, tfns_values_product))
        return sum(multiplayed_co),

    def _additional_validation(self, matrix, weights, types):
        matrix_cvalues_validator(matrix, self.cvalues)

    def get_MEJ(self):
        """ Return the Matrix Expert Judgment (MEJ) generated from the feature object comparisons. """
        if self.mej is not None:
            return self.mej

        p = self.p
        lenp = len(p)
        mej = np.diag(np.ones(lenp) / 2)
        for i in range(lenp):
            for j in range(i + 1, lenp):
                if p[i] < p[j]:
                    mej[i, j] = 0.0
                    mej[j, i] = 1.0
                elif p[i] == p[j]:
                    mej[i, j] = 0.5
                    mej[j, i] = 0.5
                else:
                    mej[i, j] = 1.0
                    mej[j, i] = 0.0
        self.mej = mej
        return mej

    @staticmethod
    def _make_tfns(chv):
        tfns = []
        # First TFN
        tfns.append(_TFN(chv[0], chv[0], chv[1]))

        for i in range(1, len(chv) - 1):
            tfns.append(_TFN(chv[i - 1], chv[i], chv[i + 1]))

        # Last TFN
        tfns.append(_TFN(chv[-2], chv[-1], chv[-1]))

        return tfns

    @staticmethod
    def make_cvalues(matrix, numbers_of_cvalues=3):
        """ Returns characteristic values matrix with `nubmers_of_cvalues` cvalues for each criterion. Characteristic values are generated equally from min to max.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix.
                    Alternatives are in rows and Criteria are in columns.
                numbers_of_cvalues : int, optional
                    Number of characteristic value for each criterion. Default value is 3.

            Returns
            -------
                cvalues : ndarray
                    Characteristic values for COMET method.

            Examples
            --------
            >>> import numpy as np
            >>> from pymcdm.methods import COMET, TOPSIS
            >>> from pymcdm.methods.comet_tools import MethodExpert
            >>> matrix = np.array([[ 96, 145, 200],
                                   [100, 145, 200],
                                   [120, 170,  80],
                                   [140, 180, 140],
                                   [100, 110,  30]])
            >>> types = np.ones(3)
            >>> weights = np.ones(3)/3
            >>> body = COMET(cvalues,
                             MethodExpert(TOPSIS(), weights, types))

            >>> preferences = body(matrix)
            >>> np.round(preferences, 4)
            array([0.5   , 0.5455, 0.5902, 0.9118, 0.0227])
        """
        return_dtype = 'object'
        if isinstance(numbers_of_cvalues, int):
            numbers_of_cvalues = [numbers_of_cvalues] * matrix.shape[1]
            return_dtype = 'float64'

        return np.array([
            np.linspace(np.min(col), np.max(col), noc)
            for noc, col in zip(numbers_of_cvalues, matrix.T)
        ], dtype=return_dtype)
