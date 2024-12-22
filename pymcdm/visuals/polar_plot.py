# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.projections.polar as polar


def polar_plot(rankings,
               labels=None,
               colors=None,
               fill=True,
               legend_ncol=5,
               rgrid_kwargs=dict(),
               plot_kwargs=dict(),
               fill_kwargs=dict(),
               ax=None):
    """ Visualize changes in rankings for several different rankings.

    Parameters
    ----------
        rankings : ndarray
            ndarray with rankings from different methods. Ranking from different methods should be in rows.

        labels : list of str or None
            Labels or name for rankings. If None, the rankings would be named R1, R2, etc.

        colors : Iterable or None
            List or tuple of acceptable for matplolib colors. Will be used as a bar face color. If the list is smaller than number of rankings, then it will cycled.

        fill : bool
            Filling the inside of the rankings function.

        legend_ncol : int
            Number of columns in legend. Default is 5.

        rgrid_kwargs : dict
            Keyword arguments to pass to the rgrid function (polar grid).

        plot_kwargs : dict
            Keyword arguments to pass into plot function (lines).

        fill_kwargs : dict
            Keyword arguments to pass into fill function (same keywords as an Polygon).

        ax : Axes
            Axes object to draw on. Should be created with `projection='polar'` argument.

    Returns
    -------
        ax : Axes
            Axes object on which plot were drawn.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from pymcdm.visuals import polar_plot
    >>> rankings = np.array([
    ...     [1, 2, 3, 4, 5],
    ...     [2, 3, 1, 5, 4],
    ...     [3, 2, 5, 1, 4],
    ...     [2.5, 2.5, 5, 1, 4],
    ...     [2, 3, 1, 5, 4],
    ... ])
    >>> polar_plot(rankings)
    >>> plt.show()
    """

    rankings = np.array(rankings)

    if ax is not None and not isinstance(ax.axes, polar.PolarAxes):
        raise TypeError(f'Wrong type of axes. Pass projection="polar" when creating the axes.')

    if ax is None:
        ax = plt.gca(projection='polar')

    if labels is None:
        labels = [f'$R_{{{i + 1}}}$' for i in range(rankings.shape[0])]

    rankings = np.column_stack([rankings, rankings[:, 0]])

    n, m = rankings.shape

    theta = np.linspace(0, 2 * np.pi, m)

    plot_kwargs = dict(
        linewidth=2,
    ) | plot_kwargs

    fill_kwargs = dict(
        alpha=0.25
    ) | fill_kwargs

    for i in range(len(labels)):
        if colors is not None:
            plot_kwargs['color'] = colors[i % len(colors)]
            fill_kwargs['color'] = colors[i % len(colors)]

        ax.plot(theta, rankings[i, :], '-o', label=labels[i], **plot_kwargs)
        if fill:
            ax.fill(theta, rankings[i, :], label='_nolegend_', **fill_kwargs)

    ax.set_xticks(theta)

    xlabels = ['$A_{' + str(i) + '}$' if i != m else '' for i in range(1, m + 1)]
    ax.set_xticklabels(xlabels)

    ax.set_ylim([0, m+0.2])

    ax.legend(bbox_to_anchor=(0., 1.10, 1., .102), loc='lower left',
           ncol=legend_ncol, mode="expand", borderaxespad=0., fontsize=12)

    ax.grid(True, linestyle='--', alpha=0.7)

    rgrid_kwargs = dict(
        angle=75,
        color='grey'
    ) | rgrid_kwargs
    ax.set_rgrids(np.arange(1, m), **rgrid_kwargs)

    return ax
