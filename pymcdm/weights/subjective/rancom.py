# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .pairwise_weights_base import PairwiseWeightsBase


class RANCOM(PairwiseWeightsBase):
    tie_value = 0.5
    user_answer_map = {'0': 0, '1/2': 0.5, '0.5': 0.5, '1': 1}

    def _answer_mapper(self, ans):
        return 1 - ans

    def _matrix_to_weights(self):
        s = np.sum(self.matrix, axis=1)
        return s / s.sum()

    def _compare_ranking(self, i, j):
        # Smaller value in the ranking represent better option
        if self.ranking[i] < self.ranking[j]:
            return 1
        elif self.ranking[i] > self.ranking[j]:
            return 0
        else:
            return 0.5

    @staticmethod
    def _question(a, b):
        return (f'Please compare two objects:\n'
                f'Choose:\n'
                f'  1: if "{a}" is more important than "{b}";\n' 
                f'1/2: if "{a}" is equally important to "{b}";\n'
                f'  0: if "{b}" is more important than "{a}".')