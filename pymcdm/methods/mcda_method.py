# Copyright (c) 2020,2022 Andrii Shekhovtsov

from abc import ABC
import numpy as np
from ..helpers import rankdata

class MCDA_method(ABC):
    _reverse_ranking = True

    def __call__(self, matrix, weights, types,
                 skip_validations=False,
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

                skip_validations : bool
                    Skip all the validations made when alternatives
                    are evaluating. Default is False.

                explained_call : bool
                    Explain the MCDA, i.e. provide matrices and vectors from
                    all the steps of the method, instead of return just the
                    preference vector. Default is False.
        """
        matrix = np.array(matrix)
        weights = np.array(weights)
        types = np.array(types)
        if not skip_validations:
            self._validate_input_data(matrix, weights, types)

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


    def rank(self, a):
        return rankdata(a, reverse=self._reverse_ranking)

