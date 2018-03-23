"""This module is used to plot graphs of fuzzy sets."""

from decimal import Decimal
from numpy import linspace
import matplotlib.pyplot as plt

import global_settings as gs


def _plot_type1_set(fs, plot_points, colour_index):
    """Add a type-1 fuzzy set to plt."""
    plt.plot(plot_points,
             [fs.calculate_membership(x) for x in plot_points],
             gs.colours[colour_index],
             linewidth=3)


def _plot_discrete_t1(fs, colour_index):
    """Add a type-1 discrete fuzzy set to plt."""
    for p in fs.points.keys():
        plt.axvline(x=p,
                    ymin=0,
                    ymax=fs.calculate_membership(p),
                    color=gs.colours[colour_index],
                    linewidth=3,
                    alpha=0.5)


def _plot_interval_type2_set(fs, plot_points, colour_index,
                             colour_alpha='0.8'):
    """Add an interval type-2 fuzzy set to plt."""
    Y = [fs.calculate_membership(x) for x in plot_points]
    for i in range(len(Y)):
        Y[i] = (float(Y[i][0]), float(Y[i][1]))
    plt.plot(plot_points,
             [y[0] for y in Y],
             color=gs.colours[colour_index],
             linewidth=0)
    plt.plot(plot_points,
             [y[1] for y in Y],
             color=gs.colours[colour_index],
             linewidth=0)
    plot_points = [float(p) for p in plot_points]
    plt.fill_between(plot_points,
                     [y[0] for y in Y],
                     [y[1] for y in Y],
                     color=gs.colours[colour_index],
                     alpha=colour_alpha)


def _plot_general_type2_set(fs, plot_points, colour_index):
    """Add a general type-2 fuzzy set to plt."""
    for z in fs.zlevel_coords:
        _plot_interval_type2_set(fs.zslice_functions[z], plot_points,
                                 colour_index, str(Decimal('0.8') * z))


def _plot_type2_iaa_sets(fs, plot_points, colour_index):
    """Add a type-2 interval agreement approach set to plt."""
    noughts = [0 for x in plot_points]
    float_plot_points = [float(x) for x in plot_points]
    for mf in fs.membership_functions:
        ys = [float(mf.calculate_membership(x)) for x in plot_points]
        plt.fill_between(float_plot_points, noughts, ys,
                         color=gs.colours[colour_index],
                         alpha=0.5)


def plot_sets(fuzzy_sets, filename=None):
    """Plot the given list of fuzzy sets.

    The fuzzy sets may be of any type.
    Discretisations and axis labels are set in the global_settings module.
    If filename is None, the plot is displayed.
    If a filename is given, the plot is saved to the given location.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    colour_index = 0
    plot_points = gs.get_x_points()
    for fs in fuzzy_sets:
        if (fs.__class__.__name__ == 'FuzzySet' or
                fs.__class__.__name__ == 'PollingT1FuzzySet' or
                fs.__class__.__name__ == 'IAAT1FuzzySet'):
            _plot_type1_set(fs, plot_points, colour_index)
        elif fs.__class__.__name__ == 'DiscreteT1FuzzySet':
            _plot_discrete_t1(fs, colour_index)
        elif fs.__class__.__name__ == 'IntervalT2FuzzySet':
            _plot_interval_type2_set(fs, plot_points, colour_index)
        elif fs.__class__.__name__ == 'GeneralT2FuzzySet':
            _plot_general_type2_set(fs, plot_points, colour_index)
        elif fs.__class__.__name__ == 'T2AggregatedFuzzySet':
            _plot_type2_iaa_sets(fs, plot_points, colour_index)
        else:
            print 'Unknown how to plot', fs.__class__.__name__, 'object'
        colour_index = (colour_index + 1) % len(gs.colours)
    ax.set_ylim(0, 1.01)
    ax.set_xlim(gs.global_uod[0], gs.global_uod[1])
    # set the tick positions to remove them from the top and right
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # change the size of the numbers along the axis
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    plt.yticks(linspace(0, 1, 6))
    # add the labels to the axes
    ax.set_xlabel(gs.xlabel, fontsize=22)
    ax.set_ylabel(gs.type_1_ylabel, fontsize=22)
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    fig.subplots_adjust(left=0.15)
    fig.subplots_adjust(bottom=0.15)
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
