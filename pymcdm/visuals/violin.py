# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def violin(data, labels=None, violin_kwargs=dict(), ax=None):
    """ Draw violin for the data, adding labels and grid.

        Parameters
        ----------
            data : ndarray or list
                Matrix or collection of vectors to build violin's from. If matrix, violins will be drawn for every row.

            labels : Iterable or None
                Tick labels on the X axis (names of the violins).

            violin_kwargs : dict
                Keyword arguments to pass into violinplot function from matploblib.

            ax : Axes or None
                Axes object to draw on. If None, then current axes is used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> from pymcdm.visuals import violin
            >>> data = [np.random.rand(100) for i in range(3)]
            >>> violin(data)
            >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    data = np.array(data)

    ax.violinplot(data.T, **violin_kwargs)
    if labels is None:
        labels = [f'$V_{{{i + 1}}}$' for i in range(len(data))]

    ax.set_xticks(range(1, len(labels) + 1), labels=labels)

    ax.grid(linestyle='--', alpha=0.5)

    return ax
