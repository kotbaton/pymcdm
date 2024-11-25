# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .pairwise_weights_base import PairwiseWeightsBase


class AHP(PairwiseWeightsBase):
    tie_value = 1
    user_answer_map = {f'1/{v}': 1 / v for v in range(2, 10)} | {str(v): v for v in range(1, 10)}

    # Rao Tummala, V. M., & Ling, H. (1998). A note on the computation of the mean random consistency index
    # of the analytic hierarchy process (AHP). Theory and decision, 44(3), 221-230.
    RI_M = [0, 0, 0.5799, 0.8921, 1.1159, 1.2358, 1.3322, 1.3952, 1.4537, 1.4882, 1.5117, 1.5356, 1.5571, 1.5714,
            1.5831]

    def get_cr(self):
        m = self.matrix
        if m is None:
            ValueError('Matrix is not existed. Model if not identified yet!')

        if m.shape[0] < 3:
            return 0
        if m.shape[0] > len(self.RI_M):
            ValueError(f"Can't calculate CR for the matrix of this size. Max size is {len(self.RI_M)}.")

        eig, _ = np.linalg.eig(m)
        lambda_max = max(eig.real)
        ci = (lambda_max - m.shape[0]) / (m.shape[0] - 1)
        ri = AHP.RI_M[m.shape[0] - 1]
        return ci / ri

    def _answer_mapper(self, ans):
        return 1 / ans

    def _matrix_to_weights(self):
        eig, eig_w = np.linalg.eig(self.matrix)
        w = eig_w[:, np.argmax(np.abs(eig))].real
        return w / w.sum()

    def _compare_ranking(self, i, j):
        if self.ranking[i] == self.ranking[j]:
            return 1

        # Find how
        d = int(max(self.ranking[i], self.ranking[j]) / min(self.ranking[i], self.ranking[j]))
        d = min(d, 9)
        # Smaller value in the ranking represent better option
        if self.ranking[i] < self.ranking[j]:
            return d
        else:
            return 1/d

    @staticmethod
    def _question(a, b):
        return (f'Please compare two objects:\n'
                f'Choose values in scale from 1 to 9 where:'
                f'  1: if "{a}" is equally important to "{b}";\n'
                f'  9: if "{a}" is extremely more important than "{b}";\n'
                f'OR value in scale 1 to 1/9 where:'
                f'  1: if "{b}" is equally important to "{a}";\n'
                f'1/9: if "{b}" is extremely more important than "{a}".')
