"""This module provides examples of coding with interval type-2 fuzzy sets."""

from decimal import Decimal

from fuzzycreator.membership_functions.triangular import Triangular
from fuzzycreator.membership_functions.trapezoidal import Trapezoidal
from fuzzycreator.membership_functions.gaussian import Gaussian
from fuzzycreator.fuzzy_sets.interval_t2_fuzzy_set import IntervalT2FuzzySet
from fuzzycreator.measures import similarity_it2
from fuzzycreator.measures import distance_it2
from fuzzycreator import global_settings as gs
from fuzzycreator import visualisations


gs.global_uod = (0, 20)
gs.global_x_disc = 201
# The upper and lower membership functions may be given in any order
A = IntervalT2FuzzySet(Triangular(0, 2, 4), Triangular(1, 2, 3, 0.8))
B = IntervalT2FuzzySet(Trapezoidal(3, 5, 6, 8, 0.8), Trapezoidal(2, 4, 7, 9))
C = IntervalT2FuzzySet(Gaussian(13, 1), Gaussian(13, 0.5, 0.8))
D = IntervalT2FuzzySet(Gaussian(15, 1), Gaussian(16, 1))


def calculations():
    """Demonstrate basic calculations on fuzzy sets."""
    print 'Membership of x=0.5 in A:\n\t',
    print A.calculate_membership(Decimal('0.5'))
    print 'Alpha-cut the UMF of A at alpha=0.5\n\t',
    print A.calculate_alpha_cut_upper(Decimal('0.5'))
    print 'Alpha-cut the LMF of A at alpha=0.5\n\t',
    print A.calculate_alpha_cut_lower(Decimal('0.5'))
    print 'Type reduced set of A:\n\t',
    print A.calculate_centre_of_sets()
    print 'Centre of type reduced set of A:\n\t',
    print A.calculate_overall_centre_of_sets()


def measuring_similarity():
    """Demonstrate measuring similarity."""
    print 's(A,B) =', similarity_it2.jaccard(A, B)
    print 's(C,D) =', similarity_it2.jaccard(C, D)


def measuring_distance():
    """Demonstrate measuring distance."""
    print 'd(A,B) =', distance_it2.mcculloch(A, B)
    print 'd(C,D) =', distance_it2.mcculloch(C, D)


if __name__ == '__main__':
    calculations()
    measuring_similarity()
    measuring_distance()
    visualisations.plot_sets((A, B, C, D))
