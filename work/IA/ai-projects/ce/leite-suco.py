import random
from inspyred import ec
from inspyred.ec import replacers
from inspyred.ec import terminators
from inspyred.ec import observers


def generate_candidates(random, args):
    """Generate candidates (Leite,Suco)"""
    return random.randint(0, 800), random.randint(0, 750)


def h1(candidate):
    """h1(L,S) = (max{0,(6*L+5*S)/100-60})/15"""
    return max(0, (6*candidate[0]+5*candidate[1])/100-60)/15


def h2(candidate):
    """h2(L,S) = (max{0,(10*L+20*S)-15000})/3750"""
    return max(0, (10*candidate[0]+20*candidate[1])-15000)/3750


def h3(candidate):
    """h3(L,S) = (max{0,L-800}/200)"""
    return max(0, candidate[0]-800)/200


def h4(candidate):
    """h4(L,S) = (max{0,S-750}/187,5)"""
    return max(0, candidate[1]-750)/187.5


def fitness(candidate):
    return (candidate[0] * 5 + candidate[1] * 4.5)/7375


def my_constraint_function(candidate):
    return fitness(candidate) - (h1(candidate=candidate)+h2(candidate)+h3(candidate)+h4(candidate))


def my_evaluator(candidates, args):
    fitness = []
    for c in candidates:
        fitness.append(my_constraint_function(c))
    return fitness


def constrained_tournament_selection(random, population, args):
    num_selected = args.setdefault("num_selected", 1)
    constraint_func = args.setdefault("constraint_function", None)
    tournament_size = 2
    pop = list(population)

    selected = []
    for _ in range(num_selected):
        tournament = random.sample(pop, tournament_size)
        # If there is not a constraint function,
        # just do regular tournament selection.
        if constraint_func is None:
            selected.append(max(tournament))
        else:
            cons = [constraint_func(t.candidate) for t in tournament]
            # If no constraints are violated, just do 
            # regular tournament selection.
            if max(cons) == 0:
                selected.append(max(tournament))
            # Otherwise, choose the least violator 
            # (which may be a non-violator).
            else:
                selected.append(tournament[cons.index(min(cons))])
    return selected


r = random.Random()
r.seed(42)

myec = ec.EvolutionaryComputation(r)
myec.selector = constrained_tournament_selection

# myec.variator = variators.gaussian_mutation
myec.replacer = replacers.generational_replacement
myec.terminator = terminators.evaluation_termination
myec.observer = observers.stats_observer

pop = myec.evolve(generator=generate_candidates,
                  evaluator=my_evaluator,
                  pop_size=500,
                  num_selected=15,
                  constraint_func=my_constraint_function,
                  mutation_rate=0.5,
                  max_evaluations=2000)

pop.sort(reverse=True)
print("Terminated due to {0}.".format(myec.termination_cause))
print(pop[0])

leite = pop[0].candidate[0]
suco = pop[0].candidate[1]

valor = (5*leite)+(4.5*suco)
print(valor) #680 388  5146
