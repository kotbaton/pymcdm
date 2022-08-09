# Copyright (c) 2020 Andrii Shekhovtsov

from itertools import product
from functools import reduce

import numpy as np

from .mcda_method import MCDA_method
from .topsis import TOPSIS


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
    def __init__(self, cvalues, rate_function=None, expert_function=None):
        """Initialize COMET model. It creates CO and rank them using `ranking_method`.

Parameters
----------
    cvalues : ndarray or list of lists
        Each row represent characteristic values for each criteria.

    rate_function : callable
        Function to rate CO without creating MEJ. Matrix with CO as rows is passed as an argument Vector with rates should be retrurn. Better CO should has higher values.

        Signature of the function should be as followed:
            rate_function(co: np.array) -> np.array

    expert_function : callable
        Function which would be used to compare CO on MEJ creation.
        It should fulfill this requirments:
           CO to compare are passed as arguments (a, b)
           if a is better then b return 1,
           if b is better then a return 0,
           if this CO are equaly prefered return 0.5

    If both ranking_method and expert_function are provided, expert_function is preffered.
"""
        # Validate input
        for i, cv in enumerate(cvalues):
            if len(cv) < 2:
                raise ValueError(
                    f'You should provide minimum 2 characteristic value for each criterion. Check criterion with index {i}.'
                    )
            # Check if sorted
            if any(cv[i] >= cv[i+1] for i in range(len(cv)-1)):
                raise ValueError(
                        f'Characteristic values must be sorted in ascending order and does not contain repeated elements. Check criterion with index {i}.'
                    )

        co = product(*cvalues)
        co = np.array(list(co))

        # Determine how MEJ and SJ is calculated
        if expert_function is not None:
            self.mej = COMET._build_mej(co, expert_function)
            sj = np.sum(self.mej , axis=1)
        elif rate_function is not None:
            self.mej = None
            sj = rate_function(co)
            if sj.shape[0] != co.shape[0]:
                raise ValueError(
                        f'Rate function must returns vector with same length as number of characteristic objects. Expected length: {co.shape[0]}, but returned vector has length {sj.shape[0]}.'
                    )
        else:
            raise ValueError('rate_function or expert_function should be provided.')

        k = np.unique(sj).shape[0]

        p = np.zeros(sj.shape[0], dtype=float)
        for i in range(1, k):
            ind = sj == np.max(sj)
            p[ind] = (k - i) / (k - 1)
            sj[ind] = 0

        self.criterion_number = len(cvalues)
        self.cvalues = cvalues
        self.p = p
        self.tfns = [COMET._make_tfns(chv) for chv in cvalues]


    def __call__(self, alts, *args, **kwargs):
        """Rank alternatives from decision matrix `alts`, with criteria weights `weights` and criteria types `types`.

Parameters
----------
    alts : ndarray
        Decision matrix / alternatives data.
        Alternatives are in rows and Criteria are in columns.

    *args and **kwargs are necessary for methods which reqiure some additional data.

Returns
-------
    ndarray
        Preference values for alternatives. Better alternatives have higher values.
"""
        if self.criterion_number != alts.shape[1]:
            raise ValueError(
                    'Number of criteria in decision matrix must be equal to number of criteria in characteristic values.'
                )

        tfns = self.tfns

        pref_level_vectors = [[tfn(values) for tfn in tfns_icrit]
                              for values, tfns_icrit in zip(alts.T, tfns)]

        tfns_values_product = product(*pref_level_vectors)
        multiplayed_co = (reduce(lambda a, b: a*b, co_values) * p
                          for p, co_values in zip(self.p, tfns_values_product))
        return sum(multiplayed_co)


    @staticmethod
    def _build_mej(co, expert_function):
        # Initiate MEJ with diagonal with 0.5 values
        mej = np.diag(np.ones(co.shape[0]) * 0.5)
        for i in range(mej.shape[0]):
            for j in range(i+1, mej.shape[0]):
                v = expert_function(co[i], co[j])
                mej[i, j] = v
                mej[j, i] = 1 - v
        return mej

    def get_MEJ(self):
        if self.mej is not None:
            return self.mej

        # If there's no MEJ then rate_function was used to create SJ and P
        # Now we can create MEJ using P to compare CO.
        p = self.p
        lenp = len(p)
        mej = np.diag(np.ones(lenp)/2)
        for i in range(lenp):
            for j in range(i+1, lenp):
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

        for i in range(1, len(chv)-1):
            tfns.append(_TFN(chv[i-1], chv[i], chv[i+1]))

        # Last TFN
        tfns.append(_TFN(chv[-2], chv[-1], chv[-1]))

        return tfns

    @staticmethod
    def manual_expert(criteria_names):
        """Returns function for manual rating characteristic objects."""
        def manual(a, b):
            # Print CO data
            print(f'{" "*15} | {"a":>9} | {"b":>9}')
            for name, va, vb in zip(criteria_names, a, b):
                print(f'{name[:15]:>15s} | {va:>9} | {vb:>9}')

            # Input from expert
            print('Which one is better?')
            options = {'a': 1.0, 'b': 0.0, '': 0.5}
            inp = None
            while inp not in options:
                inp = input('Input "a", "b" or leave empty if a i b are equaly prefered.\n>>> ')
            return options[inp]
        return manual

    @staticmethod
    def topsis_rate_function(weights, types):
        """Returns function to rate characteristic objects with TOPSIS"""
        topsis = TOPSIS()
        def topsis_rate(co):
            return topsis(co, weights, types)
        return topsis_rate

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
            >>> from pymcdm.methods import COMET
            >>> matrix = np.array([[ 96, 145, 200],
                                   [100, 145, 200],
                                   [120, 170,  80],
                                   [140, 180, 140],
                                   [100, 110,  30]])
            >>> types = np.ones(3)
            >>> weights = np.ones(3)/3
            >>> cvalues = COMET.make_cvalues(matrix)
            >>> body = COMET(cvalues, COMET.topsis_rate_function(weights, types))
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

