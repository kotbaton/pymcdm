# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def correlation_heatmap(corr_matrix,
                        labels=None,
                        labels_rotation=45,
                        labeltop=False,
                        float_fmt='%0.2f',
                        cmap='Greens',
                        adapt_text_colors=None,
                        adapt_text_threshold=None,
                        colorbar=False,
                        show_axis=True,
                        show_grid=False,
                        grid_kwargs=dict(),
                        text_kwargs=dict(),
                        ax=None):
    """ Function for visualisation correlation matrix as a color heatmap.

        Parameters
        ----------
            corr_matrix : ndarray
                Square matrix of correlation values. For example could be generated with function pymcdm.correlation.correlation_matrix.

            labels : Iterable or None
                Labels for rankings (will be displayed as a xticklabels and yticklabels). Default is None.

            labels_rotation : float
                Angle for label rotation. In some cases labels on the X axis will be overlaps, so rotating them could help. Default is 45.

            labeltop : bool
                If True, put labels from X axis on top of the heatmap. Default is False

            float_fmt : str
                Format of the float values on the plot. Default is '%0.2f'

            cmap : str or Colormap
                Colormap for heatmap. Accepts any colormap which is valid matplotlib colormap. Default is 'Greens'.

            adapt_text_colors : tuple or None
                If None, all text will be in one color. In other case, two elements tuple should be provided. For example, passing tuple ('w', 'k') will be retulted in black text if value for this element is bigger or equal to adapt_text_threshold or 'w' if less. Default is None.

            adapt_text_threshold : float or None
                If adapt_text_colors is not None then this value is used selection of text' text. If None, then average value of corr_matrix is chosen. Default is None.

            colorbar : bool
                Add colorbar on the right side of the axis. Default is False.

            show_axis : bool
                If False, then axis (black square) around plot is disabled. Could be useful if you want to add grid to the heatmap. Default is True.

            show_grid : bool
                If True, then grid is added to the heatmap. Default is False.

            grid_kwargs : dict
                Keyword arguments to pass to the grid function.

            text_kwargs : dict
                Keyword arguments to pass to the text function (for matrix values).

            ax : Axes
                Axes object to draw on.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

            cax : Axes
                Only if colorbar=True.
                Axes object on which colorbar were drawn.
    """
    corr_matrix = np.asarray(corr_matrix)

    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = [f'$R_{{{i + 1}}}$' for i in range(corr_matrix.shape[0])]

    im = ax.imshow(corr_matrix, cmap=cmap)

    text_kwargs = dict(
        ha='center',
        va='center',
        color='k'
    ) | text_kwargs

    if adapt_text_colors is not None:
        if adapt_text_threshold is None:
            adapt_text_threshold = np.mean(corr_matrix)

        for i in range(len(labels)):
            for j in range(len(labels)):
                text_kwargs['color'] = adapt_text_colors[corr_matrix[i, j] >= adapt_text_threshold]
                text = ax.text(j, i, float_fmt % corr_matrix[i, j], **text_kwargs)
    else:
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax.text(j, i, float_fmt % corr_matrix[i, j], **text_kwargs)

    if labeltop:
        ax.tick_params(top=labeltop, bottom=not labeltop,
                       labeltop=labeltop, labelbottom=not labeltop)

    if not show_axis:
        ax.spines[:].set_visible(False)

    if labels_rotation:
        plt.setp(ax.get_xticklabels(), rotation=labels_rotation,
                 ha='left' if labeltop else 'right', rotation_mode='anchor')

    ax.set_xticks(np.arange(len(labels)), labels=labels)
    ax.set_yticks(np.arange(len(labels)), labels=labels)

    if show_grid:
        grid_kwargs = dict(
            color='w',
            linestyle='-',
            linewidth=3
        ) | grid_kwargs | dict(which='minor')

        ax.set_xticks(np.arange(corr_matrix.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(corr_matrix.shape[0]+1)-.5, minor=True)
        ax.grid(**grid_kwargs)
        ax.tick_params(which='minor', bottom=False, left=False)

    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = plt.colorbar(im, cax=cax)
        return ax, cax

    return ax
