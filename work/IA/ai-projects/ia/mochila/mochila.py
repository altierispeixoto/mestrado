import random
import inspyred
import time
from items import ITEMS, MAX_CAPACITY ,MAX_VALUE
import pylab


def generate_candidates(random, args):
    bits = args.get('num_bits', 42)
    return [random.choice([0, 1]) for _ in range(bits)]

def  knapsack_calc(candidate):
    total_value = 0
    total_weight = 0
    index = 0
    nr_itens = 0
    for i in candidate:
        if index >= len(ITEMS):
            break
        if i == 1:
            total_value += ITEMS[index].value
            total_weight += ITEMS[index].weight
            nr_itens += 1
        index += 1
    return total_weight, total_value , nr_itens


@inspyred.ec.evaluators.evaluator
def evaluate_knapsack_candidates_repair(candidate, args):

    total_weight, total_value , nr_itens = knapsack_calc(candidate)
    # indivíduo será reparado na função my_replacer
    if total_weight > MAX_CAPACITY:
        return -1
    else:
        return total_value


def knapsack_penalize(total_weight):
    return MAX_CAPACITY - total_weight


def evaluate_knapsack_candidate(candidate, args):
    total_weight, total_value , nr_itens= knapsack_calc(candidate)
    return total_value


def my_replacer(random, population, parents, offspring, args):
    survivors = []
    psize = len(offspring)

    for i in range(psize):
        if offspring[i].fitness == -1:
            total_weight, total_value , nr_itens = knapsack_calc(offspring[i].candidate)

            for gene_index in range(0, len(offspring[i].candidate)):
                if offspring[i].candidate[gene_index] == 1:
                    weight = ITEMS[gene_index].weight
                    if total_weight > MAX_CAPACITY:
                        total_weight -= weight
                        offspring[i].candidate[gene_index] = 0
                    else:
                        offspring[i].candidate[gene_index] = 1
            offspring[i].fitness = evaluate_knapsack_candidate(offspring[i].candidate, args)
        survivors.append(offspring[i])

    return survivors



def knapsack_observer(population, num_generations, num_evaluations, args):

    total_weight, total_value, nr_itens = knapsack_calc(max(population).candidate)
    print("{},{}".format(num_generations, total_value))


def print_best_candidate(candidate):
    total_weight, total_value, nr_itens = knapsack_calc(candidate)
    print("-------------------------------------------")
    print("Mochila   Peso   Valor ")
    print("-------------------------------------------")
    index = 0
    for i in candidate:
        if index >= len(ITEMS):
            break
        if i == 1:
            print("ITEM[{}]  {}  {} ".format(index + 1, ITEMS[index].weight, ITEMS[index].value))
        index += 1
    print("-------------------------------------------")
    print("Mochila com {} ITENS".format(nr_itens))
    print("Mochila com {} KG".format(total_weight))
    print("Mochila com {} VALOR".format(total_value))
    print("-------------------------------------------")


@inspyred.ec.evaluators.evaluator
def evaluate_knapsack_candidates_penalize(candidate, args):
    total_weight, total_value, nr_items = knapsack_calc(candidate)

    if total_weight > MAX_CAPACITY:
        return knapsack_penalize(total_weight)
    else:
        return total_value


def ga_mochila(ga, method):

    final_pop = ga.evolve(evaluator=method,
                          generator=generate_candidates,
                          max_evaluations=1000,
                          maximize=True,
                          num_elites = 5,
                          mutation_rate=0.05,
                          crossover_rate=0.5,
                          pop_size=200,
                          num_selected=50,

                          num_crossover_points=1,
                          num_bits=42)

    final_pop.sort(reverse=True)
    print("Terminated due to {0}.".format(ga.termination_cause))
    print(final_pop[0])

    total_weight, total_value , nr_itens = knapsack_calc(final_pop[0].candidate)

    print_best_candidate(final_pop[0].candidate)

    print("Peso calculado = {} ,  valor calculado = {} \n".format(total_weight, total_value))
    #pylab.show()
    return total_value

def setup_ga():

    seed = int(time.time())
    rand = random.Random()
    rand.seed(seed)

    # Evolutionary computation representing a canonical genetic algorithm.
    ga = inspyred.ec.GA(rand)
    ga.observer = [knapsack_observer]

    # condição de término pelo máximo de avaliações
    ga.terminator = inspyred.ec.terminators.evaluation_termination

    # mutação binária
    ga.variator = inspyred.ec.variators.bit_flip_mutation

    # Seleção pela roleta
    ga.selector = inspyred.ec.selectors.fitness_proportionate_selection

    return ga, seed


def frequencyDistribution(data):
    return {i: data.count(i) for i in data}

if __name__ == "__main__":
    total_values = []

    from datetime import datetime

    start_time = datetime.now()

    execution_type = 'penalize'
    ga, seed = setup_ga()

    for i in range(0, 300):
        if execution_type == 'repair':
            ga.replacer = my_replacer
            total_values.append(ga_mochila(ga, evaluate_knapsack_candidates_repair))
        else:
            total_values.append(ga_mochila(ga, evaluate_knapsack_candidates_penalize))

    print(frequencyDistribution(total_values))
    time_elapsed = datetime.now() - start_time

    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))