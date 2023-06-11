# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022-2023 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

def ranking_flows(rankings,
                  labels=None,
                  colors=None,
                  alt_indices=None,
                  space=0.1,
                  main_plot_kwargs=dict(),
                  missing_plot_kwargs=dict(),
                  marker_plot_kwargs=dict(),
                  better_grid=False,
                  ax=None):
    """ Visualize changes in rankings for several different rankings.
        Could be also used to visualize data from leave_one_out_rr helper
        function. In this case zeros in rankings are treated as missing values
        and drawn using another linestyle.

    Parameters
    ----------
        rankings : ndarray
            ndarray with rankings from different methods.
            Ranking from different methods should be in rows.
            Zeros treated as missing values (alternatives).

        labels : list of str or None
            Labels or name for rankings for xticklabels.
            If None, the rankings would be named R1, R2, etc.

        colors : Iterable or None
            Colors for lines. If list of the colors is shorter then number
            of rankings then colors will be cycled.

        alt_indices : Iterabla or None
            It is possible to display only part of the alternatives, therefore
            we need to label them correctly. Provide list of alternative
            indices to label alternatives. Notice, that index 0 is for A1, etc.

        space : float
            Length of horizontal line around vertical bars. It also determines
            distance to alternative labels.

        main_plot_kwargs : dict
            Keyword arguments to pass into plot function (lines). Determine
            style of normal alternatives in rankings (not missing ones).

        missing_plot_kwargs : dict
            Keyword arguments to pass into plot function (lines). Determine
            style of missing alternatives in rankings.

        marker_plot_kwargs : dict
            Keyword arguments to pass into plot function (lines). Determine
            style of markers (points) on the lines.

        better_drid : bool
            If better grid should be used. Here, it means that horizontal grid
            lines will be shorter and not be drawn under text labels on sides
            of the plot. Default is False.

        ax : Axes or None
            Axes object to draw on. If None current Axes will be used.

    Returns
    -------
        ax : Axes
            Axes object on which plot were drawn.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from pymcdm.visuals import ranking_flows
    >>> rankings = np.array([
    ...     [1, 2, 3, 4, 5],
    ...     [2, 3, 1, 5, 4],
    ...     [3, 2, 5, 1, 4],
    ...     [2, 3, 5, 1, 4],
    ...     [2, 3, 1, 5, 4],
    ... ])
    >>> ranking_flows(rankings)
    >>> plt.show()
    >>> rankings = np.array([
    ...     [1, 2, 3, 4, 5],
    ...     [2, 0, 1, 4, 3],
    ...     [3, 2, 0, 1, 4],
    ...     [2, 3, 4, 1, 0],
    ...     [2, 3, 1, 0, 4],
    ...     [1, 2, 3, 4, 5],
    ... ])
    >>> ranking_flows(rankings, better_grid=True)
    >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    rankings = np.array(rankings)

    # If colors list is not provided, use default matplotlib colors
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # color_picker[i] will determine which color from colors list should be
    # chosen for this alternative. This way, color cycle will be ordered by
    # positions in the first rankings and not by order of alternatives.
    color_picker = np.zeros(rankings.shape[1], dtype='int')
    color_picker[np.argsort(rankings[0])] = np.arange(rankings.shape[1],
                                                      dtype='int')
    # Ensure that rankings is array
    rankings = np.array(rankings)

    # Define array of alternative indices if not provided
    if alt_indices is None:
        alt_indices = range(rankings.shape[1])

    # Define array of rankings names if not provided
    if labels is None:
        labels = [f'$R_{{{i + 1}}}$' for i in range(rankings.shape[0])]
    elif len(labels) != rankings.shape[0]:
        raise ValueError('Length of labels should be equal to number of ranking.')

    # Define default styles for plots
    main_plot_kwargs = dict(
            linewidth=2,
            ) | main_plot_kwargs

    missing_plot_kwargs = dict(
            linewidth=2,
            linestyle='--',
            alpha=0.7,
            zorder=10
            ) | missing_plot_kwargs

    marker_plot_kwargs = dict(
            linestyle=' ',
            marker='o'
            ) | marker_plot_kwargs

    # Visualisation is made alternative by alternative.
    for ai in range(rankings.shape[1]):
        # For each alternative we collect points to draw line before and after
        # missing value (0), and also markers
        lines_before = []
        lines_after = []
        markers = []
        # Until we met 0 for this alternative, we collect lines_before,
        # after zero we will collect lines_after
        lines = lines_before

        for i in range(rankings.shape[0]):
            if rankings[i, ai] != 0:
                lines.append((i - space, rankings[i, ai]))
                lines.append((i + space, rankings[i, ai]))
                markers.append((i, rankings[i, ai]))
            else:
                lines = lines_after

        # Add same colors for every object to be drawn
        c = colors[color_picker[ai] % len(colors)]
        main_plot_kwargs['color'] = c
        missing_plot_kwargs['color'] = c
        marker_plot_kwargs['color'] = c

        if lines_before:
            ax.plot(*zip(*lines_before), **main_plot_kwargs)

        if lines_after:
            ax.plot(*zip(*lines_after), **main_plot_kwargs)

        # Draw lines in another style for missing alternatives (if any)
        if lines_before and lines_after:
            ax.plot(*zip(*[lines_before[-1], lines_after[0]]),
                        **missing_plot_kwargs)

        # Add markers with different functions, so we don't have markers on
        # horizontal lines near the vertical ones (space)
        ax.plot(*zip(*markers), **marker_plot_kwargs)

        # Add alternative labels in color of line for this alternative
        ax.text(- space * 1.5,
                rankings[0, ai],
                f'$A_{{{alt_indices[ai] + 1}}}$',
                color=c,
                ha='right', va='center', fontsize='medium')
        ax.text(rankings.shape[0] - 1 + space * 1.5,
                rankings[-1, ai],
                f'$A_{{{alt_indices[ai] + 1}}}$',
                color=c,
                ha='left', va='center', fontsize='medium')

    ax.set(
        xticks=range(rankings.shape[0]),
        xticklabels=labels,
        xlim=(-0.5, rankings.shape[0] - 0.5),
        ylabel='Position in ranking',
        yticks=range(1, rankings.shape[1] + 1),
        ylim=(0.5, rankings.shape[1] + 0.5)
    )

    if better_grid:
        ax.grid(alpha=0.5, axis='x', linestyle='--',
                linewidth=0.9, color='#CCCCCC')
        for i in range(1, rankings.shape[1] + 1):
            plt.plot([0, rankings.shape[0] - 1], [i, i], linewidth=0.9,
                     linestyle='--', alpha=0.5, zorder=-1, color='#CCCCCC')
    else:
        ax.grid(alpha=0.5, linestyle='--')

    return ax
