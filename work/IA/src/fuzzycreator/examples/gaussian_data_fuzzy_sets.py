"""This module provides examples of creating polling type-1 fuzzy sets."""

import cPickle as pickle
import numpy as np
from decimal import Decimal
from collections import defaultdict

from fuzzycreator import generate_fuzzy_sets
from fuzzycreator import global_settings as gs
from fuzzycreator import visualisations


gs.global_uod = [-2, 2]
gs.global_x_disc = 1001
gs.normalise_generated_sets = True


def load_distributions(total_sets=3):
    """ Loads the data that is created by the 
        function load_distributions. """
    fsock = open('data/polling_data', "r")
    try:
        distributions = pickle.load(fsock)
    finally:
        fsock.close()
    return [list(distributions[i]) for i in range(total_sets)]


def create_fuzzy_set_from_data():
    """Plot type-1 fuzzy sets generated from data given by load_data()."""
    fuzzy_sets = [generate_fuzzy_sets.generate_gaussian_t1_fuzzy_set(d)
                        for d in load_distributions()]
    visualisations.plot_sets(fuzzy_sets)


def create_t2_fuzzy_set_from_data():
    """Plot type-2 fuzzy sets generated from data given by load_data().

    The data is split into three subsets.
    Each subset is constructed into a type-1 fuzzy set.
    The three type-1 sets are then aggregated into a type-2 fuzzy set.
    """
    data = [load_data(f)[ATTR] for f in FILENAMES]
    # Split the data into artificial subsets which will be type-1 fuzzy sets.
    for i in range(4):
        data[i] = [data[i][:10], data[i][10:20], data[i][20:]]
    fuzzy_sets = [generate_fuzzy_sets.generate_gaussian_t2_fuzzy_set(d)
                  for d in data]
    # visualisations.plot_sets(fuzzy_sets)
    fuzzy_sets[0].plot_set()


if __name__ == '__main__':
    create_fuzzy_set_from_data()
    #create_t2_fuzzy_set_from_data()
