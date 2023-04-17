# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt
from .comet_2d_plot import comet_2d_plot
from mpl_toolkits.axes_grid1 import make_axes_locatable


def comet_contourf(comet,
                   alternatives,
                   num=10,
                   cmap='Greens',
                   colorbar=False,
                   comet_2d_plot_kwargs=dict(),
                   contourf_kwargs=dict(),
                   ax=None):
    """ Visualise characteristic objects and alternatives for two criteria. In addition to that preference surface will be visualised as an contourf.

        Parameters
        ----------
            comet : COMET
                COMET object from `pymcdm.methods`. It will be used to evaluate preference surface and to draw characteristic values of the model.

            alternatives : ndarray
                Alternatives to draw. Alternatives are in rows and criteria are in columns.

            num : int
                Number of points in meshgrid (num argument for linspace function).

            cmap : str or Colormap
                Colormap for heatmap. Accepts any colormap which is valid matplotlib colormap. Default is 'Greens'.

            colorbar : bool
                Add colorbar on the right side of the axis. Default is False.

            comet_2d_plot_kwargs : dict
                Keyword arguments to pass into comet_2d_plot function. See its documentation for more details.

            contourf_kwargs : dict
                Keyword arguments to pass into contourf funtcion.

            ax : Axes
                Axes object to draw on.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

            cax : Axes
                Only if colorbar=True.
                Axes object on which colorbar were drawn.

        Examples
        --------
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.visuals import comet_contourf
        >>> from pymcdm.methods import COMET

        >>> w = np.array([[1, 2, 3],
        ...               [4, 4.5, 5]])

        >>> a = np.array([[1, 4.3],
        ...               [1.2, 4.8],
        ...               [2, 4.9],
        ...               [3, 4.1],
        ...               [3, 4.2],
        ...               [2.5, 4.25]])

        >>> c = COMET(w, rate_function=COMET.topsis_rate_function(np.ones(2)/2, np.ones(2)))
        >>> comet_contourf(c, a, 10)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    alternatives = np.array(alternatives)

    x = np.linspace(comet.cvalues[0][0], comet.cvalues[0][-1], num)
    y = np.linspace(comet.cvalues[1][0], comet.cvalues[1][-1], num)

    x, y = np.meshgrid(x, y)

    grid = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))
    p = comet(grid).reshape(num, num)

    contourf = ax.contourf(x, y, p, cmap=cmap, **contourf_kwargs)
    comet_2d_plot(comet.cvalues, alternatives, **comet_2d_plot_kwargs, ax=ax)

    xpad = (comet.cvalues[0][-1] - comet.cvalues[0][0]) * 0.05
    ax.set_xlim(comet.cvalues[0][0] - xpad, comet.cvalues[0][-1] + xpad)

    ypad = (comet.cvalues[1][-1] - comet.cvalues[1][0]) * 0.05
    ax.set_ylim(comet.cvalues[1][0] - ypad, comet.cvalues[1][-1] + ypad)

    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = plt.colorbar(contourf, cax=cax)
        return ax, cax

    return ax
