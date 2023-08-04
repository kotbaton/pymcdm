import numpy as np
import matplotlib.pyplot as plt

from .comet_contourf import comet_contourf

def comet_esp_plot(comet,
                   esps,
                   bounds,
                   alternatives=None,
                   ax=None):
    """ Visualize the COMET preference function for the 2d case using
        pymcdm.visuals.comet_contourf, as well as provided ESPs.

        Parameters
        ----------
            comet : pymcdm.methods.COMET
                Identified COMET method.

            esps : ndarray
                Numpy 2d matrix which defines chosed Expected Solution Points.
                Each row should define one ESP, number of the colums should be
                equal to the number of criteria.

            bounds : ndarray
                Each row should contain min and max values for each criterion.
                Min and max should be different values!

            alternatives : ndarray or None
                If necessary, alternatives also can be visualized.
                Each alternative should be represented by one row with same
                number of columns as esps.

            ax : Axis or None
                Matplotlib Axis to draw on. If None, current axis is used.

        Returns
        -------
            ax : Axis
                Matplotlib Axis on which plot was drawn.

            cax : Axis
                Matplotlib Axis for the colorbar.

        Examples
        --------
            >>> import numpy as np
            >>> import matplotlib.pyplot as plt
            >>> import pymcdm as pm
            >>> # Define criteria bounds for the decision problem
            >>> bounds = np.array([[0, 1]] * 2, dtype=float)
            >>> # Define the Expected Solution Point (or Points) for this problem
            >>> esps = np.array([[0.4, 0.4]])
            >>> # Create the expert function using ESPExpert class
            >>> expert = pm.comet_tools.ESPExpert(esps,
            ...                                   bounds,
            ...                                   cvalues_psi=0.2)
            >>> # Generate ESP-guided cvalues based on provided ESP and psi
            >>> cvalues = expert.make_cvalues()
            >>> # Create and identify COMET model
            >>> comet = pm.methods.COMET(cvalues, expert)
            >>> # Create a visualization of the characteriscic values,
            >>> # ESP and preference function
            >>> fig, ax = plt.subplots(figsize=(4, 3.5), dpi=200)
            >>> ax, cax = pm.visuals.comet_esp_plot(comet, esps, bounds)
            >>> plt.tight_layout()
            >>> plt.show()
    """
    if alternatives is None:
        alternatives = np.array([[], []]).T

    if ax is None:
        ax = plt.gca()

    ax, cax = comet_contourf(
            comet, alternatives,
            num=200, colorbar=True, ax=ax,
            contourf_kwargs=dict(levels=14, vmin=0, vmax=1))

    ax.scatter(esps[:, 0], esps[:, 1], c='orange', marker='*', s=120)

    for k, (x, y) in enumerate(zip(esps[:, 0], esps[:, 1]), 1):
        ax.text(x + (comet.cvalues[0][-1] - comet.cvalues[0][0]) * 0.03,
                y, f'$ESP_{{{k}}}$',
                color='orange', fontweight='bold', fontsize=12)

    ax.set_xlabel('$C_1$')
    ax.set_ylabel('$C_2$')

    ax.set_xticks(np.linspace(*bounds[0], 5))
    ax.set_yticks(np.linspace(*bounds[1], 5))

    cax.set_yticks(np.linspace(0, 1, 5))
    cax.set_ylim(0, 1)

    return ax, cax
