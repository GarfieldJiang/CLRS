from Common.directed_graph import Graph, Vertex
from typing import Any, Tuple
from unittest import TestCase


def _extract_min(open_set: dict) -> Tuple[Any, float]:
    assert open_set
    min_cost = float('inf')
    min_vertex_key = None
    for vertex_key, cost in open_set.items():
        if cost < min_cost:
            min_cost = cost
            min_vertex_key = vertex_key
    open_set.pop(min_vertex_key)
    return min_vertex_key, min_cost


def dijkstra(graph: Graph, srcKey) -> dict:
    open_set = {srcKey: 0}
    closed_set = set()
    came_from = {srcKey: None}
    while open_set:
        u, u_cost = _extract_min(open_set)
        closed_set.add(u)
        for v, w in graph.get_vertex(u).successors():
            if v in closed_set:
                continue
            new_cost = u_cost + w
            if v not in open_set or open_set[v] > new_cost:
                came_from[v] = u
                open_set[v] = new_cost
    return came_from


def reconstruct_path(came_from: dict, srcKey, dstKey):
    path = []
    while dstKey != srcKey:
        path.append(dstKey)
        dstKey = came_from[dstKey] if dstKey in came_from else None
        if not dstKey:
            return []
    path.append(srcKey)
    path.reverse()
    return path


class TestDijkstra(TestCase):
    def test_dijkstra_7_vertex_undirected_graph_with_one_isolated_vertex(self):
        """
        Vertex 7 will be isolated.
        :return:
        """
        graph = Graph()
        vertices = [Vertex(i) for i in range(1, 8)]
        for v in vertices:
            graph.add_vertex(v)
        graph.add_edge(1, 2, 7)
        graph.add_edge(2, 1, 7)
        graph.add_edge(1, 3, 9)
        graph.add_edge(3, 1, 9)
        graph.add_edge(1, 6, 14)
        graph.add_edge(6, 1, 14)
        graph.add_edge(2, 3, 10)
        graph.add_edge(3, 2, 10)
        graph.add_edge(2, 4, 15)
        graph.add_edge(4, 2, 15)
        graph.add_edge(3, 4, 11)
        graph.add_edge(4, 3, 11)
        graph.add_edge(3, 6, 2)
        graph.add_edge(6, 3, 2)
        graph.add_edge(4, 5, 6)
        graph.add_edge(5, 4, 6)
        graph.add_edge(5, 6, 9)
        graph.add_edge(6, 5, 9)

        src = 1
        came_from = dijkstra(graph, src)

        expected_results = {
            1: (1,),
            2: (1, 2),
            3: (1, 3),
            4: (1, 3, 4),
            5: (1, 3, 6, 5),
            6: (1, 3, 6),
            7: (),
        }

        for dst, expected in expected_results.items():
            self.assertSequenceEqual(reconstruct_path(came_from, src, dst), expected)
