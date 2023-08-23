# Copyright (c) 2020,2022 Andrii Shekhovtsov

from abc import ABC, abstractmethod
import numpy as np
from ..helpers import rankdata

class MCDA_method(ABC):
    _reverse_ranking = True
    _captions = []

    def __call__(self, matrix, weights, types,
                 skip_validation=False,
                 explained_call=False):
        """Rank alternatives from decision matrix `matrix`, with criteria 
           weights `weights` and criteria types `types`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : ndarray
                    Criteria weights. Sum of the weights should be 1. (e.g.
                    sum(weights) == 1)

                types : ndarray
                    Array with definitions of criteria types:
                    1 if criteria is profit and -1 if criteria is cost for 
                    each criteria in `matrix`.

                skip_validation : bool
                    Skip all the validations made when alternatives
                    are evaluating. Default is False.

                explained_call : bool
                    Explain the MCDA, i.e. provide matrices and vectors from
                    all the steps of the method, instead of return just the
                    preference vector. Default is False.
        """
        matrix = np.array(matrix, dtype='float')
        weights = np.array(weights, dtype='float')
        types = np.array(types)
        if not skip_validation:
            MCDA_method._validate_input_data(matrix, weights, types)
            if getattr(self, 'bounds', None) is not None:
                MCDA_method._validate_bounds(self.bounds, matrix.shape[1])

        if explained_call:
            return self._method_explained(matrix, weights, types)
        else:
            return self._method(matrix, weights, types)[-1]

    @staticmethod
    def _validate_input_data(matrix, weights, types):
        if (matrix.shape[1] != weights.shape[0]
            or weights.shape[0] != len(types)):
            raise ValueError('Number of criteria should be same as number of '
                             'weights and number of types')

        if abs(weights.sum() - 1) >= 0.01 or np.any(weights <= 0):
            raise ValueError('Weights should be positive and its sum should '
                             'be equal one. Now, sum of the weights is '
                             f'{weights.sum()}.')

        if np.sum(np.abs(types)) != types.shape[0]:
            raise ValueError('Types array should only contains values -1 '
                             'or 1.')

    @staticmethod
    def _validate_bounds(bounds, ncrit):
        if bounds.shape[0] != ncrit:
            raise ValueError('Number of criteria bounds should be same as '
                             'number of weights and number of types')
        if np.any(bounds[:, 0] == bounds[:, 1]):
            eq = np.arange(bounds.shape[0])[bounds[:, 0] == bounds[:, 1]]
            raise ValueError(
                    f'Bounds for criteria {eq} are equal. Consider changing'
                    f'min and max values for this criterion, '
                    f'delete this criterion or use another MCDA method.'
                )
        if np.any(bounds[:, 0] >= bounds[:, 1]):
            eq = np.arange(bounds.shape[0])[bounds[:, 0] >= bounds[:, 1]]
            raise ValueError(f'Lower bound of criteria {eq} is bigger or '
                              'equal to upper bound.')

        # TODO: think about validation of ESP and ref_ideal in RIM
        # if esp is not None and bounds.shape[0] != esp.shape[0]:
        #     raise ValueError(
        #             'Bounds and ESP should describe the same number of'
        #             'criteria, i.e. bounds.shape[0] should be equal to esp.shape[0].'
        #         )

    def _method_explained(self, matrix, weights, types):
        return tuple(zip(
            self._captions,
            self._method(matrix, weights, types)
            ))

    def rank(self, a):
        return rankdata(a, reverse=self._reverse_ranking)

    @abstractmethod
    def _method(self, matrix, weights, types):
        pass

