from structure import Graph, Node, Point

class GraphBuilder:


    def build_graph(self):

        # creates the nodes
        # region Nodes
        A = Node('A', Point(1, 1))
        B = Node('B', Point(1, 2))
        C = Node('C', Point(1, 3))
        D = Node('D', Point(1, 4))
        E = Node('E', Point(1, 5))

        F = Node('F', Point(2, 1))
        G = Node('G', Point(2, 2))
        H = Node('H', Point(2, 3))
        I = Node('I', Point(2, 4))
        J = Node('J', Point(2, 5))

        K = Node('K', Point(3, 1))
        L = Node('L', Point(3, 2))
        M = Node('M', Point(3, 3))
        N = Node('N', Point(3, 4))
        O = Node('O', Point(3, 5))

        P = Node('P', Point(4, 1))
        Q = Node('Q', Point(4, 2))
        R = Node('R', Point(4, 3))
        S = Node('S', Point(4, 4))
        T = Node('T', Point(4, 5))

        U = Node('U', Point(5, 1))
        V = Node('V', Point(5, 2))
        W = Node('W', Point(5, 3))
        X = Node('X', Point(5, 4))
        Y = Node('Y', Point(5, 5))

        Z = Node('Z', Point(6, 1))
        AA = Node('AA', Point(6, 2))
        BB = Node('BB', Point(6, 3))
        CC = Node('CC', Point(6, 4))
        DD = Node('DD', Point(6, 5))

        #endregion

        # creates graph
        graph = Graph()

        # add the edges
        graph.addEdge(A, B, 50)
        graph.addEdge(A, F, 50)

        graph.addEdge(B, A, 50)
        graph.addEdge(B, C, 50)
        graph.addEdge(B, G, 50)

        graph.addEdge(C, B, weight=50)
        graph.addEdge(C, D, weight=50)
        graph.addEdge(C, H, weight=50)

        graph.addEdge(D, C, weight=50)
        graph.addEdge(D, E, weight=50)
        graph.addEdge(D, I, weight=50)

        graph.addEdge(E, D, weight=50)
        graph.addEdge(E, J, weight=50)

        graph.addEdge(F, A, weight=50)
        graph.addEdge(F, K, weight=50)
        graph.addEdge(F, G, weight=50)

        graph.addEdge(G, F, weight=50)
        graph.addEdge(G, H, weight=50)
        graph.addEdge(G, L, weight=50)

        graph.addEdge(H, G, weight=50)
        graph.addEdge(H, I, weight=50)
        graph.addEdge(H, C, weight=50)
        graph.addEdge(H, M, weight=50)

        graph.addEdge(I, H, weight=50)
        graph.addEdge(I, J, weight=50)
        graph.addEdge(I, D, weight=50)
        graph.addEdge(I, N, weight=50)

        graph.addEdge(J, E, weight=50)
        graph.addEdge(J, O, weight=50)
        graph.addEdge(J, I, weight=50)

        graph.addEdge(K, F, weight=50)
        graph.addEdge(K, P, weight=50)
        graph.addEdge(K, L, weight=50)

        graph.addEdge(L, K, weight=50)
        graph.addEdge(L, M, weight=50)
        graph.addEdge(L, G, weight=50)
        graph.addEdge(L, Q, weight=50)

        graph.addEdge(M, L, weight=50)
        graph.addEdge(M, N, weight=50)
        graph.addEdge(M, H, weight=50)
        graph.addEdge(M, R, weight=50)

        graph.addEdge(N, M, weight=50)
        graph.addEdge(N, O, weight=50)
        graph.addEdge(N, I, weight=50)
        graph.addEdge(N, S, weight=50)

        graph.addEdge(O, J, weight=50)
        graph.addEdge(O, T, weight=50)
        graph.addEdge(O, N, weight=50)

        graph.addEdge(P, K, weight=50)
        graph.addEdge(P, U, weight=50)
        graph.addEdge(P, Q, weight=50)

        graph.addEdge(Q, P, weight=50)
        graph.addEdge(Q, L, weight=50)
        graph.addEdge(Q, R, weight=50)
        graph.addEdge(Q, U, weight=50)

        graph.addEdge(R, Q, weight=50)
        graph.addEdge(R, S, weight=50)
        graph.addEdge(R, M, weight=50)
        graph.addEdge(R, W, weight=50)

        graph.addEdge(S, R, weight=50)
        graph.addEdge(S, T, weight=50)
        graph.addEdge(S, N, weight=50)
        graph.addEdge(S, X, weight=50)

        graph.addEdge(T, O, weight=50)
        graph.addEdge(T, Y, weight=50)
        graph.addEdge(T, S, weight=50)

        graph.addEdge(U, P, weight=50)
        graph.addEdge(U, Z, weight=50)
        graph.addEdge(U, V, weight=50)

        graph.addEdge(V, Q, weight=50)
        graph.addEdge(V, AA, weight=50)
        graph.addEdge(V, U, weight=50)
        graph.addEdge(V, W, weight=50)

        graph.addEdge(W, V, weight=50)
        graph.addEdge(W, X, weight=50)
        graph.addEdge(W, R, weight=50)
        graph.addEdge(W, BB, weight=50)

        graph.addEdge(X, W, weight=50)
        graph.addEdge(X, Y, weight=50)
        graph.addEdge(X, S, weight=50)
        graph.addEdge(X, CC, weight=50)

        graph.addEdge(X, G, weight=50)
        graph.addEdge(X, I, weight=50)
        graph.addEdge(X, C, weight=50)
        graph.addEdge(X, M, weight=50)

        graph.addEdge(Y, T, weight=50)
        graph.addEdge(Y, X, weight=50)
        graph.addEdge(Y, DD, weight=50)

        graph.addEdge(Z, U, weight=50)
        graph.addEdge(Z, AA, weight=50)

        graph.addEdge(AA, Z, weight=50)
        graph.addEdge(AA, U, weight=50)
        graph.addEdge(AA, BB, weight=50)

        graph.addEdge(BB, AA, weight=50)
        graph.addEdge(BB, CC, weight=50)
        graph.addEdge(BB, W, weight=50)

        graph.addEdge(CC, BB, weight=50)
        graph.addEdge(CC, DD, weight=50)
        graph.addEdge(CC, X, weight=50)

        graph.addEdge(DD, CC, weight=50)
        graph.addEdge(DD, Y, weight=50)

        return graph

