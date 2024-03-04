# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def comet_3d_plot(cvalues,
                  alternatives=None,
                  alternatives_labels=False,
                  text_kwargs = dict(),
                  scatter_kwargs = dict(),
                  plot_kwargs=dict(),
                  ax=None):
    """ Visualisation of characteristic objects for three criterion.

        Parameters
        ----------
            cvalues : ndarray or Iterable
                Characteristic values for each criterion. Each row is a vector of characterictic objects for one criterion.

            alternatives : ndarray or None
                Alternatives to draw. Alternatives are in rows and criteria are in columns.

            text_kwargs : dict
                Keyword arguments to pass into text (annotate) function.

            scatter_kwargs : dict
                Keyword arguments to pass into scatter function.

            plot_kwargs : dict
                Keyword arguments to pass into plot function.

            ax : Axes
                Axes object to draw on.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> from pymcdm.visuals import comet_3d_plot
            >>> cvalues = np.array([[0, 0.5, 1],
            ...                    [2, 2.5, 3],
            ...                    [4, 5]])
            >>> a = np.array([[0.3, 2.3, 4.5],
            ...              [0.2, 2.8, 4.3],
            ...              [0.2, 2.9,4.6],
            ...              [0.3, 2.1, 4.7],
            ...              [0.3, 2.2, 4.1],
            ...              [0.5, 2.25, 4.9]])
            >>> comet_3d_plot(cvalues, a)
            >>> plt.show()
    """

    if len(cvalues) != 3:
        raise ValueError(
            f'You should provide at least 3 criteria.'
        )

    for i, cv in enumerate(cvalues):
        if len(cv) < 2:
            raise ValueError(
                f'You should provide minimum 2 characteristic value for each criterion. Check criterion with index {i}.'
            )
        # Check if sorted
        if any(cv[i] >= cv[i + 1] for i in range(len(cv) - 1)):
            raise ValueError(
                f'Characteristic values must be sorted in ascending order and does not contain repeated elements. '
                f'Check criterion with index {i}.'
            )

    if ax is None:
        ax = plt.axes(projection='3d')

    plot_kwargs = dict(
        marker='x',
        linestyle='-',
        color='k',
        linewidth=0.5,
        markersize=3,
        zorder=1
    ) | plot_kwargs

    for cvar in cvalues[0]:
        for cvar2 in cvalues[1]:
            ax.plot(len(cvalues[2]) * [cvar], len(cvalues[2]) * [cvar2], cvalues[2], **plot_kwargs)

    for cvar in cvalues[0]:
        for cvar2 in cvalues[2]:
            ax.plot(len(cvalues[1]) * [cvar], cvalues[1], len(cvalues[1]) * [cvar2], **plot_kwargs)

    for cvar in cvalues[1]:
        for cvar2 in cvalues[2]:
            ax.plot(cvalues[0], len(cvalues[0]) * [cvar], len(cvalues[0]) * [cvar2], **plot_kwargs)

    scatter_kwargs = dict(
        marker='*',
        color='green',
        s=40,
        zorder=2
    ) | scatter_kwargs

    if alternatives is not None:
        ax.scatter3D(alternatives[:, 0], alternatives[:, 1], alternatives[:, 2], **scatter_kwargs)

    if alternatives_labels:
        labels = ['$A_{' + str(i) + '}$' for i in range(1, alternatives.shape[0] + 1)]

        text_kwargs = dict(
            color='green',
            zorder=2
        ) | text_kwargs

        for i in range(alternatives.shape[0]):
            ax.text(alternatives[i, 0], alternatives[i, 1], alternatives[i, 2], labels[i],
                    **text_kwargs)

    ax.set_xlabel('$C_{1}$')
    ax.set_ylabel('$C_{2}$')
    ax.set_zlabel('$C_{3}$')

    ax.view_init(20, 30)

    ax.grid()

    axes = [ax.xaxis, ax.yaxis, ax.zaxis]

    for axis in axes:
        axis.pane.fill = False
        axis._axinfo["grid"]['linestyle'] = "--"

    ax.set_facecolor('white')

    return ax
