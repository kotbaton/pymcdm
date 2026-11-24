# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
import matplotlib.pyplot as plt


def weights_intervals(lower, upper,
                      weights=None,
                      labels=None,
                      colors=None,
                      bar_kwargs=dict(),
                      plot_kwargs=dict(),
                      ax=None):
    """ Visualise intervals of criteria weights, e.g. the ranges of all optimal weights of the nonlinear BWM
        model (`BWM.get_weight_intervals`), optionally together with a vector of weights.

        Parameters
        ----------
            lower : ndarray
                Lower bounds of the weights of the criteria.

            upper : ndarray
                Upper bounds of the weights of the criteria.

            weights : ndarray or None
                Weights of the criteria drawn as markers inside the intervals. If None, only the intervals are
                drawn.

            labels : list or None
                Labels of the criteria. If None, labels C_1, C_2, ... are used.

            colors : list or None
                Colors of the criteria. If None, colors from the default color cycle are used.

            bar_kwargs : dict
                Keyword arguments to pass into the bar function which draws the intervals.

            plot_kwargs : dict
                Keyword arguments to pass into the plot function which draws the weights.

            ax : Axes or None
                Axes object to draw on. If None current Axes object will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.weights.subjective import BWM
        >>> from pymcdm.visuals import weights_intervals
        >>> bwm = BWM(a_b=[2, 1, 4, 3, 8], a_w=[4, 8, 4, 2, 1])
        >>> lower, upper = bwm.get_weight_intervals()
        >>> fig, ax = plt.subplots(figsize=(5, 3.5), dpi=150)
        >>> ax = weights_intervals(lower, upper, bwm(), ax=ax)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    if lower.shape != upper.shape or lower.ndim != 1:
        raise ValueError('lower and upper should be one-dimensional arrays of the same length.')
    if np.any(lower > upper):
        raise ValueError('Every lower bound should not be greater than the upper bound.')
    if weights is not None and np.shape(weights) != lower.shape:
        raise ValueError('weights should have one value for each criterion.')

    n = len(lower)
    if labels is None:
        labels = [f'$C_{{{j + 1}}}$' for j in range(n)]
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    x = np.arange(n)
    bar_kwargs = dict(width=0.6, linewidth=1, edgecolor='k') | bar_kwargs
    # Degenerate intervals are drawn as thin bars so that they remain visible
    height = np.maximum(upper - lower, 0.002 * max(upper.max(), 1e-12))
    for j in range(n):
        ax.bar(x[j], height[j], bottom=lower[j], color=colors[j % len(colors)], **bar_kwargs)

    if weights is not None:
        plot_kwargs = dict(linestyle='none', marker='o', markersize=8, markerfacecolor='w',
                           markeredgecolor='k', markeredgewidth=1.5, label='Weights') | plot_kwargs
        ax.plot(x, weights, **plot_kwargs)
        ax.legend(loc='upper right')

    ax.set_xticks(x, labels=labels)
    ax.set_xlabel('Criteria')
    ax.set_ylabel('Weight value')
    ax.set_ylim(0, upper.max() * 1.1 if upper.max() > 0 else 1)
    ax.grid(alpha=0.5, linestyle='--', axis='y')
    ax.set_axisbelow(True)

    return ax
