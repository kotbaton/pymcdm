import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.text import TextPath

NAVY = "#1f2f4a"
BLUE = "#2f6f9f"
ORANGE = "#e48400"


def make_pymcdm_logo(
    height_px=300,
    dpi=100,
    with_text=True,
    filename=None
):
    """
    Generate pymcdm logo in arbitrary pixel size.

    Parameters
    ----------
    height_px : int
        Height of the logo in pixels.
    dpi : int
        Figure DPI.
    with_text : bool
        Whether to include the 'pymcdm' text.
    filename : str or None
        If given, saves the logo (extension decides format).
    """

    # --- size logic ---
    height_in = height_px / dpi

    if with_text:
        width_in = 4.0 * height_in
    else:
        width_in = height_in

    fig, ax = plt.subplots(
        figsize=(width_in, height_in),
        dpi=dpi,
        subplot_kw={'aspect': 'equal'}
    )
    fig.patch.set_alpha(0)

    # --- scale factor ---
    S = height_px / 300.0  # 300 px = reference size

    # --- bars ---
    bar_x = [0.0, 0.57, 1.14, 1.7]
    bar_h = [0.4, 0.9, 0.6, 1.2]
    bar_w = 0.30
    dot_r = 0.18
    bar_colors = [NAVY, BLUE, NAVY, ORANGE]
    dot_colors = [NAVY, NAVY, NAVY, ORANGE]

    for x, h, c in zip(bar_x, bar_h, bar_colors):
        ax.add_patch(
            patches.FancyBboxPatch(
                (x, 0),
                bar_w,
                h,
                boxstyle=f"round,pad={0.02*S},rounding_size={0.07*S}",
                linewidth=0,
                facecolor=c
            )
        )

    # --- line + points ---
    line_x = [x + bar_w / 2 for x in bar_x]
    line_y = [h + 0.3 for h in bar_h]

    ax.plot(
        line_x,
        line_y,
        color=NAVY,
        linewidth=7 * S
    )

    point_size = 700 * S**2
    for x, y, dc in zip(line_x, line_y, dot_colors):
        dot = patches.Circle((x, y), dot_r, color=dc, zorder=3)
        ax.add_patch(dot)

    # --- text ---
    if with_text:
        ax.text(
            2.1,
            0.0,
            "pymcdm",
            fontsize=130 * S,
            fontweight="bold",
            fontfamily="DejaVu Sans",
            color=NAVY,
            va="bottom"
        )
        ax.set_xlim(-0.1, 2.05)
    else:
        ax.set_xlim(-0.05, 2.05)

    ax.set_ylim(-0.05, 2.05)
    ax.axis("off")

    if filename:
        plt.savefig(filename, bbox_inches='tight', dpi=dpi)

    return fig, ax


if __name__=='__main__':
    make_pymcdm_logo(height_px=512, with_text=False, filename="logo_icon.svg")
    make_pymcdm_logo(height_px=512, with_text=True, filename="logo_text.svg")

    plt.show()

