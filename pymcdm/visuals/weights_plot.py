# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def weights_plot(weights,
                 xticklabels=None,
                 bar_kwargs=dict(),
                 legend_ncol=5,
                 colors=None,
                 show_text=False,
                 show_text_threshold=0.0,
                 text_kwargs=dict(),
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

            show_text : bool
                Show the weights values as text on bars.

            show_text_threshold : float
                The smallest value of the weights to be show.
                The values below this threshold wont be shown.

            text_kwargs : dict
                Keyword arguments for weights text.

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
            >>> from pymcdm.visuals import weights_plot
            >>> w = np.array([[0.3, 0.2, 0.5],
            ...              [0.2, 0.5, 0.3]])
            >>> weights_plot(w)
            >>> plt.show()
    """

    weights = np.array(weights).T

    if ax is None:
        ax = plt.gca()

    if xticklabels is None:
        xticklabels = [f'$M_{{{i + 1}}}$' for i in range(weights.shape[1])]

    bar_kwargs = dict(
        linewidth=1,
        edgecolor='black'
    ) | bar_kwargs

    text_kwargs = dict(
        ha='center',
        va='center',
        color='w',
        fontweight='bold',
        fontsize=8
    ) | text_kwargs

    bottom = np.zeros(weights.shape[1], dtype=float)
    for i, alt in enumerate(weights):
        if colors is not None:
            bar_kwargs['color'] = colors[i % len(colors)]

        ax.bar(xticklabels, alt, label=f'$C_{i + 1}$', bottom=bottom, **bar_kwargs)
        bottom += alt

    if show_text:
        bottom = np.zeros(weights.shape[1])
        for j, w in enumerate(weights):
            means = (w / 2) + bottom
            for i in range(len(w)):
                if w[i] >= show_text_threshold:
                    ax.text(
                        i,
                        means[i],
                        f'{w[i]:0.3f}',
                        **text_kwargs
                    )
            bottom += w

    ax.grid(alpha=0.5, linestyle='--')
    ax.set_axisbelow(True)

    ax.set_xticks(range(len(xticklabels)), labels=xticklabels)
    ax.set_xticklabels(xticklabels)
    ax.set_xlabel('Method')

    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel('Weight value')

    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
              ncol=legend_ncol, mode="expand", borderaxespad=0.)

    return ax
