# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
import matplotlib.pyplot as plt


def flowsort_flows(phi_plus_r, phi_minus_r, phi_r, phi_a,
                   profiles_type='limiting',
                   category_colors=None,
                   marker_kwargs=dict(),
                   text_kwargs=dict(),
                   ax=None):
    """ Visualise the flows of one alternative against the flows of the reference profiles in the FlowSort method,
        separately for the positive, negative and net flows. Every axis is oriented so that better categories are
        on the right (the axis of the negative flow is reversed). The categories are drawn as coloured bands
        between the limiting profiles (or between the midpoints of the central profiles) and the alternative is
        marked with a triangle.

        Parameters
        ----------
            phi_plus_r : ndarray
                Positive flows of the profiles, computed together with the alternative (the first table of the
                verbose FLOWSORT results).

            phi_minus_r : ndarray
                Negative flows of the profiles (the second table of the verbose FLOWSORT results).

            phi_r : ndarray
                Net flows of the profiles (the third table of the verbose FLOWSORT results).

            phi_a : ndarray
                Positive, negative and net flow of the alternative (one row of the fourth table of the verbose
                FLOWSORT results).

            profiles_type : str
                'limiting' if the profiles are the limits of the categories, 'central' if they are their central
                profiles. Default is 'limiting'.

            category_colors : list or None
                Colors of the categories, from the worst to the best one. If None, shades of the 'Blues'
                colormap are used.

            marker_kwargs : dict
                Keyword arguments to pass into the plot function which draws the alternative.

            text_kwargs : dict
                Keyword arguments to pass into the text function which draws the names of the flows.

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
        >>> from pymcdm.methods.sorting import FLOWSORT
        >>> from pymcdm.visuals import flowsort_flows
        >>> matrix = np.array([[54, 17, 71, 45, 63],
        ...                    [25, 25, 50, 75, 75]])
        >>> profiles = np.array([[0] * 5, [25] * 5, [50] * 5, [75] * 5, [100] * 5])
        >>> weights = np.ones(5) / 5
        >>> types = np.ones(5)
        >>> res = FLOWSORT(profiles)(matrix, weights, types, verbose=True)
        >>> phi_plus_r, phi_minus_r, phi_r, phi_a = [r.data for r in res.results[:4]]
        >>> fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
        >>> ax = flowsort_flows(phi_plus_r[1], phi_minus_r[1], phi_r[1], phi_a[1], ax=ax)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    if profiles_type not in ('limiting', 'central'):
        raise ValueError(f"profiles_type should be 'limiting' or 'central', but is {profiles_type!r}.")

    phi_a = np.asarray(phi_a, dtype=float)
    if phi_a.shape != (3,):
        raise ValueError('phi_a should contain the positive, negative and net flow of the alternative.')
    n = len(phi_plus_r)
    k = n - 1 if profiles_type == 'limiting' else n
    if category_colors is None:
        category_colors = plt.cm.Blues(np.linspace(0.12, 0.45, k))

    rows = [('$\\phi^+$', phi_plus_r, phi_a[0], (0, 1), False),
            ('$\\phi^-$', phi_minus_r, phi_a[1], (0, 1), True),
            ('$\\phi$', phi_r, phi_a[2], (-1, 1), False)]

    marker_kwargs = dict(marker='v', color='C3', markersize=10, zorder=5, linestyle='none') | marker_kwargs

    for y, (name, prof, value, (lo, hi), reverse) in zip([2, 1, 0], rows):
        def pos(v):
            return (hi - v) / (hi - lo) if reverse else (v - lo) / (hi - lo)

        p = pos(np.asarray(prof, dtype=float))
        if profiles_type == 'limiting':
            edges = p
        else:
            edges = np.concatenate([[0], (p[1:] + p[:-1]) / 2, [1]])

        for h in range(k):
            ax.add_patch(plt.Rectangle((edges[h], y - 0.18), edges[h + 1] - edges[h], 0.36,
                                       color=category_colors[h % len(category_colors)], lw=0))
            ax.text((edges[h] + edges[h + 1]) / 2, y + 0.24, f'$C_{{{h + 1}}}$', ha='center', va='bottom',
                    fontsize=8, color='0.3')
        ax.plot([0, 1], [y, y], 'k', lw=1)
        for i, x in enumerate(p):
            ax.plot([x, x], [y - 0.18, y + 0.18], 'k', lw=1.5)
            ax.text(x, y - 0.24, f'$r_{{{i + 1}}}$', ha='center',
                    va='top', fontsize=8)
        ax.plot(pos(value), y, **marker_kwargs)
        ax.text(-0.09, y, name, ha='right', va='center', **text_kwargs)
        ax.text(-0.015, y, f'{hi if reverse else lo:g}', ha='right', va='center', fontsize=7, color='0.4')
        ax.text(1.015, y, f'{lo if reverse else hi:g}', ha='left', va='center', fontsize=7, color='0.4')

    ax.set_xlim(-0.16, 1.06)
    ax.set_ylim(-0.55, 2.55)
    ax.axis('off')

    return ax
