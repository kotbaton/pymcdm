# Copyright (c) 2020,2022 Andrii Shekhovtsov

from abc import ABC
from ..helpers import rankdata


class MCDA_method(ABC):
    reverse_ranking = True

    def __call__(self, matrix, weights, types, *args, **kwargs):
        """Rank alternatives from decision matrix `matrix`, with criteria weights `weights` and criteria types `types`.

        Parameters
        ----------
            matrix : ndarray
                Decision matrix / alternatives data.
                Alternatives are in rows and Criteria are in columns.

            weights : ndarray
                Criteria weights. Sum of the weights should be 1. (e.g. sum(weights) == 1)

            types : ndarray
                Array with definitions of criteria types:
                1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.

            *args: is necessary for methods which reqiure some additional data.

            **kwargs: is necessary for methods which reqiure some additional data.
        """
        pass

    @staticmethod
    def _validate_input_data(matrix, weights, types):
        if matrix.shape[1] != weights.shape[0] and weights.shape[0] != len(types):
            raise ValueError(f'Number of criteria should be same as number of weights and number of types')

    def rank(self, a):
        return rankdata(a, reverse=self.reverse_ranking)

