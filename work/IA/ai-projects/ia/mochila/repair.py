from random import Random
from time import time
import inspyred
import math
import logging
import logging.handlers
from multiprocessing import Manager

# for a small tutorial on the Manager object:
# http://stackoverflow.com/questions/6832554/python-multiprocessing-how-do-i-share-a-dict-among-multiple-processes

logger = logging.getLogger('inspyred.ec')
logger.propagate = False
logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler('inspyred.log', mode='w', maxBytes=1024 * 100, backupCount=2)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def generate_rastrigin(random, args):
    size = args.get('num_inputs', 10)
    return [random.uniform(-5.12, 5.12) for i in xrange(size)]


def evaluate_rastrigin(candidates, args):
    fitness = []
    coeffs = args["coeffs"]
    for cs in candidates:
        fit = coeffs[0] * len(cs) + sum([((x - coeffs[1]) ** 2 - coeffs[0] *
                                          math.cos(2 * math.pi * (x - coeffs[1])))
                                         for x in cs])
        fitness.append(fit)
        c2 = list(cs)
        c2[0] += 0.5
        args['cands'].append((cs, c2, fit))
    return fitness


def geneRepair(offspring, args):
    # modify the offspring (assumes that the population is already correct
    d = args['cands']
    # go through each offspring and match the initial candidate and fitness
    # each entry of d is a list
    pickedLocs = []
    for off in offspring:
        fit = off.fitness
        match = [i for i, x in enumerate(d) if x[0] == off.candidate and not i in pickedLocs]
        # if there is more than one in match, pick the first
        matchInd = match[0]
        pickedLocs.append(matchInd)
        logger.debug(
            "Matched {4}   {0} with {1}: {2},{3}".format(off.candidate, d[matchInd][1], d[matchInd][2], off.fitness,
                                                         matchInd))
        off.candidate = d[matchInd][1]
        # if the candidate is changed, the fitness is erased.
        off.fitness = fit
    # clear out d once it's been used
    while len(d) > 0:
        d.pop()


def testObservers(population, num_generations, num_evaluations, args):
    # log the population
    for p in population:
        logger.debug(p)
    # if this is the first evaluation run, then the replacer that corrects the candidates won't be called
    # do that correction here
    if num_generations == 0:
        geneRepair(population, args)


def testReplacer(random, population, parents, offspring, args):
    geneRepair(offspring, args)
    # run the real replacer
    survivors = inspyred.ec.replacers.generational_replacement(random, population, parents, offspring, args)
    return survivors


def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())
    args = {}
    args["coeffs"] = [10, 1]
    ea = inspyred.ec.GA(prng)
   # ea.observer = testObservers
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    ea.replacer = testReplacer
    # make a manager
    manager = Manager()
    # we'll just use a list for now, since we want to avoid conflicts
    d = manager.list()

    args['cands'] = d

    final_pop = ea.evolve(generator=generate_rastrigin,
                          evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                          mp_evaluator=evaluate_rastrigin,
                          mp_num_cpus=8,
                          pop_size=10,
                          bounder=inspyred.ec.Bounder(-5.12, 5.12),
                          maximize=False,
                          max_evaluations=20,
                          num_inputs=3,
                          **args)

    if display:
        best = max(final_pop)
        print('Best Solution: \n{0}'.format(str(best)))
    return ea


if __name__ == '__main__':
    main(display=True)