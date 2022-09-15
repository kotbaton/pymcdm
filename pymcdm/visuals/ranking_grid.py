# Andrii Shekhovtsov (c) 2022

import numpy as np
import matplotlib.pyplot as plt
from .ranking_scatter import ranking_scatter


def ranking_grid(rankings, labels=None, upper=True, correlations=False, ranking_scatter_kwargs=dict(), fig=None):
    if fig is None:
        fig = plt.figure()

    if labels is None:
        labels = [f'$R_{{{i + 1}}}$' for i in range(rankings.shape[0])]

    rankings = np.array(rankings)

    n = rankings.shape[0]
    for i in range(n):
        for j in range(n):
            if (upper and i < j) or (not upper and i > j):
                ax = fig.add_subplot(n, n, i * n + j + 1, aspect='equal')
                ranking_scatter(rankings[i], rankings[j], **ranking_scatter_kwargs, ax=ax)


    plt.tight_layout()
