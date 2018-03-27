from graphcreator import GraphBuilder

gb = GraphBuilder()

graph = gb.build_graph()
total_cost = graph.executeAStar('C', 'A')  # executes the algorithm
