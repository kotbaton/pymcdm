# Copyright (c) 2020-2024 Andrii Shekhovtsov

from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import ArrayLike

from ..helpers import rankdata
from ..validators import validate_decision_problem
from ..io import MCDA_results


class MCDA_method(ABC):
    _reverse_ranking = True
    _tables = None

    def __call__(self, matrix: ArrayLike, weights: ArrayLike, types: ArrayLike,
                 skip_validation: bool = False,
                 verbose: bool = False):
        """ Rank alternatives from decision matrix `matrix`, with criteria
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

                verbose : bool
                    Explain the MCDA, i.e. provide matrices and vectors from
                    all the steps of the method, instead of return just the
                    preference vector. Default is False.
        """
        matrix = np.asarray(matrix, dtype='float')
        weights = np.asarray(weights, dtype='float')
        types = np.asarray(types)

        if not skip_validation:
            validate_decision_problem(matrix, weights, types)
            self._additional_validation(matrix, weights, types)

        if verbose:
            return self._method_explained(matrix, weights, types)
        else:
            return self._method(matrix, weights, types)[-1]

    def _additional_validation(self, matrix, weights, types):
        return

    def _method_explained(self, matrix, weights, types):
        results = self._method(matrix, weights, types)
        return MCDA_results(
            method=self,
            matrix=matrix,
            results=[t.create_table(r) for t, r in zip(self._tables, results)]
            )

    def rank(self, a):
        return rankdata(a, reverse=self._reverse_ranking)

    @abstractmethod
    def _method(self, matrix, weights, types):
        pass
