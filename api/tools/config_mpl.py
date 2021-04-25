# -*- coding: utf-8 -*-

__doc__ = """
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler


def figsize(
    width: str, fraction: float = 1.0, subplots: tuple[int, int] = (1, 1),
) -> tuple[float, float]:
    r"""Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width : str
        Document width in points, or string of predefined document type.
    fraction : float, optional
        Fraction of the width which you wish the figure to occupy,
        by default 1.
    subplots : tuple[int, int], optional
        The number of rows and columns of subplots, by default (1, 1).

    Returns
    -------
    tuple[float, float]
        Dimensions of figure in inches.

    Raises
    ------
    AssertionError
        If another LaTeX class than scrbook is used.

    Notes
    -----
    The textwidth used in the LaTeX document can be determined by
    typing \the\textwidth anywhere in your LaTeX document.

    References
    ----------
    [1] https://golatex.de/wiki/LaTeX-Einheiten
    [2] https://jwalton.info/Embed-Publication-Matplotlib-Latex/

    """
    if width == "scrbook":
        width_pt = 423.94608
    else:
        raise AssertionError
    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27
    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5 ** 0.5 - 1) / 2
    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])
    return (fig_width_in, fig_height_in)


def set_up_mpl(tex: bool = False) -> None:
    """Set up matplotlib to be coherent with the TUM standard for LaTeX.

    Parameters
    ----------
    tex : bool, optional
        Determine if LaTeX settings in matplotlib should be used,
        by default False.
    
    """
    # print(mpl.rcParams.keys())
    # print(mpl.matplotlib_fname())

    plt.style.use("default")

    params = {
        "text.usetex": tex,
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{siunitx}",
            # r"\usepackage[scaled]{helvet}",
            # r"\renewcommand{\familydefault}{\sfdefault}",
            # r"\usepackage{amsmath}",
        ]
        if tex
        else [],
        "pgf.texsystem": "pdflatex",
        "axes.labelsize": 10,
        "axes.titlesize": 12,
        "lines.linewidth": 2,
        # "axes.titleweight": 700,
        # "text.fontsize": 8,  # was 10
        "legend.fontsize": 8,  # was 10
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        # "figure.figsize": figsize(1, nplots) if tex else [10, 10],  # 0.85 width from latex
        "figure.titleweight": 600,
        "font.size": 10,
        "font.family": "sans-serif",
        "font.weight": 400,  # equals bold, maximum is 900, minimum is 100
        # "backend": "module://Qt5Agg",
        "axes.grid": False,
        "axes.prop_cycle": cycler(
            "color", ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]
        ),
        "grid.linestyle": "--",
        "grid.linewidth": 0.8,
        "image.cmap": "viridis",
        # "savefig.format": "pdf",
    }

    mpl.rcParams.update(params)
