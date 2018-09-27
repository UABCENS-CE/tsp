import numpy as np

def random_tour(O):
    names = O.V
    return list(np.random.permutation(names))

def TSP_greedy(O,start_index=0):
    nodes = O.V
    matrix = O._M
    n = len(nodes)
    tour = [nodes[start_index]]
    for i in range(n-1):
        available_nodes = list(set(nodes)-set(tour+[nodes[i]]))
        neighbors = {k:matrix[tour[-1]][k] for k in available_nodes}
        best = min(neighbors, key=neighbors.get)
        tour.append(best)
    return tour
	
def Best_TSP_greedy(O):
    _min_cost = np.inf
    _min_tour = None
    for start_index in range(len(O.V)):
        tour = TSP_greedy(O,start_index=start_index)
        cost = O.evaluate_tour(tour)
        if cost<_min_cost:
            _min_cost=cost
            _min_tour=tour
    return _min_tour
	
def tsp_c(O):
    data = O.points
	
	# build a graph
    G = build_graph(data)

    # build a minimum spanning tree
    MSTree = minimum_spanning_tree(G)

    # find odd vertexes
    odd_vertexes = find_odd_vertexes(MSTree)

    # add minimum weight matching edges to MST
    minimum_weight_matching(MSTree, G, odd_vertexes)

    # find an eulerian tour
    eulerian_tour = find_eulerian_tour(MSTree, G)

    current = eulerian_tour[0]
    path = [str(current+1)]
    visited = [False] * len(eulerian_tour)
    visited[current] = True
    length = 0
    for v in eulerian_tour[1:]:
        if not visited[v]:
            path.append(str(v+1))
            visited[v] = True
            length += G[current][v]
            current = v
    return path


def get_length(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def build_graph(data):
    graph = {}
    for this in range(len(data)):
        for another_point in range(len(data)):
            if this != another_point:
                if this not in graph:
                    graph[this] = {}
                graph[this][another_point] = get_length(data[this][0], data[this][1], data[another_point][0],
                                                        data[another_point][1])
    return graph


class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object
        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]
        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def minimum_spanning_tree(G):
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)
    return tree


def find_odd_vertexes(MST):
    tmp_g = {}
    vertexes = []
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0
        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0
        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1
    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)
    return vertexes


def minimum_weight_matching(MST, G, odd_vert):
    import random
    random.shuffle(odd_vert)
    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u
        MST.append((v, closest, length))
        odd_vert.remove(closest)


def find_eulerian_tour(MatchedMSTree, G):
    # find neigbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []
        if edge[1] not in neighbours:
            neighbours[edge[1]] = []
        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # finds the hamiltonian circuit
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]
    while len(MatchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break
        while len(neighbours[v]) > 0:
            w = neighbours[v][0]
            remove_edge_from_matchedMST(MatchedMSTree, v, w)
            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]
            i += 1
            EP.insert(i, w)
            v = w
    return EP


def remove_edge_from_matchedMST(MatchedMST, v1, v2):
    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]
    return MatchedMST