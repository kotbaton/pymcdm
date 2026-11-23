# Copyright (c) 2026 Bartłomiej Kizielewicz

import re

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def _label_positions(x, y, sizes, offset=0.02):
    """ Greedy placement of the labels of points (all values in axes coordinates, [0, 1]): every label is put in
        the one of eight positions around its point which overlaps the least with the points, the labels already
        placed and the border of the axes. Returns the lower left corners of the labels. """
    candidates = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    placed = []
    for px, py, (w, h) in zip(x, y, sizes):
        best, best_cost = None, np.inf
        for cx, cy in candidates:
            bx = px + offset * cx - (w if cx < 0 else w / 2 if cx == 0 else 0)
            by = py + offset * cy - (h if cy < 0 else h / 2 if cy == 0 else 0)
            m = offset * 0.75
            cost = np.sum((x > bx - m) & (x < bx + w + m) & (y > by - m) & (y < by + h + m))
            for ox, oy, ow, oh in placed:
                ix = max(0.0, min(bx + w, ox + ow) - max(bx, ox))
                iy = max(0.0, min(by + h, oy + oh) - max(by, oy))
                cost += 5 * ix * iy / (w * h)
            if bx < 0 or by < 0 or bx + w > 1 or by + h > 1:
                cost += 3
            if cost < best_cost - 1e-12:
                best, best_cost = (bx, by, w, h), cost
        placed.append(best)
    return [(bx, by) for bx, by, _, _ in placed]


