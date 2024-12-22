# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap

def mej_plot(mej, grid_width=2, cmap=None, colorbar=False, ax=None):
    """ Draw MEJ extracted from COMET object.

        Parameters
        ----------
            mej : ndarray
                MEJ matrix extracted from COMET object.

            grid_width : float
                Width of the grid lines. Default is 2.

            cmap : str or Colormap
                Colormap used for imshow function, could be any colormap acceptable by matplotlib. If None then Green - Blue - Red custom colormap is used.

            colorbar : bool
                If colorbar should be added to plot. Default is False.

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
        >>> from pymcdm.methods import COMET, TOPSIS
        >>> from pymcdm.visuals import mej_plot
        >>> from pymcdm.methods.comet_tools import MethodExpert
        >>> cvalues = np.array([
        ...     [1, 2],
        ...     [3, 4],
        ... ], dtype='float')
        >>> n = len(cvalues)
        >>> weights = np.ones(n) / n
        >>> types = np.ones(n)
        >>> comet = COMET(cvalues, MethodExpert(TOPSIS(), weights, types))
        >>> mej_plot(comet.get_MEJ(), grid_width=4)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    if cmap is None:
        cmap = ListedColormap(['tab:red', 'tab:blue', 'tab:green'])
    im = ax.imshow(mej, cmap=cmap, aspect='auto')

    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(mej.shape[1]+1)-0.51, minor=True)
    ax.set_yticks(np.arange(mej.shape[0]+1)-0.51, minor=True)

    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    ax.grid(which='minor', color='k', linestyle='-', linewidth=grid_width)
    ax.tick_params(which='minor')

    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=cax)
        cbar.set_ticks([0, 0.5, 1])
        return ax, cax

    return ax
