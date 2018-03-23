"""This module provides examples of creating IAA type-1 fuzzy sets.

The IAA starts as an empty fuzzy set and is populated with intervals.
The membership of any value is given by the percentage of its occurences
within all of the given intervals.

generate_fuzzy_sets.generate_iaa_t1_fuzzy_set can be used to automatically
create a type-1 fuzzy set from a list of intervals.

A type-2 fuzzy set is created by passing multiple lists of intervals. Each
list is used to create a type-1 fuzzy set, and each resulting set is
aggregated into the final type-2 fuzzy set.
"""

import numpy as np
from decimal import Decimal
from collections import defaultdict

from fuzzycreator.measures import similarity_t1
from fuzzycreator.measures import distance_t1
from fuzzycreator import generate_fuzzy_sets
from fuzzycreator import global_settings as gs
from fuzzycreator import visualisations
from fuzzycreator import visualisations_3d

gs.global_uod = [0, 15]
gs.global_x_disc = 1001
gs.global_zlevel_disc = 3
gs.type_2_3d_colour_scheme = gs.GREYSCALE
gs.normalise_generated_sets = True


def generate_data(mean, std_dev=1):
    """Generate normally distributed interval data around the given mean."""
    d1 = list(np.random.normal(mean, std_dev, 100))
    d2 = list(np.random.normal(mean, std_dev, 100))
    d1 = [round(i, 1) for i in d1]
    d2 = [round(i, 1) for i in d2]
    return [(min(d1[i], d2[i]), max(d1[i], d2[i])) for i in range(100)]


def create_fuzzy_set_from_data():
    """Plot fuzzy sets from generated data."""
    mean = np.random.random_integers(0, 10)
    fs = generate_fuzzy_sets.generate_iaa_t1_fuzzy_set(generate_data(mean))
    fs.plot_set()


def create_t2_fuzzy_set_from_data():
    """Plot type-2 fuzzy sets from generated data.

    The data is split into three subsets.
    Each subset is constructed into a type-1 fuzzy set.
    The three type-1 sets are then aggregated into a type-2 fuzzy set.
    """
    mean = np.random.random_integers(0, 10)
    data = [generate_data(mean, 1),
            generate_data(mean, 0.5),
            generate_data(mean, 0.25)]
    print '..Building type-2 fuzzy set'
    fs = generate_fuzzy_sets.generate_iaa_t2_fuzzy_set(data)
    print '..Plotting 3-dimensional model'
    fs.plot_set_3d()
    print '..Plotting 2-dimensional model'
    fs.plot_set()


if __name__ == '__main__':
    print 'Type-1 example'
    create_fuzzy_set_from_data()
    print 'Type-2 example'
    create_t2_fuzzy_set_from_data()