def midia_plane(DI, DAI,
                alpha=0.5,
                fill=True,
                levels=None,
                num=100,
                cmap='Greens',
                colorbar=True,
                labels=None,
                contourf_kwargs=dict(),
                contour_kwargs=dict(),
                scatter_kwargs=dict(),
                text_kwargs=dict(),
                ax=None):
    """ Visualise the alternatives in the plane of the closeness to the ideal point (DI) and the distance from the
        anti-ideal point (DAI) of the MIDIA method, together with the lines of equal final preference
        D(alpha) = alpha DI + (1 - alpha) DAI. The lines can be drawn on a background coloured by D(alpha)
        (`fill=True`) or as labelled dashed lines only (`fill=False`).

        Parameters
        ----------
            DI : ndarray
                Closeness of the alternatives to the ideal point, 1 - dI / d (the second table of the verbose MIDIA
                results).

            DAI : ndarray
                Distance of the alternatives from the anti-ideal point, dAI / d (the third table of the verbose MIDIA
                results).

            alpha : float
                Coefficient alpha of the MIDIA method used to compute D(alpha). Default is 0.5.

            fill : bool
                If True, the background is coloured by D(alpha) with contourf. If False, only labelled dashed
                lines of equal D(alpha) are drawn. Default is True.

            levels : int, ndarray or None
                Levels of D(alpha) passed to contourf (fill=True) or contour (fill=False). If None, 10 equal
                intervals (fill=True) or 4 lines (fill=False) are used.

            num : int
                Number of points in meshgrid (num argument for linspace function). Default is 100.

            cmap : str or Colormap
                Colormap for the background. Default is 'Greens'.

            colorbar : bool
                Add colorbar on the right side of the axis (only if fill=True). Default is True.

            labels : list or None
                Labels of the alternatives. If None, labels A_1, A_2, ... are used.

            contourf_kwargs : dict
                Keyword arguments to pass into contourf function (fill=True).

            contour_kwargs : dict
                Keyword arguments to pass into contour function (fill=False).

            scatter_kwargs : dict
                Keyword arguments to pass into scatter function which draws the alternatives.

            text_kwargs : dict
                Keyword arguments to pass into text function which draws the labels of the alternatives.

            ax : Axes or None
                Axes object to draw on. If None current Axes object will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

            cax : Axes
                Only if fill=True and colorbar=True.
                Axes object on which colorbar were drawn.

        Examples
        --------
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.methods import MIDIA
        >>> from pymcdm.visuals import midia_plane
        >>> matrix = np.array([[20, 3, 91, 50, 80],
        ...                    [16, 50, 100, 11, 62],
        ...                    [11, 50, 97, 25, 68],
        ...                    [10, 100, 85, 10, 50],
        ...                    [2, 36, 76, 5, 53]])
        >>> weights = np.ones(5) / 5
        >>> types = np.ones(5)
        >>> res = MIDIA(alpha=0.5)(matrix, weights, types, verbose=True)
        >>> DI, DAI = res.results[1].data, res.results[2].data
        >>> fig, ax = plt.subplots(figsize=(4, 3.5), dpi=200)
        >>> ax, cax = midia_plane(DI, DAI, alpha=0.5, ax=ax)
        >>> plt.tight_layout()
        >>> plt.show()

        >>> fig, ax = plt.subplots(figsize=(4, 3.5), dpi=200)
        >>> ax = midia_plane(DI, DAI, alpha=0.5, fill=False, ax=ax)
        >>> plt.tight_layout()
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    if not 0 <= alpha <= 1:
        raise ValueError(f'alpha should be in [0, 1], but is {alpha}.')

    DI = np.asarray(DI, dtype=float)
    DAI = np.asarray(DAI, dtype=float)
    if labels is None:
        labels = [f'$A_{{{i + 1}}}$' for i in range(len(DI))]

    x0, x1 = min(0.0, DI.min()), max(1.0, DI.max())
    y0, y1 = min(0.0, DAI.min()), max(1.0, DAI.max())
    xpad, ypad = (x1 - x0) * 0.05, (y1 - y0) * 0.05
    xlim, ylim = (x0 - xpad, x1 + xpad), (y0 - ypad, y1 + ypad)

    x, y = np.meshgrid(np.linspace(*xlim, num), np.linspace(*ylim, num))
    z = alpha * x + (1 - alpha) * y
    zmin, zmax = alpha * x0 + (1 - alpha) * y0, alpha * x1 + (1 - alpha) * y1

    # Alternatives in axes coordinates
    ux = (DI - xlim[0]) / (xlim[1] - xlim[0])
    uy = (DAI - ylim[0]) / (ylim[1] - ylim[0])

    cax = None
    if fill:
        if levels is None:
            levels = np.linspace(zmin, zmax, 11)
        contourf_kwargs = dict(levels=levels, extend='both') | contourf_kwargs
        contourf = ax.contourf(x, y, z, cmap=cmap, **contourf_kwargs)
        if colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)
            plt.colorbar(contourf, cax=cax, extendfrac=0)
            cax.set_yticks(np.linspace(zmin, zmax, 5))
            cax.set_ylim(zmin, zmax)
            cax.set_ylabel('$D(\\alpha)$')
    else:
        if levels is None:
            levels = np.linspace(zmin, zmax, 6)[1:-1]
        contour_kwargs = dict(levels=levels, colors='k', linestyles='--', linewidths=1) | contour_kwargs
        contour = ax.contour(x, y, z, **contour_kwargs)

        # Labels of the lines are put where they are the furthest from the alternatives
        manual = []
        mx, my = (x1 - x0) * 0.08, (y1 - y0) * 0.08
        for level in contour.levels:
            if alpha < 1:
                lx = np.linspace(x0 + mx, x1 - mx, 200)
                ly = (level - alpha * lx) / (1 - alpha)
            else:
                ly = np.linspace(y0 + my, y1 - my, 200)
                lx = np.full_like(ly, level)
            inside = (lx >= x0 + mx) & (lx <= x1 - mx) & (ly >= y0 + my) & (ly <= y1 - my)
            if not inside.any():
                continue
            lx, ly = lx[inside], ly[inside]
            vx = (lx - xlim[0]) / (xlim[1] - xlim[0])
            vy = (ly - ylim[0]) / (ylim[1] - ylim[0])
            dist = np.min(np.hypot(vx[:, None] - ux[None], vy[:, None] - uy[None]), axis=1)
            k = np.argmax(dist)
            manual.append((lx[k], ly[k]))
        if manual:
            ax.clabel(contour, fontsize=8, fmt='%.2f', manual=manual)

    scatter_kwargs = dict(marker='*', color='orange', edgecolor='k', linewidth=0.5, s=120,
                          zorder=3) | scatter_kwargs
    ax.scatter(DI, DAI, **scatter_kwargs)

    text_kwargs = dict(fontsize=9, zorder=4) | text_kwargs
    bbox = ax.get_window_extent()
    scale = ax.figure.dpi / 72 * text_kwargs['fontsize']
    sizes = []
    for label in labels:
        chars = len(re.sub(r'[${}_\\]', '', str(label)))
        sizes.append((0.6 * chars * scale / bbox.width, 1.3 * scale / bbox.height))
    for (bx, by), label in zip(_label_positions(ux, uy, sizes), labels):
        ax.text(bx, by, label, ha='left', va='bottom', transform=ax.transAxes, **text_kwargs)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(np.linspace(x0, x1, 5))
    ax.set_yticks(np.linspace(y0, y1, 5))
    ax.set_xlabel('$DI$')
    ax.set_ylabel('$DAI$')
    ax.grid(alpha=0.5, linestyle='--')
    ax.set_axisbelow(True)

    if cax is not None:
        return ax, cax
    return ax
