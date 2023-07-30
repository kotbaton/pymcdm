import numpy as np
import matplotlib.pyplot as plt

from .comet_contourf import comet_contourf

def comet_esp_plot(comet,
                   esps,
                   bounds,
                   alternatives=None,
                   ax=None):
    if alternatives is None:
        alternatives = np.array([[], []]).T

    if ax is None:
        ax = plt.gca()

    ax, cax = comet_contourf(
            comet, alternatives,
            num=200, colorbar=True, ax=ax,
            contourf_kwargs=dict(levels=14, vmin=0, vmax=1))

    ax.scatter(esps[:, 0], esps[:, 1], c='orange', marker='*', s=120)

    for k, (x, y) in enumerate(zip(esps[:, 0], esps[:, 1]), 1):
        ax.text(x + (comet.cvalues[0][-1] - comet.cvalues[0][0]) * 0.03,
                y, f'$ESP_{{{k}}}$',
                color='orange', fontweight='bold', fontsize=12)

    ax.set_xlabel('$C_1$')
    ax.set_ylabel('$C_2$')

    ax.set_xticks(np.linspace(*bounds[0], 5))
    ax.set_yticks(np.linspace(*bounds[1], 5))

    cax.set_yticks(np.linspace(0, 1, 5))
    cax.set_ylim(0, 1)

    return ax, cax
