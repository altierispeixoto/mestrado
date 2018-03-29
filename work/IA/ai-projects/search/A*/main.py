from graphcreator import GraphBuilder

gb = GraphBuilder()

graph = gb.build_graph()
total_cost = graph.executeAStar('H', 'A')  # executes the algorithm
