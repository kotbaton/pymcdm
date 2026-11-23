# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def sorting_assignments(categories, n_categories,
                        intervals=None,
                        labels=None,
                        colors=None,
                        bar_kwargs=dict(),
                        scatter_kwargs=dict(),
                        ax=None):
    """ Visualise the categories to which a sorting method assigned the alternatives (categories numbered from
        1, the worst one, to `n_categories`, the best one). Optionally, an interval of categories can be drawn for
        every alternative, e.g. from the pessimistic to the optimistic ELECTRE TRI assignment or between the
        FlowSort assignments based on the positive and the negative flows.

        Parameters
        ----------
            categories : ndarray or list
                Category assigned to every alternative.

            n_categories : int
                Number of the categories.

            intervals : ndarray or None
                Matrix with two columns, the lower and the upper category of the interval of every alternative.
                If None, no intervals are drawn.

            labels : list or None
                Labels of the alternatives. If None, labels A_1, A_2, ... are used.

            colors : list or None
                Colors of the categories, from the worst to the best one. If None, shades of the 'Blues' colormap
                are used.

            bar_kwargs : dict
                Keyword arguments to pass into the FancyBboxPatch which draws the intervals.

            scatter_kwargs : dict
                Keyword arguments to pass into the scatter function which draws the assigned categories.

            ax : Axes or None
                Axes object to draw on. If None current Axes object will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.methods.sorting import ELECTRE_TRI
        >>> from pymcdm.visuals import sorting_assignments
        >>> matrix = np.array([[54, 17, 71, 45, 63],
        ...                    [15, 5, 19, 9, 23],
        ...                    [25, 25, 50, 75, 75]])
        >>> profiles = np.array([[25] * 5, [50] * 5, [75] * 5])
        >>> weights = np.ones(5) / 5
        >>> types = np.ones(5)
        >>> thresholds = dict(q=[2] * 5, p=[10] * 5, v=[40] * 5)
        >>> pes = ELECTRE_TRI(profiles, **thresholds, procedure='pessimistic')(matrix, weights, types)
        >>> opt = ELECTRE_TRI(profiles, **thresholds, procedure='optimistic')(matrix, weights, types)
        >>> fig, ax = plt.subplots(figsize=(5, 2.5), dpi=150)
        >>> ax = sorting_assignments(pes, 4, intervals=np.column_stack([pes, opt]), ax=ax)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    categories = np.asarray(categories).astype(int)
    n = len(categories)
    if np.any(categories < 1) or np.any(categories > n_categories):
        raise ValueError(f'Categories should be between 1 and {n_categories}.')
    if labels is None:
        labels = [f'$A_{{{i + 1}}}$' for i in range(n)]
    if colors is None:
        colors = plt.cm.Blues(np.linspace(0.35, 0.85, n_categories))
    if intervals is not None:
        intervals = np.asarray(intervals)
        if intervals.shape != (n, 2):
            raise ValueError('intervals should have one row with two values for every alternative.')

    for h in range(n_categories):
        ax.axvspan(h + 0.5, h + 1.5, color='0.96' if h % 2 else 'white', zorder=0)

    for i, c in enumerate(categories):
        y = n - 1 - i
        color = colors[(c - 1) % len(colors)]
        if intervals is not None:
            lo, hi = intervals[i]
            ax.add_patch(FancyBboxPatch((lo - 0.38, y - 0.22), hi - lo + 0.76, 0.44,
                                        boxstyle='round,pad=0,rounding_size=0.15',
                                        **(dict(color=color, alpha=0.35, lw=0) | bar_kwargs)))
        ax.scatter(c, y, **(dict(s=90, color=color, edgecolor='k', zorder=3) | scatter_kwargs))

    ax.set_xlim(0.5, n_categories + 0.5)
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xticks(range(1, n_categories + 1), [f'$C_{{{h}}}$' for h in range(1, n_categories + 1)])
    ax.set_yticks(range(n), labels[::-1])
    ax.tick_params(length=0)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.set_xlabel('Category (worst $\\rightarrow$ best)')

    return ax
