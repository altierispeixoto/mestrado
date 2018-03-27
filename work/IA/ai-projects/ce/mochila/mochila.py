import random


class Item(object):
    def __init__(self, v, w):
        self.value = v # Item's value. You want to maximize that!
        self.weight = w # Item's weight. The sum of all items should be <= CAPACITY

##########################################################################################
# 0-1 Knapsack Problem solved using Genetic Algorithms
#
# Edmilson Rocha
# GitHub: https://github.com/edmilsonrobson
##########################################################################################
# CONFIG

# Obj      1 2 3  4 5 6 7 8 9 10 11 12 13 14
# Peso(kg) 3 8 12 2 8 4 4 5 1  1  8  6  4  3
# Valor    1 3  1 8 9 3 2 8 5  1  1  6  3  2

# Obj      15 16 17 18 19 20 21 22 23 24 25 26 27 28
# Peso(kg)  3  5  7  3  5  7  4  3  7  2  3  5  4  3
# Valor     5  2  3  8  9  3  2  4  5  4  3  1  3  2

# Obj     29 30 31 32 33 34 35 36 37 38 39 40 41 42
# Peso(Kg)  7 19 20 21 11 24 13 17 18  6 15 25 12 19
# Valor    14 32 20 19 15 37 18 13 19 10 15 40 17 39


ITEMS = [
    Item(1, 3), Item(3, 8), Item(1, 12), Item(8, 2), Item(9, 8), Item(3, 4), Item(2, 4), Item(8, 5), Item(5, 1), Item(1, 1)
    , Item(1, 8), Item(6, 6), Item(3, 4), Item(2, 3), Item(5, 3), Item(2, 5), Item(7, 3), Item(8, 3), Item(9, 5), Item(3, 7)
    , Item(2, 4), Item(4, 3), Item(5, 7), Item(4, 2), Item(3, 3), Item(1, 5), Item(3, 4), Item(2, 3), Item(14, 7), Item(32, 19)
    , Item(20, 20), Item(19, 21), Item(15, 11), Item(37, 24), Item(18, 13), Item(13, 17), Item(19, 18), Item(10, 6)
    , Item(15, 5), Item(40, 25), Item(17, 12), Item(39, 19)
]

# Capacity of the knapsack randomized according to number of items
CAPACITY = 113

# Size of initial population filled with some permutation of 0s and 1s
POP_SIZE = 50

# Maximum number of generations the algorithm will run
GEN_MAX = 200

# Start initial population with only zeros? If not, random permutation of 0s and 1s will be given
# Starting with 0s and 1s will generally make you find a good solution faster
START_POP_WITH_ZEROES = False


# END OF CONFIG
##########################################################################################

def fitness(target):
    """
    fitness(target) will return the fitness value of permutation named "target".
    Higher scores are better and are equal to the total value of items in the permutation.
    If total_weight is higher than the capacity, return 0 because the permutation cannot be used.
    """
    total_value = 0
    total_weight = 0
    index = 0
    for i in target:
        if index >= len(ITEMS):
            break
        if i == 1:
            total_value += ITEMS[index].value
            total_weight += ITEMS[index].weight
        index += 1

    if total_weight > CAPACITY:
        # Nope. No good!
        return 0
    else:
        # OK
        return total_value


def spawn_starting_population(amount):
    return [spawn_individual() for x in range(0, amount)]


def spawn_individual():
    if START_POP_WITH_ZEROES:
        return [random.randint(0, 0) for x in range(0, len(ITEMS))]
    else:
        return [random.randint(0, 1) for x in range(0, len(ITEMS))]


def mutate(target):
    """
    Changes a random element of the permutation array from 0 -> 1 or from 1 -> 0.
    """
    r = random.randint(0, len(target) - 1)
    if target[r] == 1:
        target[r] = 0
    else:
        target[r] = 1


def evolve_population(pop):
    parent_eligibility = 0.2
    mutation_chance = 0.08
    parent_lottery = 0.05

    parent_length = int(parent_eligibility * len(pop))
    parents = pop[:parent_length]
    nonparents = pop[parent_length:]

    # Parent lottery!
    for np in nonparents:
        if parent_lottery > random.random():
            parents.append(np)

    # Mutation lottery... I guess?
    for p in parents:
        if mutation_chance > random.random():
            mutate(p)

    # Breeding! Close the doors, please.
    children = []
    desired_length = len(pop) - len(parents)
    while len(children) < desired_length:
        male = pop[random.randint(0, len(parents) - 1)]
        female = pop[random.randint(0, len(parents) - 1)]
        half = int(len(male) / 2)
        child = male[:half] + female[half:]  # from start to half from father, from half to end from mother
        if mutation_chance > random.random():
            mutate(child)
        children.append(child)

    parents.extend(children)
    return parents


def main():
    generation = 1
    population = spawn_starting_population(POP_SIZE)
    for g in range(0, GEN_MAX):
        print("Generation {} with {}".format(generation, len(population)))
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        for i in population:
            print("{}, fit: {}".format(str(i), fitness(i)))
        population = evolve_population(population)
        generation += 1


if __name__ == "__main__":
    main()