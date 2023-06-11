# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def comet_2d_plot(cvalues,
                  alternatives,
                  text_kwargs = dict(),
                  scatter_kwargs = dict(),
                  plot_kwargs=dict(),
                  ax=None):
    """ Visualise characteristic objects and alternatives for two criteria.

        Parameters
        ----------
            cvalues : ndarray or Iterable
                Characteristic values for each criterion. Each row is a vector of characterictic objects for one criterion.

            alternatives : ndarray
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
            >>> from pymcdm.visuals import comet_2d_plot
            >>> cvalues = np.array([[1, 2, 3],
            ...                    [4, 4.5, 5]])
            >>> a = np.array([[1, 4.3],
            ...              [1.2, 4.8],
            ...              [2, 4.9],
            ...              [3, 4.1],
            ...              [3, 4.2]])
            >>> comet_2d_plot(cvalues, a)
            >>> plt.show()
    """

    if len(cvalues) != 2:
        raise ValueError(
            f'You should provide minimum 2 characteristic value for each criterion. Check criterion with index {i}.'
        )

    for i, cv in enumerate(cvalues):
        if len(cv) < 2:
            raise ValueError(
                f'You should provide minimum 2 characteristic value for each criterion. Check criterion with index {i}.'
            )
        # Check if sorted
        if any(cv[i] >= cv[i + 1] for i in range(len(cv) - 1)):
            raise ValueError(
                f'Characteristic values must be sorted in ascending order and does not contain repeated elements. Check criterion with index {i}.'
            )

    if ax is None:
        ax = plt.gca()

    alternatives = np.array(alternatives)

    plot_kwargs = dict(
        marker='o',
        linestyle='--',
        color='k',
        zorder=1
    ) | plot_kwargs

    for cval in cvalues[0]:
        ax.plot([cval] * len(cvalues[1]), cvalues[1], **plot_kwargs)

    for cval in cvalues[1]:
        ax.plot(cvalues[0], [cval] * len(cvalues[0]), **plot_kwargs)

    labels = ['$A_{' + str(i) + '}$' for i in range(1, alternatives.shape[0] + 1)]

    scatter_kwargs = dict(
        marker='*',
        color='green',
        s=80,
        zorder=2
    ) | scatter_kwargs

    ax.scatter(alternatives[:, 0], alternatives[:, 1], **scatter_kwargs)

    const_x = 0.1 / (np.max(cvalues[0]) + np.min(cvalues[0]))
    const_y = 0.1 / (np.max(cvalues[1]) + np.min(cvalues[1]))

    text_kwargs = dict(
        color='green',
        zorder=2
    ) | text_kwargs

    for i in range(alternatives.shape[0]):
        ax.annotate(labels[i], (alternatives[i, 0] + const_x, alternatives[i, 1] + const_y), **text_kwargs)

    ax.set_xlabel('$C_1$')
    ax.set_ylabel('$C_2$')

    ax.grid(alpha=0.5, linestyle='--')
    ax.set_axisbelow(True)

    return ax
