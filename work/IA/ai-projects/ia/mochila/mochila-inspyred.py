import random
import inspyred
import time
import logging.handlers

logger = logging.getLogger('inspyred.ec')
logger.propagate = False
logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler('inspyred-knapsack.log', mode='w', maxBytes=1024 * 100, backupCount=2)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Item(object):
    def __init__(self, v, w):
        self.value = v # Item's value. You want to maximize that!
        self.weight = w # Item's weight. The sum of all items should be <= CAPACITY


ITEMS = [
    Item(1, 3), Item(3, 8), Item(1, 12), Item(8, 2), Item(9, 8), Item(3, 4), Item(2, 4), Item(8, 5), Item(5, 1), Item(1, 1)
    , Item(1, 8), Item(6, 6), Item(3, 4), Item(2, 3), Item(5, 3), Item(2, 5), Item(7, 3), Item(8, 3), Item(9, 5), Item(3, 7)
    , Item(2, 4), Item(4, 3), Item(5, 7), Item(4, 2), Item(3, 3), Item(1, 5), Item(3, 4), Item(2, 3), Item(14, 7), Item(32, 19)
    , Item(20, 20), Item(19, 21), Item(15, 11), Item(37, 24), Item(18, 13), Item(13, 17), Item(19, 18), Item(10, 6)
    , Item(15, 5), Item(40, 25), Item(17, 12), Item(39, 19)
]

MAX_CAPACITY = 113
MAX_VALUE = 418

def generate_candidates(random, args):
    bits = args.get('num_bits', 42)
    return [random.choice([0, 1]) for _ in range(bits)]


@inspyred.ec.evaluators.evaluator
def evaluate_knapsack_candidates(candidate, args):
    total_weight, total_value = knapsack_calc(candidate)

    if total_weight > MAX_CAPACITY:
        return MAX_CAPACITY - total_weight
    else:
        return total_value


def  knapsack_calc(candidate):
    total_value = 0
    total_weight = 0
    index = 0
    for i in candidate:
        if index >= len(ITEMS):
            break
        if i == 1:
            total_value += ITEMS[index].value
            total_weight += ITEMS[index].weight
        index += 1
    return total_weight, total_value


rand = random.Random()
rand.seed(int(time.time()))

#Evolutionary computation representing a canonical genetic algorithm.
ga            = inspyred.ec.GA(rand)

ga.observer   = inspyred.ec.observers.stats_observer
ga.terminator = inspyred.ec.terminators.evaluation_termination
ga.variator   = inspyred.ec.variators.bit_flip_mutation

ga.selector = inspyred.ec.selectors.fitness_proportionate_selection
final_pop = ga.evolve(evaluator=evaluate_knapsack_candidates,
                      generator=generate_candidates,
                      max_evaluations=1000,
                      maximize=True,
                      mutation_rate=0.25,
                      num_elites=1,
                      pop_size=100,
                      crossover_rate=1,
                      num_crossover_points=1,
                      num_bits=42)

final_pop.sort(reverse=True)
for ind in final_pop:
    print(str(ind))

#pop.sort(reverse=True)
print("Terminated due to {0}.".format(ga.termination_cause))
print(final_pop[0])



total_weight, total_value = knapsack_calc(final_pop[0].candidate)

print("Peso calculado = {} ,  valor calculado = {}".format(total_weight,total_value))