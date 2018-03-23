"""This module is used to create a discrete type-2 fuzzy set."""

from decimal import Decimal
from collections import defaultdict

from .. import global_settings as gs
from ..fuzzy_exceptions import AlphaCutError, ZLevelError


class DiscreteT2FuzzySet():
    """Create a discrete type-2 fuzzy set."""

    def __init__(self, points):
        """Create a discrete type-1 fuzzy set using a dict as {x: {mu: z}}."""
        self.points = points
        # A dict of z:mu pairs for the height of each zslice
        self.zslice_primary_heights = defaultdict(lambda: [0,0])
        for x in self.points:
            for mu in self.points[x]:
                z = self.points[x][mu]
                self.zslice_primary_heights[z][0] = min(
                        self.zslice_primary_heights[z][0], mu)
                self.zslice_primary_heights[z][1] = max(
                        self.zslice_primary_heights[z][1], mu)
        self.zlevel_coords = sorted(self.zslice_primary_heights.keys())

    def validate_zlevel(self, z):
        """Find the closest valid zlevel.

        Checks if the zlevel at z exists. If it exists then return z.
        If not, then return the closest zlevel that encompasses z.
        """
        z = Decimal(z).quantize(gs.DECIMAL_ROUNDING)
        if z in self.zlevel_coords:
            return z
        else:
            points = self.zlevel_coords[:]
            if z > max(points):
                raise ZLevelError('zLevel ' + str(z) +
                                  ' is higher than the greatest zLevel at ' +
                                  str(max(points)))
            points.sort()
            for i in points:
                if i > z:
                    return i

    def calculate_membership(self, x, z):
        """Calculate the primary membership of x at the zlevel z."""
        try:
            y_list = []
            for y in self.points[x].keys():
                if self.points[x][y] >= z:
                    y_list.append(y)
            if len(y_list) == 0:
                return 0, 0
            else:
                return (Decimal(min(y_list)).quantize(gs.DECIMAL_ROUNDING),
                        Decimal(max(y_list)).quantize(gs.DECIMAL_ROUNDING))
        except KeyError:
            return 0, 0

    def calculate_secondary_membership(self, x, mu):
        """Calculate the secondary membership of x at primary membership y."""
        try:
            return self.points[x][mu]
        except KeyError:
            return 0

    def calculate_alpha_cut_lower(self, alpha, z=0):
        """Calculate the alpha-cut of the lower membership function.

        alpha must be greater than 0 and less than the function height.
        Returns a two-tuple.
        """
        alpha = Decimal(alpha).quantize(gs.DECIMAL_ROUNDING)
        x_values = []
        for x in self.points.keys():
            for mu in self.points[x].keys():
                if mu >= alpha and self.points[x][mu] >= z:
                    x_values.append(x)
        if len(x_values) == 0:
            raise AlphaCutError('alpha level', alpha, 'is above max y level.')
        return min(x_values), max(x_values)

    def calculate_alpha_cut_upper(self, alpha, z=0):
        """Calculate the alpha-cut of the lower membership function.

        alpha must be greater than 0 and less than the function height.
        Returns a two-tuple.
        """
        alpha = Decimal(alpha).quantize(gs.DECIMAL_ROUNDING)
        x_values = []
        for x in self.points.keys():
            for mu in self.points[x].keys():
                if mu >= alpha and self.points[x][mu] >= z:
                    x_values.append(x)
        if len(x_values) == 0:
            raise AlphaCutError('alpha level', alpha, 'is above max y level.')
        return min(x_values), max(x_values)
