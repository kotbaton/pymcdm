# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def ranking_bar(rankings, labels=None, colors=None, compromise=None,
                spacing=0.1, legend_ncol=5, invert_y=False,
                bar_kwargs=dict(), plot_kwargs=dict(), ax=None):
    """ Function to draw rankings from different methods as a bar plot.

        Parameters
        ----------
            rankings : ndarray
                Rankings which should be drawn. Rankings from different methods should be in rows.

            labels : Iterable or None
                Names of the different rankings. If None placeholder names will be used.

            colors : Iterable or None
                List or tuple of acceptable for matplolib colors. Will be used as a bar face color.
                If the list is smaller than number of rankings, then it will cycled.

            compromise : ndarray
                Compromise ranking to be shown in form of plot line over the bars.

            spacing : float
                Distance between group of bars.

            legend_ncol : int
                Number of columns for legend.

            invert_y : bool
                If True, then y axis will be inverted (smaller values on top). Default is False.

            bar_kwargs : dict
                Keyword arguments for matplolib's bar function.

            plot_kwargs : dict
                Keyword arguments for matplotlib's plot function (for compromise ranking).

            ax : Axes or None
                Axes object to drawn on. If None current Axes will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> from pymcdm.visuals import ranking_bar
            >>> rankings = np.array([
            ...     [1, 2, 3, 4, 5],
            ...     [2, 3, 1, 5, 4],
            ...     [3, 2, 5, 1, 4]
            ... ])
            >>> ranking_bar(rankings)
            >>> plt.show()
            >>> ranking_bar(rankings, compromise=np.mean(rankings, axis=0).astype('int'))
            >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    rankings = np.array(rankings)

    width = 1 / rankings.shape[0] - spacing / 2
    if rankings.shape[0] % 2:
        pads = np.arange(- (rankings.shape[0] // 2 * width),
                         width * np.ceil(rankings.shape[0] / 2),
                         width)
    else:
        pads = np.arange(- (rankings.shape[0] / 2 * width) + width/2,
                         width * rankings.shape[0] / 2,
                         width)

    if labels is None:
        labels = [f'$R_{{{i + 1}}}$' for i in range(rankings.shape[0])]

    bar_kwargs = dict(
        linewidth=1,
        edgecolor='k'
    ) | bar_kwargs

    x = np.arange(rankings.shape[1])
    for i in range(rankings.shape[0]):
        if colors is not None:
            bar_kwargs['color'] = colors[i % len(colors)]
        ax.bar(x + pads[i], rankings[i], width, label=labels[i], **bar_kwargs)

    if compromise is not None:
        plot_kwargs = dict(
            linewidth=2,
            marker='o',
            markersize=10,
            linestyle='--',
            color='k'
        ) | plot_kwargs
        ax.plot(range(len(compromise)), compromise, **plot_kwargs)

    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=legend_ncol, mode="expand", borderaxespad=0.)

    ax.set_axisbelow(True)
    ax.grid(alpha=0.5, linestyle='--', axis='y')

    alts = [f'$A_{{{i + 1}}}$' for i in range(rankings.shape[1])]
    ax.set_xticks(range(len(alts)), labels=alts)

    high = int(np.ceil(np.max(rankings)))
    ax.set_yticks(range(1, high + 1))

    return ax
