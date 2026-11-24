# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
import matplotlib.pyplot as plt


def weights_intervals(lower, upper,
                      weights=None,
                      labels=None,
                      color='C0',
                      bar_kwargs=dict(),
                      scatter_kwargs=dict(),
                      ax=None):
    """ Visualise intervals of criteria weights, e.g. the ranges of all optimal weights of the nonlinear BWM
        model (`BWM.get_weight_intervals`), as horizontal bars, optionally together with a vector of weights.

        Parameters
        ----------
            lower : ndarray
                Lower bounds of the weights of the criteria.

            upper : ndarray
                Upper bounds of the weights of the criteria.

            weights : ndarray or None
                Weights of the criteria drawn as markers on the intervals. If None, only the intervals are drawn.

            labels : list or None
                Labels of the criteria. If None, labels C_1, C_2, ... are used.

            color : str
                Color of the intervals and markers. Default is 'C0'.

            bar_kwargs : dict
                Keyword arguments to pass into the barh function which draws the intervals.

            scatter_kwargs : dict
                Keyword arguments to pass into the scatter function which draws the weights.

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
        >>> fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
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

    # The first criterion is at the top
    y = np.arange(n)[::-1]
    half = 0.22

    bar_kwargs = dict(height=2 * half, color=color, alpha=0.35, linewidth=0) | bar_kwargs
    ax.barh(y, upper - lower, left=lower, **bar_kwargs)
    for yi, lo, hi in zip(y, lower, upper):
        # Ends of the intervals, visible also for degenerate intervals
        ax.plot([lo, lo], [yi - half, yi + half], color=color, linewidth=2)
        ax.plot([hi, hi], [yi - half, yi + half], color=color, linewidth=2)

    if weights is not None:
        scatter_kwargs = dict(s=60, color=color, edgecolor='k', linewidth=1.5, zorder=3,
                              label='Weights') | scatter_kwargs
        ax.scatter(weights, y, **scatter_kwargs)
        ax.legend(loc='lower right')

    ax.set_yticks(y, labels=labels)
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlim(0, upper.max() * 1.1 if upper.max() > 0 else 1)
    ax.set_xlabel('Weight value')
    ax.set_ylabel('Criteria')
    ax.grid(alpha=0.5, linestyle='--')
    ax.set_axisbelow(True)

    return ax
