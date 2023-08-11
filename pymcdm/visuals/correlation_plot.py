import numpy as np
import matplotlib.pyplot as plt

def correlation_plot(cors,
                     ylabel='Correlation',
                     ylim=None,
                     labels=None,
                     space_multiplier=0.05,
                     plot_kwargs=dict(),
                     fill_between_kwargs=dict(),
                     ax=None):
    """ Visualize correlation changes for different rankings.

        Parameters
        ----------
            cors : Iterable
                list or ndarray with correlation values.

            ylabel : str
                Name of the Y ax.

            ylim : Iterable or None
                Limits of values for Y ax. Default is None.

            labels : Iterable or None
                Labels which should be displayed as xticks.

            space_multiplier : float
                Values which allows to change distance beteeen correlation
                labels and markers. Default is 0.05.

            plot_kwargs : dict
                Keyword arguments to pass into plot function (line).

            fill_between_kwargs : dict
                Keyword arguments to pass into fill_between
                function (same keywords as an Polygon).

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
        >>> from pymcdm.visuals import correlation_plot
        >>> cors = [0.9, 0.85, 0.95, 0.89, 0.93]
        >>> correlation_plot(cors, ylim=(0.7, 1))
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = [f'$R_{{{i}}}$' for i in range(len(cors))]

    default_plot_kwargs = dict(
            linewidth=1,
            linestyle='--',
            marker='*',
            markersize=8,
            color='green'
            )
    plot_kwargs = default_plot_kwargs | plot_kwargs

    default_fill_between_kwargs = dict(
            color='green',
            alpha=0.2
            )
    fill_between_kwargs = default_fill_between_kwargs | fill_between_kwargs

    ax.plot(range(len(labels)), cors, **plot_kwargs)
    ax.fill_between(range(len(labels)),
                    [np.min(cors) - 0.5] * len(labels), cors,
                    **fill_between_kwargs)

    spacing = (np.max(cors) - np.min(cors)) * space_multiplier
    for i, c in enumerate(cors):
        ax.text(i, c - spacing, f'{c:0.3f}', color='green', ha='center', va='top')

    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.grid(ls='--', alpha=0.5)
    ax.set_axisbelow(True)

    ax.set_xticks(range(len(labels)), labels=labels)

    return ax
