###
# Breadth First Search - Busca em Largura
#
# http://interactivepython.org/runestone/static/pythonds/Graphs/ImplementingBreadthFirstSearch.html
#
# https://www.redblobgames.com/pathfinding/a-star/implementation.html
#
#http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
#
###

graph = {'Ag': set(['A', 'B', 'C', 'D']),
         'A': set(['E']),
         'E': set(['A', 'I', 'J']),
         'I': set(['E']),
         'J': set(['E', 'Q']),
         'Q': set(['J']),
         'B': set(['F']),
         'F': set(['B', 'K', 'L']),
         'K': set(['F', 'R']),
         'L': set(['F', 'R']),
         'R': set(['K', 'L', 'O']),
         'C': set(['G']),
         'G': set(['C', 'M', 'N']),
         'M': set(['G']),
         'N': set(['G']),
         'D': set(['H']),
         'H': set(['D', 'O', 'P']),
         'O': set(['H', 'R']),
         'P': set(['H'])
         }


def bfs(graph, start):

    print('initialize the search')
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            print("nó visitado "+vertex)
            queue.extend(graph[vertex] - visited)
            print("nós filhos")
            print(graph[vertex] - visited)

    return visited


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))


def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


print(list(bfs_paths(graph, 'Ag', 'E')))

print(list(dfs_paths(graph, 'Ag', 'E')))


# {'B', 'C', 'A', 'F', 'D', 'E'}
#bfs(graph(), 'A')

#dfs(graph(), 'C')


