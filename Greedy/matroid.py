from unittest import TestCase
from collections import namedtuple
from HeapSort.heap_sort import heap_sort
from queue import Queue


class WeightedEdge(object):
    def __init__(self, vertex_a, vertex_b, standard_weight):
        assert vertex_a < vertex_b
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b
        self.standard_weight = standard_weight


def _check_connectivity(adj_matrix, vertex_a, vertex_b, vertex_count, edge_count_limit):
    """
    A naive BFS implementation to check the connectivity between two vertices in a undirected graph. If the input graph
    is G = (V, E), then the running time is O(|V| |E|).
    :param adj_matrix: the adjacent matrix of the input graph.
    :param vertex_a: input vertex index.
    :param vertex_b: input vertex index.
    :param vertex_count: how many vertices the input graph has.
    :param edge_count_limit: how many edges at most the input graph has.
    :return: whether vertex_a and vertex_b are connected.
    """
    visited = set()
    q = Queue(maxsize=edge_count_limit)
    q.put(vertex_a)
    while not q.empty():
        v = q.get()
        visited.add(v)
        for i in range(0, vertex_count):
            if i in visited:
                continue
            if adj_matrix[v][i]:
                if i == vertex_b:
                    return True
                q.put(i)

    return False


def minimum_spanning_tree(adj_matrix):
    """
    A MST construction algorithm based on the concept of the matroid. Running time is O(|V|^2 + |E| log |E| + |V| |E|^2)
    if the input graph is G = (V, E).
    :param adj_matrix: the weighted adjacent matrix of the input graph.
    :return: the MST edges.
    """
    if not adj_matrix or len(adj_matrix) == 1:
        return ()

    vertex_count = len(adj_matrix)
    weighted_edges = []
    for i in range(0, vertex_count):
        for j in range(0, i + 1):
            if adj_matrix[i][j] >= 0:
                weighted_edges.append(WeightedEdge(j, i, adj_matrix[i][j]))

    heap_sort(weighted_edges, key=lambda e: e.standard_weight)
    edge_count = len(weighted_edges)
    max_standard_weight = weighted_edges[edge_count - 1].standard_weight
    for edge in weighted_edges:
        edge.new_weight = max_standard_weight + 1 - edge.standard_weight

    tree_edges = []
    tree_edges_matrix = [[0 for _ in range(0, vertex_count)] for _ in range(0, vertex_count)]

    for i in range(0, edge_count):
        edge = weighted_edges[i]
        if not _check_connectivity(tree_edges_matrix, edge.vertex_a, edge.vertex_b, vertex_count, edge_count):
            tree_edges.append((edge.vertex_a, edge.vertex_b))
            tree_edges_matrix[edge.vertex_a][edge.vertex_b] = 1
            tree_edges_matrix[edge.vertex_b][edge.vertex_a] = 1

    return tuple(tree_edges)


class TestMatroid(TestCase):
    def test_minimum_spanning_tree(self):
        case_class = namedtuple('Case', 'desc adj_matrix msts')
        cases = (
            case_class(desc='Empty', adj_matrix=(), msts=()),
            case_class(desc='Single node', adj_matrix=((-1,),), msts=()),
            case_class(desc='Two nodes connected', adj_matrix=(
                (-1,),
                (10, -1),
            ), msts=(
                {(0, 1)},
            )),
            case_class(desc='5 nodes complete #0', adj_matrix=(
                (-1,),
                (3, -1),
                (4, 3, -1),
                (10, 4, 3, -1),
                (10, 10, 4, 3, -1),
            ), msts=(
                {(0, 1), (1, 2), (2, 3), (3, 4)},
            )),
            case_class(desc='5 nodes complete #1', adj_matrix=(
                (-1,),
                (10, -1),
                (3, 3, -1),
                (10, 10, 10, -1),
                (10, 3, 10, 3, -1),
            ), msts=(
                {(0, 2), (1, 2), (1, 4), (3, 4)},
            )),
            case_class(desc='5 nodes incomplete', adj_matrix=(
                (-1,),
                (3, -1),
                (-1, 6, -1),
                (-1, -1, 4, -1),
                (1, 2, 3, 5, -1),
            ), msts=(
                {(0, 4), (1, 4), (2, 4), (2, 3)},
            )),
        )

        for case in cases:
            mst = minimum_spanning_tree(case.adj_matrix)
            if (not mst) and case.msts:
                self.fail('%s, MST should not be empty' % case.desc)
            if (not mst) and not case.msts:
                continue

            self.assertTrue(set(mst) in case.msts, msg='%s, unexpected result %s' % (case.desc, mst))


