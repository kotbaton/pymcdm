# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def simos_cards(r, w_c,
                weights=None,
                labels=None,
                cmap='Greens',
                card_kwargs=dict(),
                text_kwargs=dict(),
                ax=None):
    """ Visualise the cards of the Simos procedure (SIMOS and SRF): the criteria from the least to the most
        important one, with criteria of the same importance stacked on each other and white cards between the
        positions. Optionally, the weights of the criteria are written under the positions.

        Parameters
        ----------
            r : list
                Criteria indices from the least to the most important one, with inner lists for ties, as in
                :class:`pymcdm.weights.subjective.SIMOS`.

            w_c : list or ndarray
                Number of white cards between consecutive positions.

            weights : ndarray or None
                Weights of the criteria, written (in percent) under the positions. If None, no weights are
                written.

            labels : list or None
                Labels of the criteria. If None, labels C_1, C_2, ... are used.

            cmap : str or Colormap
                Colormap of the cards: the more important the position, the darker the card. Default is 'Greens'.

            card_kwargs : dict
                Keyword arguments to pass into the FancyBboxPatch which draws the cards.

            text_kwargs : dict
                Keyword arguments to pass into the text function which draws the labels of the criteria.

            ax : Axes or None
                Axes object to draw on. If None current Axes object will be used.

        Returns
        -------
            ax : Axes
                Axes object on which plot were drawn.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from pymcdm.weights.subjective import SRF
        >>> from pymcdm.visuals import simos_cards
        >>> r = [[2, 6], [3], [1, 5], [4], [0]]
        >>> w_c = [0, 1, 0, 2]
        >>> weights = SRF(r=r, w_c=w_c, z=6)()
        >>> fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
        >>> ax = simos_cards(r, w_c, weights=weights, ax=ax)
        >>> plt.show()
    """
    if ax is None:
        ax = plt.gca()

    groups = [list(g) if isinstance(g, (list, tuple, np.ndarray)) else [g] for g in r]
    w_c = np.asarray(w_c)
    if len(w_c) != len(groups) - 1:
        raise ValueError(f'w_c should have {len(groups) - 1} values (number of positions - 1).')
    if np.any(w_c < 0) or np.any(w_c != np.round(w_c)):
        raise ValueError('Numbers of white cards should be non-negative integers.')

    n = max(c for g in groups for c in g) + 1
    if labels is None:
        labels = [f'$C_{{{j + 1}}}$' for j in range(n)]
    # Colors of the positions from the least to the most important one
    colormap = plt.get_cmap(cmap)
    shades = colormap(np.linspace(0.25, 0.9, len(groups)))

    width, height, gap = 0.8, 0.5, 0.15
    card_kwargs = dict(boxstyle='round,pad=0,rounding_size=0.05', linewidth=1, edgecolor='k') | card_kwargs
    text_kwargs = dict(ha='center', va='center', fontsize=10) | text_kwargs

    x = 0.0
    for k, group in enumerate(groups):
        for s, c in enumerate(group):
            y = s * (height + gap)
            shade = shades[k]
            ax.add_patch(FancyBboxPatch((x, y), width, height, **(dict(facecolor=shade) | card_kwargs)))
            # White text on dark cards
            luminance = 0.299 * shade[0] + 0.587 * shade[1] + 0.114 * shade[2]
            ax.text(x + width / 2, y + height / 2, labels[c],
                    **(dict(color='w' if luminance < 0.5 else 'k') | text_kwargs))
        if weights is not None:
            ax.text(x + width / 2, -0.2, f'{100 * weights[group[0]]:.1f}%', ha='center', va='top', fontsize=8)
        x += width + gap
        if k < len(groups) - 1:
            for _ in range(int(w_c[k])):
                ax.add_patch(FancyBboxPatch((x, 0), width, height,
                                            **(card_kwargs | dict(facecolor='w', linestyle='--'))))
                x += width + gap

    end = x - gap
    ax.annotate('', xy=(end, -0.7), xytext=(0, -0.7), arrowprops=dict(arrowstyle='-|>', color='k', lw=1))
    ax.text(0, -0.8, 'Least important', ha='left', va='top', fontsize=8)
    ax.text(end, -0.8, 'Most important', ha='right', va='top', fontsize=8)

    ax.set_xlim(-0.1, end + 0.1)
    ax.set_ylim(-1.15, max(len(g) for g in groups) * (height + gap) + 0.05)
    ax.set_aspect('equal')
    ax.axis('off')

    return ax
