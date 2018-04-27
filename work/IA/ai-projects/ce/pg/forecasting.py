import operator
import pandas as pd
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


train_data =  pd.read_csv("train_data.csv")
print(train_data.shape)

test_data =  pd.read_csv("test_data.csv")
print(test_data.shape)

# Define new functions
#def protectedDiv(left, right):
#    with numpy.errstate(divide='ignore',invalid='ignore'):
#        x = numpy.divide(left, right)
#        if isinstance(x, numpy.ndarray):
#            x[numpy.isinf(x)] = 1
#            x[numpy.isnan(x)] = 1
#        elif numpy.isinf(x) or numpy.isnan(x):
#            x = 1
#    return x

def protectedDiv(left, right):
    try: return left / right
    except ZeroDivisionError: return 1


pset = gp.PrimitiveSet("MAIN", 12)

pset.addPrimitive(numpy.add, 2, name="vadd")
pset.addPrimitive(numpy.subtract, 2, name="vsub")
pset.addPrimitive(numpy.multiply, 2, name="vmul")
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(numpy.negative, 1, name="vneg")
pset.addPrimitive(numpy.cos, 1, name="vcos")
pset.addPrimitive(numpy.sin, 1, name="vsin")

pset.addEphemeralConstant("rand101", lambda: random.randint(-1, 1))

pset.renameArguments(ARG0='x1')
pset.renameArguments(ARG1='x2')
pset.renameArguments(ARG2='x3')
pset.renameArguments(ARG3='x4')
pset.renameArguments(ARG4='x5')
pset.renameArguments(ARG5='x6')
pset.renameArguments(ARG6='x7')
pset.renameArguments(ARG7='x8')
pset.renameArguments(ARG8='x9')
pset.renameArguments(ARG9='x10')
pset.renameArguments(ARG10='x11')
pset.renameArguments(ARG11='x12')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)



def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def evalSymbReg(individual):

    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    diff = 0
    i = 0
    while i < len(train_data):
        if i + 13 > len(train_data):
            i -= i + 13 - len(train_data)
        x1 = train_data.iloc[i]['industrial_activity']
        x2 = train_data.iloc[i + 1]['industrial_activity']
        x3 = train_data.iloc[i + 2]['industrial_activity']
        x4 = train_data.iloc[i + 3]['industrial_activity']
        x5 = train_data.iloc[i + 4]['industrial_activity']
        x6 = train_data.iloc[i + 5]['industrial_activity']
        x7 = train_data.iloc[i + 6]['industrial_activity']
        x8 = train_data.iloc[i + 7]['industrial_activity']
        x9 = train_data.iloc[i + 8]['industrial_activity']
        x10 = train_data.iloc[i + 9]['industrial_activity']
        x11 = train_data.iloc[i + 10]['industrial_activity']
        x12 = train_data.iloc[i + 11]['industrial_activity']
        y = train_data.iloc[i + 12]['industrial_activity']
        i += i + 12

        diff += numpy.sum((func(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12) - y) ** 2)

    return diff,


toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=5)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=50))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=50))


def main():
    random.seed(318)

    pop = toolbox.population(n=500)
    hof = tools.HallOfFame(5)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 51, stats, halloffame=hof)

    return pop, stats, hof


if __name__ == "__main__":
    #pop, stats, hof = main()
    #print(pop[0])
    #print(hof[0])
    #func = toolbox.compile(expr=pop[0])
    func = toolbox.compile(expr="vadd(vmul(protectedDiv(vsub(vsub(vsub(x12, vcos(vsub(vsub(x12, x4), protectedDiv(1, x2)))), vsin(x12)), 1), x2), vsin(vmul(protectedDiv(vsub(vsub(x12, vsin(x12)), 1), vsin(x4)), vsin(x10)))), vsub(vsub(x12, vcos(vsin(vneg(vmul(vsin(vneg(vmul(x1, x10))), x10))))), 1))")

    print(func(72.4
,69.7
,77.4
,79.6
,80.4
,77.5
,83.3
,83.6
,82.1
,89.2
,83.9
,74.6
)) #, 75.7

    func2 = toolbox.compile(expr="vadd(vmul(protectedDiv(vsub(vsub(vsub(x12, vcos(vsub(vsub(x12, vcos(vcos(vsub(vsub(x12, vcos(vsin(x10))), protectedDiv(x5, x2))))), protectedDiv(1, vcos(vsub(x12, vcos(vsin(protectedDiv(vsub(vcos(vsub(vsub(x12, x9), protectedDiv(1, x2))), 1), protectedDiv(vsub(x12, vsin(x12)), x2)))))))))), vsin(x12)), 1), x2), vsin(vmul(protectedDiv(vsub(vsub(x12, vsin(x12)), 1), vsin(x4)), vsin(x10)))), vsub(vsub(x12, vcos(vsin(vsin(vneg(vmul(vsin(vneg(vmul(x1, x10))), x10)))))), 1))")
    print(func2(72.4
,69.7
,77.4
,79.6
,80.4
,77.5
,83.3
,83.6
,82.1
,89.2
,83.9
,74.6
)) #, 75.7


#vadd(vsin(vsin(x10)), vsub(vsub(x12, protectedDiv(vcos(vsin(vsin(x10))), x2)), vsin(x2))) 0.146398

# 75,8
# 83,7
# 83
# 86,3
# 87,7
# 89,6
# 93
# 90,6
# 90,2
# 86,6
# 77,2
# 77,8
# 75,7


