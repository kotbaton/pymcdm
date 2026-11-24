# Copyright (c) 2026 Bartłomiej Kizielewicz

from fractions import Fraction

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def _format_comparison(value, fractions):
    """ Value of a pairwise comparison, as a fraction 1/k for the reciprocals of the Saaty scale if possible. """
    if fractions and 0 < value < 1:
        fraction = Fraction(value).limit_denominator(9)
        if np.isclose(float(fraction), value) and fraction.numerator == 1:
            return f'1/{fraction.denominator}'
    if np.isclose(value, round(value)):
        return f'{round(value):d}'
    return f'{value:.2f}'


def pairwise_matrix(matrix,
                    labels=None,
                    labels_rotation=0,
                    labeltop=False,
                    cmap='Greens',
                    fractions=True,
                    adapt_text_colors=('k', 'w'),
                    colorbar=False,
                    show_axis=True,
                    show_grid=False,
                    grid_kwargs=dict(),
                    text_kwargs=dict(),
                    ax=None):
    """ Visualise a matrix of pairwise comparisons of criteria, e.g. of AHP, as a heatmap. The cells are coloured
        by the logarithm of the comparisons, so that a comparison and its reciprocal are equally far from 1, and
        the reciprocals of the Saaty scale are written as fractions (1/3, 1/5, ...).

        Parameters
        ----------
            matrix : ndarray
                Square matrix of positive pairwise comparisons, a_ij is the importance of criterion i over j.

            labels : list or None
                Labels of the criteria. If None, labels C_1, C_2, ... are used.

            labels_rotation : float
                Rotation of the labels of the columns. Default is 0.

            labeltop : bool
                Put the labels of the columns on the top of the heatmap. Default is False.

            cmap : str or Colormap
                Colormap of the heatmap. Default is 'Greens'.

            fractions : bool
                Write values below 1 as fractions 1/k if they are reciprocals of integers up to 9. Default is True.

            adapt_text_colors : tuple or None
                Colors of the text on light and dark cells. If None, all texts are black. Default is ('k', 'w').

            colorbar : bool
                Add colorbar with ln(a_ij) on the right side of the axis. Default is False.

            show_axis : bool
                Show the frame of the heatmap. Default is True.

            show_grid : bool
                Separate the cells with lines. Default is False.

            grid_kwargs : dict
                Keyword arguments to pass into the grid function (if show_grid is True).

            text_kwargs : dict
                Keyword arguments to pass into the text function which draws the values.

            ax : Axes or None
                Axes object to draw on. If None current Axes object will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

            cax : Axes
                Only if colorbar=True.
                Axes object on which colorbar were drawn.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.weights.subjective import AHP
        >>> from pymcdm.visuals import pairwise_matrix
        >>> matrix = [[1, 3, 7, 5], [1/3, 1, 5, 3], [1/7, 1/5, 1, 1/3], [1/5, 1/3, 3, 1]]
        >>> ahp = AHP(matrix=matrix)
        >>> fig, ax = plt.subplots(figsize=(4, 3.5), dpi=150)
        >>> ax = pairwise_matrix(ahp.matrix, ax=ax)
        >>> ax.set_title(f'CR = {ahp.get_cr():.3f}')  # doctest: +ELLIPSIS
        Text(...)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError('The matrix of pairwise comparisons should be square.')
    if np.any(matrix <= 0):
        raise ValueError('All pairwise comparisons should be positive.')

    n = matrix.shape[0]
    if labels is None:
        labels = [f'$C_{{{i + 1}}}$' for i in range(n)]

    values = np.log(matrix)
    limit = np.max(np.abs(values)) or 1.0
    im = ax.imshow(values, cmap=cmap, vmin=-limit, vmax=limit)

    text_kwargs = dict(ha='center', va='center', color='k') | text_kwargs
    for i in range(n):
        for j in range(n):
            if adapt_text_colors is not None:
                text_kwargs['color'] = adapt_text_colors[int(values[i, j] > limit / 2)]
            ax.text(j, i, _format_comparison(matrix[i, j], fractions), **text_kwargs)

    ax.set_xticks(np.arange(n), labels=labels)
    ax.set_yticks(np.arange(n), labels=labels)
    if labeltop:
        ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    if labels_rotation:
        plt.setp(ax.get_xticklabels(), rotation=labels_rotation,
                 ha='left' if labeltop else 'right', rotation_mode='anchor')
    if not show_axis:
        ax.spines[:].set_visible(False)
    if show_grid:
        grid_kwargs = dict(color='w', linestyle='-', linewidth=3) | grid_kwargs | dict(which='minor')
        ax.set_xticks(np.arange(n + 1) - .5, minor=True)
        ax.set_yticks(np.arange(n + 1) - .5, minor=True)
        ax.grid(**grid_kwargs)
        ax.tick_params(which='minor', bottom=False, left=False)

    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        plt.colorbar(im, cax=cax)
        cax.set_ylabel(r'$\ln a_{ij}$')
        return ax, cax

    return ax
