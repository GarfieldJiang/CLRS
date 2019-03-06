from P6_Graph.directed_graph import Graph, Vertex
from unittest import TestCase


def get_transpose(graph: Graph):
    """Ex 22.1-3."""
    tr = Graph()
    for v in graph.vertex_keys():
        tr.add_vertex(Vertex(v))
    for u in graph.vertex_keys():
        for v, weight in graph.get_vertex(u).successors():
            tr.add_edge(v, u, weight)
    return tr


def universal_sink(adj_matrix):
    """Ex 22.11-6."""
    v = len(adj_matrix)
    i, j = 0, 0
    while i < v and j < v:
        if adj_matrix[i][j] == 0:
            j += 1
        else:
            i += 1

    if i == v:
        return -1

    return -1 if (sum(1 for elem in adj_matrix[i] if elem == 0) != v or
                  sum(1 for row in adj_matrix if row[i] == 1) != v - 1) else i


def graph_from_adj_matrix(adj_matrix) -> Graph:
    vertex_count = len(adj_matrix)
    graph = Graph()
    for i in range(vertex_count):
        graph.add_vertex(Vertex(i))
    for i in range(vertex_count):
        for j in range(vertex_count):
            if adj_matrix[i][j]:
                graph.add_edge(i, j)
    return graph


def graph_to_adj_matrix(graph: Graph):
    vertex_count = graph.vertex_len
    adj_matrix = [([0] * vertex_count) for _ in range(vertex_count)]
    for u in graph.vertex_keys():
        for v, _ in graph.get_vertex(u).successors():
            adj_matrix[u][v] = 1
    return adj_matrix


class TestRepresentation(TestCase):
    def test_transpose(self):
        adj_matrix = [
            [1, 1, 1],
            [1, 0, 1],
            [0, 0, 0],
        ]

        expected_tr = [
            [1, 1, 0],
            [1, 0, 0],
            [1, 1, 0],
        ]

        graph = graph_from_adj_matrix(adj_matrix)
        tr = get_transpose(graph)
        tr_adj_matrix = graph_to_adj_matrix(tr)
        self.assertEqual(expected_tr, tr_adj_matrix)

    def test_universal_sink(self):
        cases = (
            [
                [1, 1, 1],
                [1, 0, 0],
                [0, 0, 0],
            ],
            [
                [1, 1, 1],
                [0, 0, 0],
                [1, 1, 1],
            ],
        )

        expected_results = (-1, 1)

        for i in range(len(cases)):
            self.assertEqual(expected_results[i], universal_sink(cases[i]))
