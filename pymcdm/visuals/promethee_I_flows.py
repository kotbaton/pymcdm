# Copyright (c) 2022 Bartłomiej Kizielewicz
# Copyright (c) 2022 Andrii Shekhovtsov

import numpy as np
import matplotlib.pyplot as plt

def promethee_I_flows(Fp, Fm,
                      colors=None,
                      line_kwargs=dict(),
                      text_kwargs=dict(),
                      ax=None):
    """
        Visualise positive and negative flows for PROMETHEE I method.

        Parameters
        ----------
            Fp : ndarray or list
                Positive flow.

            Fm : ndarray or list
                Negative flow.

            colors : list
                Color of the plotted line. If size of the list is smaller than set of the alternatives then colors starts to cycle.

            line_kwargs : dict
                Keyword arguments to pass into plot functions.

            text_kwargs : dict
                Keyword arguments to pass into text functions.

            ax : Axes or None
                Axes object to draw on. If None current Axes object will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.visuals import promethee_I_flows
        >>> N = 5
        >>> Fp = np.random.rand(N)
        >>> Fm = np.random.rand(N)
        >>> promethee_I_flows(Fp, Fm)
        >>> plt.show()

        >>> fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
        >>> promethee_I_flows(Fp, Fm, ax=ax)
        >>> plt.show()

        >>> fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
        >>> promethee_I_flows(Fp, Fm, colors=['red', 'blue', 'green'], ax=ax)
        >>> plt.show()

        >>> fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
        >>> promethee_I_flows(Fp, Fm, text_kwargs=dict(fontsize=14), ax=ax)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    ax.set_xlim(-0.51, 0.51)
    ax.set_ylim(-0.51, 0.51)
    ax.axis('off')

    ax.plot([0.5, 0.5], [-0.5, 0.5], 'k', linewidth=3)
    ax.plot([-0.5, -0.5], [-0.5, 0.5], 'k', linewidth=3)
    ax.plot([0, 0], [-0.5, 0.5], 'k',
            alpha=0.5, linewidth=2, linestyle='--')

    ax.text(-0.49, 0.5, '$\\Phi$+', **text_kwargs)
    ax.text(-0.51, 0.5, '1.0', ha='right', **text_kwargs)
    ax.text(-0.51, 0.0, '0.5', ha='right', **text_kwargs)
    ax.text(-0.51, -0.5, '0.0', ha='right', **text_kwargs)

    ax.text(0.49, 0.5, '$\\Phi$-', ha='right', **text_kwargs)
    ax.text(0.51, -0.5, '1.0', **text_kwargs)
    ax.text(0.51, 0.0, '0.5', **text_kwargs)
    ax.text(0.51, 0.5, '0.0', **text_kwargs)

    for i in np.arange(-0.5, 0.51, 0.25):
        ax.plot([-0.49, -0.51], [i, i], 'k')
        ax.plot([0.49, 0.51], [i, i], 'k')

    if colors:
        for i, (fp, fm) in enumerate(zip(Fp, Fm)):
            ax.plot([-0.5, 0.5], [-0.5 + fp, 0.5 - fm],
                    linewidth=2, color=colors[i % len(colors)],
                    label=f'$A_{{{i+1}}}$', **line_kwargs)
    else:
        for i, (fp, fm) in enumerate(zip(Fp, Fm)):
            ax.plot([-0.5, 0.5], [-0.5 + fp, 0.5 - fm],
                    linewidth=2, label=f'$A_{{{i+1}}}$', **line_kwargs)

    ax.legend(bbox_to_anchor=(0., 1.05, 1., .105), loc='lower left',
           ncol=5, mode="expand", borderaxespad=0.)

    return ax
