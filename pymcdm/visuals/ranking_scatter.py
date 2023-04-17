# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def ranking_scatter(r1, r2, draw_labels=True, text_offset=0.05, scatter_kwargs=dict(), plot_kwargs=dict(), text_kwargs=dict(), ax=None):
    """ Draw visual comparison between two rankings.

        Parameters
        ----------
            r1 : ndarray
                First ranking.

            r2 : ndarray
                Second ranking.

            draw_labels : bool
                If alternative labels should be drawn on the plot. Default if True.

            text_offset : float
                Offset for the text from scatter point in x and y coordinates. Could be useful if text overlaps with points. Default is 0.05.

            scatter_kwargs : dict
                Keyword arguments to pass into scatter function.

            plot_kwargs : dict
                Keyword arguments to pass into plot function (diagonal line).

            text_kwargs : dict
                Keyword arguments to pass into text function.

            ax : Axes
                Axes object to draw on.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.
    """
    if ax is None:
        ax = plt.gca()

    m = int(max(max(r1), max(r2)))

    scatter_kwargs = dict(
        c='k',
    ) | scatter_kwargs

    ax.scatter(r1, r2, **scatter_kwargs)

    plot_kwargs = dict(
        c='k',
        linestyle='--',
        alpha=0.7
    ) | plot_kwargs

    ax.plot([1, m], [1, m], **plot_kwargs)

    text_kwargs = dict(
    ) | text_kwargs

    if draw_labels:
        for i, (r1i, r2i) in enumerate(zip(r1, r2)):
            ax.text(r1i + text_offset, r2i + text_offset, f'$A_{{{i + 1}}}$', **text_kwargs)

    ax.grid(alpha=0.5, linestyle='--')
    ax.set_axisbelow(True)

    ax.set_xlabel('Ranking 1')
    ax.set_xticks(range(1, m + 1))

    ax.set_ylabel('Ranking 2')
    ax.set_yticks(range(1, m + 1))

    return ax
