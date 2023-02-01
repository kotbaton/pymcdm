import numpy as np
import matplotlib.pyplot as plt

def correlation_plot(cors, labels=None, ax=None):
    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = [f'$R_{{{i}}}$' for i in range(len(cors))]

    ax.plot(range(len(labels)), cors, lw=1, ls='--', marker='*', markersize=8, color='green')
    ax.fill_between(range(len(labels)), [np.min(cors) - 0.5] * len(labels), cors, color='green', alpha=0.2)

    spacing = max((np.max(cors) - np.min(cors)) * 0.05, 0.05)
    for i, c in enumerate(cors):
        ax.text(i, c - spacing, f'{c:0.3f}', color='green', ha='center', va='top')

    ax.set_ylabel('$r_w$')

    ax.grid(ls='--', alpha=0.5)
    ax.set_axisbelow(True)

    ax.tick_params(bottom=False)
