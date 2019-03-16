from P6_Graph.directed_graph import Graph, Vertex
from typing import Tuple
from unittest import TestCase


def euler_tour_undirected(graph: Graph) -> list:
    ret = []
    if graph.vertex_len == 0:
        return ret
    for v_key in graph.vertex_keys():
        ret.append(v_key)
        break
    ret, _ = _euler(graph, ret, 0)
    return ret


def _euler(graph: Graph, path: list, src_index: int) -> Tuple[list, int]:
    src_key = path[src_index]
    src = graph.get_vertex(src_key)
    u = src
    sub_path = [src_key]
    while u.successor_len > 0:
        v = None
        for v_key, _ in u.successors():
            v = graph.get_vertex(v_key)
            break
        graph.remove_edge(u.key, v.key)
        graph.remove_edge(v.key, u.key)
        sub_path.append(v.key)
        u = v
    i = 1
    while i < len(sub_path):
        sub_path, delta_len = _euler(graph, sub_path, i)
        i += delta_len

    path = path[0:src_index] + sub_path + path[src_index + 1:]
    return path, len(sub_path)


class TestEuler(TestCase):
    def test_euler_undirected(self):
        graph = Graph()
        for i in range(8):
            graph.add_vertex(Vertex(i))
        graph.add_2_edges(0, 1)
        graph.add_2_edges(1, 2)
        graph.add_2_edges(0, 3)
        graph.add_2_edges(1, 3)
        graph.add_2_edges(1, 4)
        graph.add_2_edges(2, 4)
        graph.add_2_edges(3, 5)
        graph.add_2_edges(3, 6)
        graph.add_2_edges(4, 6)
        graph.add_2_edges(4, 7)
        graph.add_2_edges(5, 6)
        graph.add_2_edges(6, 7)
        self.assertSequenceEqual([0, 1, 2, 4, 6, 3, 5, 6, 7, 4, 1, 3, 0], euler_tour_undirected(graph))

        graph = Graph()
        for i in range(6):
            graph.add_vertex(Vertex(i))
        graph.add_2_edges(0, 1)
        graph.add_2_edges(0, 2)
        graph.add_2_edges(0, 3)
        graph.add_2_edges(0, 4)
        graph.add_2_edges(1, 2)
        graph.add_2_edges(1, 3)
        graph.add_2_edges(1, 4)
        graph.add_2_edges(2, 3)
        graph.add_2_edges(3, 4)
        graph.add_2_edges(2, 5)
        graph.add_2_edges(4, 5)
        self.assertSequenceEqual([0, 1, 2, 3, 4, 5, 2, 0, 3, 1, 4, 0], euler_tour_undirected(graph))

    def test_mohammed_scimitars(self):
        graph = Graph()
        for i in range(11):
            graph.add_vertex(Vertex(i))
        for edge in (
                (0, 1), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (3, 5), (3, 6), (4, 5), (4, 8),
                (5, 6), (5, 8), (6, 7), (6, 10), (7, 8), (7, 9), (7, 10), (8, 9)):
            graph.add_2_edges(edge[0], edge[1])
        self.assertSequenceEqual([0, 1, 2, 3, 5, 4, 8, 7, 6, 10, 7, 9, 8, 5, 6, 3, 1, 4, 0], euler_tour_undirected(graph))
