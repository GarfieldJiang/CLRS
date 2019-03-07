from P6_Graph.SingleSourceShortestPaths.common import extract_min, reconstruct_path, dijkstra_basic_test_case
from P6_Graph.directed_graph import Graph
from unittest import TestCase


def dijkstra(graph: Graph, src_key) -> dict:
    open_set = {src_key: 0}
    closed_set = set()
    came_from = {src_key: None}
    while open_set:
        u, u_cost = extract_min(open_set)
        closed_set.add(u)
        for v, w in graph.get_vertex(u).successors():
            if v in closed_set:
                continue
            new_cost = u_cost + w
            if v not in open_set or open_set[v] > new_cost:
                came_from[v] = u
                open_set[v] = new_cost
    return came_from


class TestDijkstra(TestCase):
    def test_dijkstra_basic(self):
        graph, src, expected_results = dijkstra_basic_test_case()
        came_from = dijkstra(graph, src)
        for dst, expected in expected_results.items():
            self.assertSequenceEqual(reconstruct_path(came_from, src, dst), expected)
