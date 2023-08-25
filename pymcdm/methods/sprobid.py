import numpy as np

from pymcdm.methods.probid import PROBID

class SPROBID(PROBID):
    _captions = PROBID._captions[:6] + [
        'Overall positive-ideal distance.',
        'Overall negative-ideal distance.',
        'Final preference values.'
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

        return (Si_pos_ideal, Si_neg_ideal, p)
