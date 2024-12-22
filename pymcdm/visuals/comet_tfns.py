# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def comet_tfns(comet,
               criterion_index,
               criterion_name=None,
               fill=True,
               colors=None,
               plot_kwargs=None,
               fill_kwargs=None,
               ax=None
               ):
    """ Function to draw TFNs used in the COMET method.

        Parameters
        ----------
            comet : COMET
                Object of the COMET method.

            criterion_index : int
                TFNs will be drawn for the criterion with this indes.

            criterion_name : str or None
                Name of the criterion. Will be used as title of the ax.
                Default is None.

            fill : bool
                If TFNs should be filled or not. Default is True.

            colors : Iterable or None
                List or tuple of acceptable for matplolib colors. If the list
                is smaller than number of rankings, then it will cycled.
                Default is None.

            plot_kwargs : dict
                Keyword arguments to pass into plot function (for TFNs).
                Default is None.

            fill_kwargs : dict
                Keyword arguments to pass into fill_between function.
                Default is None.

            ax : Axes or None
                Axes object to draw on. Default is None.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> from pymcdm.methods import COMET
            >>> cvalues = [[100, 150, 180], [400, 900, 3000],]
            >>> comet = COMET(cvalues, rate_function=COMET.topsis_rate_function(np.ones(2) / 2, [1, -1]))
            >>> fig, axes = plt.subplots(2, 1, figsize=(5, 4), dpi=200)
            >>> for i in range(2):
            ...     comet_tfns(comet,
            ...                criterion_index=i,
            ...                ax=axes[i])
            ...
            >>> plt.tight_layout()
            >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    if criterion_name is None:
        criterion_name = f'$C_{{{criterion_index + 1}}}$'

    if plot_kwargs is None:
        plot_kwargs = dict()

    if fill_kwargs is None:
        fill_kwargs = dict(
            alpha=0.5
        )

    tfns = comet.tfns[criterion_index]
    cvalues = comet.cvalues[criterion_index]

    x = np.linspace(cvalues[0], cvalues[-1], 512)
    x = np.hstack((cvalues[0], x, cvalues[-1]))
    for i, tfn in enumerate(tfns):
        if colors is not None:
            plot_kwargs['color'] = colors[i % len(colors)]
            fill_kwargs['color'] = colors[i % len(colors)]
        y = tfn(x)
        y[[0, -1]] = 0
        ax.plot(x, y, **plot_kwargs)
        if fill:
            ax.fill_between(x, y, 0, **fill_kwargs)

    ax.set_title(criterion_name)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$\\mu(x)$')

    ax.grid(linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    return ax
