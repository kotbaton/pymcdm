# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt


def polar_weights(weights,
                  xticklabels=None,
                  bar_kwargs=dict(),
                  legend_ncol=5,
                  colors=None,
                  ax=None):
    """ Function for criteria weights visualisation.

        Parameters
        ----------
            weights : ndarray
                Matrix of weights. Each row is a vector of weights.

            xticklabels : None or Iterable
                Labels for bars (names for the different weighting methods).

            bar_kwargs : dict
                Keywors arguments to pass into bar function.

            legend_ncol : int
                Number of columns in legend.

            colors : Iterable or None
                Colors for bars. If there are less colors then criteria, then colors will be cycled.
            ax : Axes or None
                Axes object to dwaw on.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> from pymcdm.visuals import polar_weights
            >>> w = np.array([[0.3, 0.2, 0.5],
            ...              [0.2, 0.5, 0.3]])
            >>> polar_weights(w)
            >>> plt.show()
    """

    weights = np.array(weights).T

    if ax is None:
        ax = plt.gca(polar=True)

    if xticklabels is None:
        xticklabels = [f'$M_{{{i + 1}}}$' for i in range(weights.shape[1])]

    theta = np.linspace(0.0, 2 * np.pi, weights.shape[1], endpoint=False)

    width = 2 * np.pi / weights.shape[1]

    bar_kwargs = dict(
        linewidth=1,
        edgecolor='black',
        alpha=0.7
    ) | bar_kwargs

    for i, alt in enumerate(weights):
        if colors is not None:
            bar_kwargs['color'] = colors[i % len(colors)]

        if i == 0:
            ax.bar(theta, alt, width=width, label=f'$C_{i + 1}$', **bar_kwargs)
        else:
            ax.bar(theta, alt, width=width, label=f'$C_{i + 1}$', bottom=np.sum(weights[:i], axis=0), **bar_kwargs)

    ax.grid(True, alpha=0.7, linestyle='--')
    ax.set_axisbelow(True)

    ax.set_xticks(theta)
    ax.set_xticklabels(xticklabels)

    ax.set_ylim([0, 1.0])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    ax.legend(bbox_to_anchor=(0., 1.1, 1., .11), loc='lower left',
              ncol=legend_ncol, mode="expand", borderaxespad=0.)

    return ax
