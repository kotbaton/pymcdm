# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .ranking_flows import ranking_flows
from .correlation_plot import correlation_plot

def rankings_flow_correlation(rankings,
                              correlations,
                              labels=None,
                              correlation_name='Correlation',
                              correlation_ax_size='25%',
                              correlation_plot_kwargs=dict(),
                              ranking_flows_kwargs=dict(),
                              ax=None):
    """ Visualize changes in rankings for several different rankings. As well
        as show the correlation change for this rankings. Main purpose of this
        function is to visualize the data from `leave_one_out_rr` function,
        however it also could visualize manually prepared rankings.

        This function will divide ax into two different axes
        to draw both plots.

        Parameters
        ----------
            rankings : ndarray
                ndarray with rankings from different methods.
                Ranking from different methods should be in rows.
                Zeros treated as missing values (alternatives).

            correlations : Iterable
                Iterable with correlation values which should be displayed.

            labels : list of str or None
                Labels or name for rankings for xticklabels.
                If None, the rankings would be named R1, R2, etc.

            colors : Iterable or None
                Colors for lines. If list of the colors is shorter then number
                of rankings then colors will be cycled.

            correlation_name : str
                Str with correlation name which should be displayed as ylabel on
                correlation plot. Default is 'Correlation'.

            correlation_ax_size : str
                Valid argument for matplotlib AxisDivider, size of the correlation
                plot relatively to full height of the plot. Default is '25%'.

            correlation_plot_kwargs : dict
                Kwargs to be passed into `correlation_plot` function.

            ranking_flows_kwargs : dict
                Kwargs to be passed into `ranking_flows` function.

            ax : Axes or None
                Axes object to draw on. If None current Axes will be used.

        Returns
        -------
            ax : Axes
                Axes object on which ranking flows were drawn.

            cax : Axes
                Axes object on which correlation plot was drawn.

        Examples
        --------
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> import pymcdm as pm
        >>> matrix = np.array([
        ...     [1, 2, 3, 4, 5],
        ...     [2, 3, 1, 5, 4],
        ...     [3, 2, 4, 5, 1],
        ...     [1, 9, 3, 4, 2],
        ...     [5, 2, 3, 6, 1],
        ... ])
        >>> topsis = pm.methods.TOPSIS()
        >>> weights = np.ones(5)/5
        >>> types = np.ones(5)
        >>> args = pm.helpers.leave_one_out_rr(topsis, matrix, weights, types, pm.correlations.weighted_spearman, only_rr=False)
        >>> fig, ax = plt.subplots(figsize=(8, 4))
        >>> pm.visuals.rankings_flow_correlation(*args, ax=ax)
        >>> plt.tight_layout()
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("top", size=correlation_ax_size, pad=0.05)

    correlation_plot(correlations, ylabel=correlation_name, labels=labels, **correlation_plot_kwargs, ax=cax)
    cax.tick_params(bottom=False, labelbottom=False)

    ranking_flows(rankings, labels, **ranking_flows_kwargs, ax=ax)

    cax.set_xlim(ax.get_xlim())

    return ax, cax
