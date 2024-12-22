# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from ..methods.probid import PROBID
from ..io import TableDesc

class SPROBID(PROBID):
    _tables = PROBID._tables[:6] + [
        TableDesc(caption='Overall positive-ideal distance',
                  label='pi_dist', symbol='$S_{i(pos-ideal)}$', rows='A', cols=None),
        TableDesc(caption='Overall negative-ideal distance',
                  label='ni_dist', symbol='$S_{i(neg-ideal)}$', rows='A', cols=None),
        TableDesc(caption='Final preference values',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def _final_preference_calculation(self, Si, Si_average):
        m = Si.shape[0]

        Si_pos_ideal = np.zeros(m)
        Si_neg_ideal = np.zeros(m)

        if m >= 4:
            for k in range(1, m // 4 + 1):
                Si_pos_ideal += Si[:, k - 1] / k

            for k in range(m + 1 - (m // 4), m + 1):
                Si_neg_ideal += Si[:, k - 1] / (m - k + 1)

        else:
            Si_pos_ideal = Si[0]
            Si_neg_ideal = Si[-1]

        p = Si_neg_ideal / Si_pos_ideal

        return Si_pos_ideal, Si_neg_ideal, p
