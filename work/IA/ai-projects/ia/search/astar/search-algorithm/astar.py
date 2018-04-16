# -*- coding: utf-8 -*-

from abc import abstractmethod
from heapq import heappush, heappop



Infinite = float('inf')

class AStar:

    class SearchNode:

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
    def heuristic_cost_estimate(self, current, goal, speed_average):
        """Metodo de heuristica para avaliação do tempo estimado da rota"""
        raise NotImplementedError

    @abstractmethod
    def distance_between(self, n1, n2):
        """Método de heurística para cálculo da distancia entre cruzamentos"""
        raise NotImplementedError

    @abstractmethod
    def cost_between(self, n1, n2, speed_average):
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node):
        """Retorna os filhos de um nó."""
        raise NotImplementedError

    def is_goal_reached(self, current, goal):
        """ retorna true quando o destino é alcançado"""
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

    def astar(self, start, goal, reversepath=False, use_speed_average=False):

        SPEED_AVERAGE_OVERALL=66.6
        closed_list = set()
        child_not_openset = set()

        if self.is_goal_reached(start, goal):
            return [start]

        searchNodes = AStar.SearchNodeDict()

        if use_speed_average:
            startNode = searchNodes[start] = AStar.SearchNode(start, gscore=.0, fscore=self.heuristic_cost_estimate(start, goal, SPEED_AVERAGE_OVERALL))
        else:
            startNode = searchNodes[start] = AStar.SearchNode(start, gscore=.0,
                                                              fscore=self.distance_between(start, goal))

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
                return self.reconstruct_path(current, reversepath)

            current.out_openset = True
            current.closed = True
            closed_list.add(current)

            for n, speed_average in self.neighbors(current.data):
                filho = searchNodes[n]

                print("Estado do filho {}, Já explorado = {}".format(filho.data.name, filho.closed))

                if filho.closed:
                    continue

                nanl = 0
                if use_speed_average:
                    nanl = self.heuristic_cost_estimate(current.data, filho.data, speed_average)
                    tentative_gscore = current.gscore + self.heuristic_cost_estimate(current.data, filho.data, speed_average)
                else:
                    nanl = self.distance_between(current.data, filho.data)
                    tentative_gscore = current.gscore + self.distance_between(current.data, filho.data)

                if tentative_gscore >= filho.gscore:
                    continue

                filho.came_from = current
                filho.gscore = tentative_gscore
                hscore=0
                if use_speed_average:
                    hscore = self.heuristic_cost_estimate(filho.data, goal, SPEED_AVERAGE_OVERALL)
                    filho.fscore = tentative_gscore + hscore
                else:
                    hscore = self.distance_between(filho.data, goal)
                    filho.fscore = tentative_gscore + hscore

                print("f({}) = {}".format(filho.data.name, filho.fscore))
                print("g({}) = {}".format(filho.data.name, tentative_gscore))
                print("c({}, a, {})({}) = {}".format(current.data.name,filho.data.name, filho.data.name, nanl))
                print("h({}) = {}".format(filho.data.name, hscore))

                if filho.out_openset:
                    filho.out_openset = False
                    heappush(openSet, filho)
                    print("Filho {} foi adicionado a fronteira.".format(filho.data.name))
                else:
                    child_not_openset.add(filho)
                    print("Filho {} não foi adicionado a fronteira.".format(filho.data.name))
                print("------------------------------------------------------------------")
            print("Quantidade total de nós explorados {}".format(closed_list.__len__() + openSet.__len__() + child_not_openset.__len__()))
            print("Tamanho da fronteira {}".format(openSet.__len__()))
            print("------------------------------------------------------------------")
        return None


def find_path(start, goal, neighbors_fnct,
              reversepath=False,
              heuristic_cost_estimate_fnct=lambda a, b: Infinite,
              distance_between_fnct=lambda a, b: 1.0,
              use_speed_average=False):


    class FindPath(AStar):

        def heuristic_cost_estimate(self, current, goal, speed_average):
            return heuristic_cost_estimate_fnct(current, goal,speed_average)

        def distance_between(self, n1, n2):
            return distance_between_fnct(n1, n2)

        def neighbors(self, node):
            return neighbors_fnct(node)

        def is_goal_reached(self, current, goal):
            return current == goal

    return FindPath().astar(start, goal, reversepath, use_speed_average=use_speed_average)