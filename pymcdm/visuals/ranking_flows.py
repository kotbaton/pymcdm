# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def ranking_flows(rankings, labels=None, colors=None, spacer=0.2, plot_kwargs=dict(), ax=None):
    """ Visualize changes in rankings for several different rankings.

    Parameters
    ----------
        rankings : ndarray
            ndarray with rankings from different methods. Ranking from different methods should be in rows.

        labels : list of str or None
            Labels or name for rankings. If None, the rankings would be named R1, R2, etc.

        colors : Iterable or None
            Colors for lines. If list of the colors is shorter then number of rankings then colors will be cycled.

        spacer : float
            Length of horizontal line around vertical bars.

        plot_kwargs : dict
            Keyword arguments to pass into plot function (lines).

        ax : Axes or None
            Axes object to draw on. If None current Axes will be used.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from pymcdm.visuals import ranking_flows
    >>> rankings = np.array([
    ...     [1, 2, 3, 4, 5],
    ...     [2, 3, 1, 5, 4],
    ...     [3, 2, 5, 1, 4],
    ...     [2.5, 2.5, 5, 1, 4],
    ...     [2, 3, 1, 5, 4],
    ... ])
    >>> ranking_flows(rankings)
    >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    rankings = np.array(rankings)

    high = int(np.ceil(np.max(rankings)))
    for i in range(rankings.shape[1]):
        ax.plot([i, i], [1, high], 'k', linewidth=3)

    if labels is None:
        labels = [f'$R_{{{i + 1}}}$' for i in range(rankings.shape[0])]
    elif len(labels) != rankings.shape[0]:
        raise ValueError('Length of labels should be equal to number of ranking.')

    plot_kwargs = dict(
        linewidth=2,
    ) | plot_kwargs

    for i in range(rankings.shape[1]):
        if colors is not None:
            plot_kwargs['color'] = colors[i % len(colors)]

        points = []
        markers = []
        for j in range(rankings.shape[0]):
            points.append((j - spacer/2, rankings[j, i]))
            points.append((j + spacer/2, rankings[j, i]))
            markers.append((j, rankings[j, i]))

        line, = ax.plot(*zip(*points), **plot_kwargs, label=f'$A_{{{i + 1}}}$')
        ax.plot(*zip(*markers), marker='o', c=line.get_color(), linestyle=' ')

    ax.set_yticks(range(1, high + 1))
    ax.set_ylabel('Ranking position')

    ax.set_xticks(range(rankings.shape[0]))
    ax.set_xticklabels(labels)
    ax.set_xlabel('Methods')

    ax.set_xlim([-0.5, rankings.shape[0] - 0.5])
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=5, mode="expand", borderaxespad=0.)

    ax.grid(alpha=0.5, linestyle='--')

    plt.tight_layout()
