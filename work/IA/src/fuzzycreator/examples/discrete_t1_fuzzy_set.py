"""This module provides examples of coding with type-1 fuzzy sets."""

from decimal import Decimal

from fuzzycreator.fuzzy_sets.discrete_t1_fuzzy_set import DiscreteT1FuzzySet
from fuzzycreator.measures import similarity_t1
from fuzzycreator.measures import distance_t1
from fuzzycreator import global_settings as gs
from fuzzycreator import visualisations


A_points = {1: Decimal('0.25'), 2: 1, 3: Decimal('0.25')}
B_points = {2: Decimal('0.33'), 3: Decimal('0.66'), 4: Decimal('0.33')}
A = DiscreteT1FuzzySet(A_points)
B = DiscreteT1FuzzySet(B_points)


def calculations():
    """Demonstrate basic calculations on discrete fuzzy sets."""
    print 'Membership of x=1 in A:\n\t',
    print A.calculate_membership(1)
    print 'Alpha-cut of A at alpha=0.25\n\t',
    print A.calculate_alpha_cut(Decimal('0.25'))
    print 'Centroid of A:\n\t',
    print A.calculate_centroid()


def measuring_similarity():
    """Demonstrate measuring similarity."""
    print 's(A,B) =', similarity_t1.jaccard(A, B)


if __name__ == '__main__':
    calculations()
    measuring_similarity()
    visualisations.plot_sets((A, B))
