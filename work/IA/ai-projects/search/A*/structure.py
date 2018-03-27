import heapq # priority queue
from collections import defaultdict # dictionary of lists


# class that represents a priority queue
class PriorityQueue:

    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def remove(self):
        return heapq.heappop(self._queue)[-1]

    def isEmpty(self):
        return len(self._queue) == 0

    def getSize(self):
        return self._index


class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def x(self): return self.x

    def y(self): return self.x

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])# class that represents a node


class Node:

    def __init__(self, key, point):
        self.key = key
        self.point = point

    def getKey(self):
        return self.key

    def getPoint(self):
        return self.point


# class that represents a graph
class Graph:

    def __init__(self):
        self.nodes = {} # dictionary of the nodes
        self.edges = [] # list of 3-tuple (source, destination, weight)
        self.path = [] # path

        # dictionary with the lists of successors of each node, faster for get the successors
        # each item of list is a 2-tuple: (destination, weight)
        self.successors = defaultdict(list)


    # function that adds edges
    def addEdge(self, source, destination, weight):

        edge = (source, destination, weight) # creates tuple (3-tuple)

        if not self.existsEdge(edge): # adds edge if not exists
            self.nodes[source], self.nodes[destination] = source, destination # adds the nodes
            self.edges.append(edge) # adds edge
            self.successors[source.getKey()].append((destination, weight)) # adds successor
        else:
            print('Error: edge (%s -> %s with weight %s) already exists!!' \
                % (edge[0].getKey(), edge[1].getKey(), edge[2]))


    # function that checks if edge exists
    def existsEdge(self, edge):
        for e in self.edges:
            # compares source's key, destionation's key and weight of edge
            if e[0].getKey() == edge[0].getKey() and \
                e[1].getKey() == edge[1].getKey() and e[2] == edge[2]:
                return True
        return False


    # function that returns the path
    def getPath(self):
        return self.path


    def heuristic(self,a, b):
        """Manhathan distance"""

        (x1, y1) = (a.point.x, a.point.y)
        (x2, y2) = (b.point.x, b.point.y)
        return abs(x1 - x2) + abs(y1 - y2)

    def node_exists(self, name):
        for node in self.nodes:
            if node.key == name:
                return node
        return None

    # function that run the "A*" algorithm
    def executeAStar(self, inicio, objetivo):

        if not self.edges:
            print('Error: graph not contains edges!!')
        else:

            no_inicial = self.node_exists(inicio)
            no_objetivo = self.node_exists(objetivo)

            # checks if both the nodes exists
            if no_inicial is not None and no_objetivo is not None:

                if no_inicial == no_objetivo: # checks if are the same nodes
                    return True

                frontier = PriorityQueue() # creates a priority queue (min heap)

                # calculates costs
                g_cost, h_cost = 0, 0
                f_cost = g_cost + h_cost
                frontier.insert((no_inicial, g_cost, h_cost), f_cost)
                print("Nó {} inserido na fronteira".format(no_inicial.getKey()))

                while not frontier.isEmpty():

                    # a item of the queue is a 3-tuple: (current_node, g_cost, h_cost)
                    current_node, g_cost, h_cost = frontier.remove()
                    print("=========================================================")
                    print("Nó {} selecionado para a expansão. f(n) = {} , g(n) = {} ".format(current_node.getKey(), (g_cost + h_cost), g_cost))

                    if current_node.getKey() == no_objetivo.getKey():
                        print("Objetivo alcançado. {} ".format(current_node.getKey()))

                        print("Custo de {} --> {} [ f(n) = {}]".format(no_inicial.getKey(), no_objetivo.getKey(), (g_cost + h_cost)))
                        return True

                    # gets all the successors of "current_node"
                    for successor in self.successors[current_node.getKey()]:

                        destination, weight = successor # unpack 2-tuple successor
                        print("No sucessor de {} --> {}".format(current_node.getKey(), destination.getKey()))

                        # calculates costs
                        new_g_cost = g_cost + weight
                        h_cost = self.heuristic(no_objetivo, destination)
                        f_cost = new_g_cost + h_cost
                        print("Custo de {} --> {} [ f(n) = {} ,g(n) = {},h(n) ={} ]".format(current_node.getKey(), destination.getKey(), f_cost, g_cost, h_cost))

                        frontier.insert((destination, new_g_cost, h_cost), f_cost) # fronteira ordenada por f(n)
                        print("inseriu {} na fronteira".format(destination.getKey()))
            else:
                print('Error: the node(s) not exists in the graph!!')
