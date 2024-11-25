# Copyright (c) 2024 Andrii Shekhovtsov
import os
from abc import ABC, abstractmethod

import numpy as np

from itertools import combinations
from ...validators import validate_pairwise_matrix, validate_scoring


# TODO group the methods in this class and add some comments
# TODO AHP and RANCOM tests + docs + examples
class PairwiseWeightsBase(ABC):
    tie_value: float | int = None
    user_answer_map: dict[str, float | int] = None

    def __init__(self, ranking=None, scoring=None, object_names=None, matrix=None, filename=None):
        if sum(obj is not None for obj in (ranking, scoring, object_names, matrix, filename)) != 1:
            raise ValueError('One of the arguments `ranking`, `scoring`, `object_names`,'
                             '`matrix` or `filename` should be provided!')

        if scoring is not None:
            scoring = np.array(scoring)  # Make copy here because we will modify it
            validate_scoring(scoring)
            idx = np.argsort(scoring)
            scoring[idx] = scoring[idx][::-1]
            self.ranking = scoring
        elif ranking is not None:
            ranking = np.asarray(ranking)
            validate_scoring(ranking)
            self.ranking = ranking
        else:
            self.ranking = None

        self.object_names = object_names

        if filename is not None:
            matrix = np.loadtxt(filename, delimiter=',')

        if matrix is not None:
            validate_pairwise_matrix(matrix, self.user_answer_map.values(), self._answer_mapper)
            self.matrix = matrix
        else:
            self.matrix = None

        self.weights = None

    def __call__(self):
        # If we already have weights, then just return them
        if self.weights is not None:
            return self.weights

        if self.matrix is None:
            # If we don't have matrix or weights, then calculate matrix and weights
            # either from ranking or from pairwise comparison
            if self.ranking is not None:
                self.matrix = self._identify(self.ranking, self._compare_ranking)
            elif self.object_names is not None:
                self.matrix = self._identify(self.object_names, self._compare_pairwise)

        # Now we should have matrix, therefore we can create weights
        # As the matrix is created with internal functions
        # or validated in init we don't need any validators here
        self.weights = self._matrix_to_weights()
        return self.weights

    def _compare_pairwise(self, i, j):
        print(self._question(self.object_names[i], self.object_names[j]))

        ans = self.user_answer_map.get(input('\nYour answer: ').strip(), None)
        while ans is None:
            print(f'Provide valid option: {self.user_answer_map.keys()}!')
            ans = self.user_answer_map.get(input('\nYour answer: ').strip(), None)
        return ans

    def _identify(self, objects, comparison_func):
        n = len(objects)
        matrix = np.diag([float(self.tie_value)] * n)

        for i, j in combinations(range(n), 2):
            ans = comparison_func(i, j)
            matrix[i, j] = ans
            matrix[j, i] = self._answer_mapper(ans)

        return matrix

    def to_csv(self, filename: str, allow_overwrite: bool = False):
        if self.matrix is None:
            raise ValueError('Matrix is not identified yet.')

        if not filename.endswith('.csv'):
            filename = filename + '.csv'

        if os.path.exists(filename) and not allow_overwrite:
            raise FileExistsError(f'{filename} is exist! To override run the method with allow_overwrite=True.')

        np.savetxt(filename, self.matrix, delimiter=',', fmt='%0.6f')

    @abstractmethod
    def _answer_mapper(self, ans):
        pass

    @abstractmethod
    def _matrix_to_weights(self):
        pass

    @abstractmethod
    def _compare_ranking(self, i, j):
        pass

    @staticmethod
    @abstractmethod
    def _question(a, b):
        pass

