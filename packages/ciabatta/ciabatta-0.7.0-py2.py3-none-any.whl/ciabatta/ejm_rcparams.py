"""
Constants and functions for making matplotlib prettier.
"""
from __future__ import (division, absolute_import,
                        print_function)

import numpy as np
import matplotlib as mpl
from matplotlib import cm as mpl_cm
import matplotlib.dates as mdates
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pgf import FigureCanvasPgf
from matplotlib.backend_bases import register_backend

golden_ratio = (np.sqrt(5) - 1.0) / 2.0
almost_black = '#262626'
almost_white = '#FEFEFA'

set3_map = mpl_cm.Set3
set3 = set3_map.colors


def set_pretty_plots(use_latex=False, use_pgf=False, use_microtype=True):
    if use_latex:
        if use_pgf:
            register_backend('pdf', FigureCanvasPgf, 'pgf')
            rcParams['pgf.texsystem'] = 'pdflatex'
        preamble = [r'\usepackage{siunitx}',
                    r'\usepackage{lmodern}',
                    r'\usepackage{subdepth}',
                    ]
        if use_microtype:
            preamble.append(
                r'\usepackage[protrusion = true, expansion = true]{microtype}'
            )
        rcParams['text.usetex'] = True
        rcParams['text.latex.preamble'] = preamble
        rcParams['pgf.preamble'] = preamble
        rcParams['text.latex.unicode'] = True
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['STIXGeneral']

    rcParams['axes.prop_cycle'] = mpl.cycler(color=set3)
    rcParams['axes.edgecolor'] = almost_black
    rcParams['axes.labelcolor'] = almost_black
    rcParams['text.color'] = almost_black
    rcParams['grid.color'] = almost_black
    rcParams['legend.scatterpoints'] = 1
    rcParams['legend.fancybox'] = True
    rcParams['legend.frameon'] = False
    rcParams['legend.framealpha'] = 0.0
    rcParams['lines.linewidth'] = 2.0
    # rcParams['image.aspect'] = 'equal'
    # rcParams['image.origin'] = 'lower'
    rcParams['image.interpolation'] = 'nearest'


def increase_font_sizes(scale=1.0):
    base_big = 24
    big = base_big * scale
    small = 0.75 * big

    def get_nearest_int(n):
        return int(round(n))

    big = get_nearest_int(big)
    small = get_nearest_int(small)
    rcParams['figure.titlesize'] = big
    rcParams['axes.titlesize'] = big
    rcParams['axes.labelsize'] = big
    rcParams['xtick.labelsize'] = small
    rcParams['ytick.labelsize'] = small
    rcParams['legend.fontsize'] = big


def prettify_axis(ax):
    for spine in ax.spines:
        ax.spines[spine].set_linewidth(0.5)
        ax.spines[spine].set_color(almost_black)
        ax.xaxis.label.set_color(almost_black)
        ax.yaxis.label.set_color(almost_black)
        ax.title.set_color(almost_black)
        [i.set_color(almost_black) for i in ax.get_xticklabels()]
        ax.tick_params(axis='both', colors=almost_black)

        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')


def prettify_axes(*axs):
    for ax in axs:
        prettify_axis(ax)


def get_figsize(width=512, factor=0.6, ratio=golden_ratio):
    """Get width using \showthe\textwidth in latex file, then see the tex
    compile log.
    """
    fig_width_pt = width * factor
    inches_per_pt = 1.0 / 72.27
    fig_width_in = fig_width_pt * inches_per_pt  # figure width in inches
    fig_height_in = fig_width_in * ratio   # figure height in inches
    figsize = [fig_width_in, fig_height_in]  # fig dims as a list
    return figsize


def shifted_cmap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False),
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap


def norm_to_colour(x):
    c = x - float(x.min())
    c /= float(x.max())
    c *= 255.0
    return c


def make_x_axis_datey(ax, interval=1, is_daily=False):
    date_formatter = mdates.DateFormatter('%Y-%m-%d')
    Locator = mdates.DayLocator if is_daily else mdates.MonthLocator
    locator = Locator(interval=interval)
    ax.tick_params(axis='x', which='major', pad=15)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(locator)
    ax.format_xdata = date_formatter
    ax.xaxis.set_major_formatter(date_formatter)


def get_new_pretty_axis_set(**fig_options):
    fig = plt.figure(**fig_options)
    ax = fig.gca()
    prettify_axes(ax)
    return fig, ax


def show_or_save(fig, file_name=None, debug=True):
    if debug:
        plt.show()
    else:
        # fig.savefig(file_name, bbox_inches='tight', transparent=True)
        fig.savefig(file_name, bbox_inches='tight')


def add_below_legend(ax, bbox_to_anchor=(0.5, -0.1), ncol=10,
                     *args, **kwargs):
    ax.legend(loc='upper center', bbox_to_anchor=bbox_to_anchor, ncol=ncol,
              *args, **kwargs)
