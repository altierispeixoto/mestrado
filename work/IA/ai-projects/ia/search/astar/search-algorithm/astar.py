# -*- coding: utf-8 -*-
""" generic A-Star path searching algorithm """

from abc import ABCMeta, abstractmethod
from heapq import heappush, heappop

__author__ = "Julien Rialland"
__copyright__ = "Copyright 2012-2017, J.Rialland"
__license__ = "BSD"
__version__ = "0.9"
__maintainer__ = __author__
__email__ = ''.join(map(chr, [106, 117, 108, 105, 101, 110, 46, 114, 105,
                              97, 108, 108, 97, 110, 100, 64, 103, 109, 97, 105, 108, 46, 99, 111, 109]))
__status__ = "Production"


Infinite = float('inf')


class AStar:
    __metaclass__ = ABCMeta
    __slots__ = ()

    class SearchNode:
        __slots__ = ('data', 'gscore', 'fscore',
                     'closed', 'came_from', 'out_openset')

        def __init__(self, data, gscore=Infinite, fscore=Infinite):
            self.data = data
            self.gscore = gscore
            self.fscore = fscore
            self.closed = False
            self.out_openset = True
            self.came_from = None

        def __lt__(self, b):
            return self.fscore < b.fscore


    class SearchNodeDict(dict):

        def __missing__(self, k):
            v = AStar.SearchNode(k)
            self.__setitem__(k, v)
            return v

    @abstractmethod
    def heuristic_cost_estimate(self, current, goal):
        """Computes the estimated (rough) distance between a node and the goal,
         this method must be implemented in a subclass. The second parameter is always the goal."""
        raise NotImplementedError

    @abstractmethod
    def distance_between(self, n1, n2):
        """Gives the real distance between two adjacent nodes n1 and n2 (i.e n2 belongs to the list of n1's neighbors).
           n2 is guaranteed to belong to the list returned by the call to neighbors(n1).
           This method must be implemented in a subclass."""
        raise NotImplementedError

    @abstractmethod
    def cost_between(self, n1, n2, speed_average):
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node):
        """For a given node, returns (or yields) the list of its neighbors.
         this method must be implemented in a subclass"""
        raise NotImplementedError

    def is_goal_reached(self, current, goal):
        """ returns true when we can consider that 'current' is the goal"""
        return current == goal

    def reconstruct_path(self, last, reversePath=False):
        def _gen():
            current = last
            while current:
                yield current.data
                current = current.came_from
        if reversePath:
            return _gen()
        else:
            return reversed(list(_gen()))

    def astar(self, start, goal, reversePath=False,use_speed_average=False):

        closed_list = set()
        child_not_openset = set()

        if self.is_goal_reached(start, goal):
            return [start]

        searchNodes = AStar.SearchNodeDict()
        startNode = searchNodes[start] = AStar.SearchNode(start, gscore=.0, fscore=self.heuristic_cost_estimate(start, goal))
        openSet = []
        heappush(openSet, startNode)
        while openSet:

            # Retira o nó da lista de prioridades
            current = heappop(openSet)

            print("Nó {} selecionado para expansão".format(current.data.name))
            print("f({}) = {}".format(current.data.name, current.fscore))
            print("g({}) = {}".format(current.data.name, current.gscore))

            if self.is_goal_reached(current.data, goal):
                print("O objetivo foi alcançado {}".format(current.data.name))
                return self.reconstruct_path(current, reversePath)

            current.out_openset = True
            current.closed = True
            closed_list.add(current)

            for n, speed_average in self.neighbors(current.data):
                filho = searchNodes[n]
                print(speed_average)

            #for filho in [searchNodes[n] for n , speed in self.neighbors(current.data)]:

                print("Estado do filho {}, Já explorado = {}".format(filho.data.name, filho.closed))
                print("f({}) = {}".format(filho.data.name, filho.fscore))
                print("g({}) = {}".format(filho.data.name, filho.fscore))

                if filho.closed:
                    continue

                #if(use_speed_average):
                tentative_gscore = current.gscore + \
                                   self.cost_between(current.data, filho.data, speed_average) \
                    if use_speed_average \
                    else self.distance_between(current.data, filho.data)

                #tentative_gscore = current.gscore + self.distance_between(current.data, filho.data)

                if tentative_gscore >= filho.gscore:
                    continue

                filho.came_from = current
                filho.gscore = tentative_gscore
                filho.fscore = tentative_gscore + self.heuristic_cost_estimate(filho.data, goal)

                if filho.out_openset:
                    filho.out_openset = False
                    heappush(openSet, filho)
                    print("Filho {} foi adicionado a froteira.".format(filho.data.name))
                else:
                    child_not_openset.add(filho)
                    print("Filho {} não foi adicionado a froteira.".format(filho.data.name))

            print("Quantidade total de nós explorados {}".format(closed_list.__len__() + openSet.__len__() + child_not_openset.__len__()))
            print("Tamanho da fronteira {}".format(openSet.__len__()))

        return None


def find_path(start, goal, neighbors_fnct, reversePath=False, heuristic_cost_estimate_fnct=lambda a, b: Infinite, distance_between_fnct=lambda a, b: 1.0, use_speed_average=False):

    """A non-class version of the path finding algorithm"""
    class FindPath(AStar):

        def heuristic_cost_estimate(self, current, goal):
            return heuristic_cost_estimate_fnct(current, goal)

        def distance_between(self, n1, n2):
            return distance_between_fnct(n1, n2)

        def cost_between(self, n1, n2, speed_average):
            return distance_between_fnct(n1, n2) / speed_average

        def neighbors(self, node):
            return neighbors_fnct(node)

        def is_goal_reached(self, current, goal):
            return current == goal

    return FindPath().astar(start, goal, reversePath, use_speed_average=use_speed_average)


__all__ = ['AStar', 'find_path']