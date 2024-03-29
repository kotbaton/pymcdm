import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from .comet_3d_plot import comet_3d_plot

def comet_3d_esp_plot(comet,
                   esps,
                   alternatives=None,
                   cvalues=None,
                   scatter_kwargs=dict(),
                   text_kwargs=dict(),
                   offset_value = 0.06,
                   ax=None):
    """ Visualize the COMET preference function for the 3D case using provided ESPs.

        Parameters
        ----------
            comet : pymcdm.methods.COMET
                Identified COMET method.

            esps : ndarray
                Numpy 2d matrix which defines chosed Expected Solution Points.
                Each row should define one ESP, number of the colums should be
                equal to the number of criteria.

            alternatives : ndarray
                Each alternative should be represented by one row with same
                number of columns as esps.
            
            cvalues : ndarray or None
                If necessary, alternatives also can be visualized.
                Each alternative should be represented by one row with same
                number of columns as esps.

            scatter_kwargs : dict
                kwargs passed to scatter function which draws ESP points.

            text_kwargs : dict
                kwargs passed to text function which draws lables for ESPs.

            offset_value : float, default=0.06
                Value used as multiplier for text annotation offset in all axes

            ax : Axis or None
                Matplotlib Axis to draw on. If None, current axis is used.

        Returns
        -------
            ax : Axis
                Matplotlib Axis on which plot was drawn.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> import pymcdm as pm
            >>> # Define criteria bounds for the decision problem
            >>> bounds = np.array([[0, 1]] * 3, dtype=float)
            >>> # Define the Expected Solution Point (or Points) for this problem
            >>> esps = np.array([[0.4, 0.4, 0.5]])
            >>> # Create the expert function using ESPExpert class
            >>> expert = pm.methods.comet_tools.ESPExpert(esps,
            ...                                           bounds,
            ...                                           cvalues_psi=0.2)
            >>> # Generate ESP-guided cvalues based on provided ESP and psi
            >>> cvalues = expert.make_cvalues()
            >>> # Create and identify COMET model
            >>> comet = pm.methods.COMET(cvalues, expert)
            >>> # Create a visualization of the characteriscic values,
            >>> # ESP and preference function
            >>> fig, ax = plt.subplots(figsize=(5, 5), dpi=150, tight_layout=True, subplot_kw=dict(projection='3d'))
            >>> ax pm.visuals.comet_3d_esp_plot(comet, esps, cvalues=cvalues, ax=ax)
            >>> plt.tight_layout()
            >>> plt.show()
    """

    if ax is None:
        ax = plt.axes(projection='3d')

    if cvalues is None:
        if alternatives is None:
            raise ValueError(
                f'You should provide alternatives to generate Characteristic Objects values.'
            )
        cvalues = comet.make_cvalues(alternatives)

        
    ax = comet_3d_plot(cvalues, alternatives, ax=ax)

    scatter_kwargs = dict(c='orange', marker='*', s=120, edgecolor='black') | scatter_kwargs
    ax.scatter(esps[:, 0], esps[:, 1], esps[:, 2], **scatter_kwargs)

    text_kwargs = dict(color='orange', fontweight='bold', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
    for k, (x, y, z) in enumerate(zip(esps[:, 0], esps[:, 1], esps[:, 2]), 1):
        ax.text(x + (comet.cvalues[0][-1] - comet.cvalues[0][0]) * offset_value,
                y + (comet.cvalues[1][-1] - comet.cvalues[1][0]) * offset_value, z + (comet.cvalues[2][-1] - comet.cvalues[2][0]) * offset_value, f'$ESP_{{{k}}}$', **text_kwargs)

    return ax
