import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def check_pref(fp1, fm1, fp2, fm2):
    if fp1 == fp2 and fm1 == fm2:
        return 0 # Indifference

    elif (fp1 > fp2 and fm1 < fm2)\
            or (fp1 == fp2 and fm1 < fm2)\
            or (fp1 > fp2 and fm1 == fm2):
        return 1
    else:
        return -1


def promethee_I_graph(Fp, Fm,
                      start_angle=0.5*np.pi,
                      circle_kwargs=dict(),
                      arrow_kwargs=dict(),
                      ax=None):
    """
    Visualise flows of the PROMETHEE I method as a graph.

    Parameters
    ----------
        Fp : ndarray or list
            Positive flow.

        Fm : ndarray or list
            Negative flow.

        start_angle : floar
            Start angle in radians (where to place first alternative).

        circle_kwargs : dict
            Keyword arguments for matploglib's Circle polygon.

        circle_kwargs : dict
            Keyword arguments for matploglib's arrow function.

        ax : Axes
            Axes object to draw on. If None current Axes object will be used.

    Examples
    --------
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.visuals import promethee_I_graph
        >>> N = 7
        >>> Fp = np.random.rand(N)
        >>> Fm = np.random.rand(N)
        >>> promethee_I_graph(Fp, Fm)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')
    ax.set_aspect('equal')

    theta= - 2 * np.pi / len(Fp)

    x = np.cos(theta * np.arange(len(Fp)) + start_angle)
    y = np.sin(theta * np.arange(len(Fp)) + start_angle)

    circle_kwargs = dict(
        radius=0.12,
        edgecolor='k',
        alpha=0.4,
    ) | circle_kwargs
    # ax.scatter(x, y, **scatter_kwargs)

    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.text(xi, yi, f'$A_{{{i + 1}}}$', ha='center', va='center')
        c = Circle((xi, yi), **circle_kwargs)
        ax.add_patch(c)

    arrow_kwargs = dict(
        length_includes_head=True,
        head_starts_at_zero=False,
        head_width=0.05,
        facecolor='k'
    ) | arrow_kwargs
    for i in range(len(Fp)):
        for j in range(len(Fp)):
            if check_pref(Fp[i], Fm[i], Fp[j], Fm[j]) == 1:
                dx = x[j] - x[i]
                dy = y[j] - y[i]

                alpha = np.arctan2(dy, dx)

                ddx = np.cos(alpha) * circle_kwargs['radius']
                ddy = np.sin(alpha) * circle_kwargs['radius']

                ax.arrow(x[i] + ddx, y[i] + ddy,
                         dx - 2*ddx, dy - 2*ddy, **arrow_kwargs)

    plt.tight_layout()
