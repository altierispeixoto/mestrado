"""This module is used to create a discrete type-1 fuzzy set."""

from decimal import Decimal

from .. import global_settings as gs
from ..fuzzy_exceptions import AlphaCutError, ZLevelError
from .. import visualisations


class DiscreteT1FuzzySet():
    """Create a discrete type-1 fuzzy set."""

    def __init__(self, points):
        """Create a discrete type-1 fuzzy set using a dict of x,mu pairs."""
        self.points = points

    def calculate_membership(self, x):
        """Calculate the membership of x within the uod.

        Returns a Decimal value.
        """
        #x = Decimal(str(x))
        try:
            return Decimal(self.points[x]).quantize(gs.DECIMAL_ROUNDING)
        except KeyError:
            return 0

    def calculate_alpha_cut(self, alpha):
        """Calculate the alpha-cut of the function within the uod.

        alpha must be greater than 0 and less than the function height.
        Returns a two-tuple.
        """
        alpha = Decimal(alpha).quantize(gs.DECIMAL_ROUNDING)
        x_values = []
        for x in self.points.keys():
            if self.points[x] >= alpha:
                x_values.append(x)
        if len(x_values) == 0:
            raise AlphaCutError('alpha level', alpha, 'is above max y level.')
        return min(x_values), max(x_values)

    def calculate_centroid(self):
        """Calculate the centroid x-value of the fuzzy set."""
        top = 0
        bottom = 0
        for x in self.points.keys():
            mu = self.points[x]
            top += x * mu
            bottom += mu
        return (top / bottom).quantize(gs.DECIMAL_ROUNDING)

    def plot_set(self, filename=None):
        """Plot a graph of the fuzzy set.

        If filename is None, the plot is displayed.
        If a filename is given, the plot is saved to the given location.
        """
        visualisations.plot_sets((self,), filename)
