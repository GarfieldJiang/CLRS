from P6_Graph.ElementaryGraphAlgorithms.dfs import dfs
from P6_Graph.ElementaryGraphAlgorithms.representation import get_transpose
from P6_Graph.directed_graph import Graph, Vertex
from collections import deque
from unittest import TestCase
from typing import Sequence


def topological_sort_dfs(graph: Graph) -> list:
    q = deque()

    def post_visit(v_key):
        q.appendleft(v_key)
        return True

    dfs(graph, None, post_visit)
    return list(q)


def count_simple_path(graph: Graph, src_key, dst_key) -> int:
    """Ex 22.4-2. O(V + E) time."""
    sort_result = topological_sort_dfs(graph)
    src_index, dst_index = -1, -1
    for i in range(len(sort_result)):
        if sort_result[i] == src_key:
            src_index = i
        if sort_result[i] == dst_key:
            dst_index = i
    assert src_index >= 0
    assert dst_index >= 0
    if src_index >= dst_index:
        return 0
    counts = [0] * (dst_index - src_index + 1)
    checked_vertices = {}
    for i in range(dst_index - 1, src_index - 1, -1):
        checked_vertices[sort_result[i]] = i
        for v_key, _ in graph.get_vertex(sort_result[i]).successors():
            if v_key == dst_key:
                counts[i] += 1
            elif v_key in checked_vertices:
                counts[i] += counts[checked_vertices[v_key]]
    return counts[0]


def topological_sort_kahn(graph: Graph) -> list:
    """
    Ex 22.4-5. If return list is shorter than graph vertex length, it means the topological sort cannot be performed.
    O(V + E) time.
    """
    in_degrees = {}
    ret = []
    for v_key in graph.vertex_keys():
        in_degrees[v_key] = 0
    for u_key in graph.vertex_keys():
        for v_key, _ in graph.get_vertex(u_key).successors():
            in_degrees[v_key] += 1

    zero_in_degree_set = deque()
    for v_key in graph.vertex_keys():
        if in_degrees[v_key] == 0:
            zero_in_degree_set.append(v_key)

    while zero_in_degree_set:
        u_key = zero_in_degree_set.popleft()
        ret.append(u_key)
        for v_key, _ in list(graph.get_vertex(u_key).successors()):
            graph.remove_edge(u_key, v_key)
            in_degrees[v_key] -= 1
            if in_degrees[v_key] == 0:
                zero_in_degree_set.append(v_key)
    return ret


class TestTopologicalSort(TestCase):
    def test_topological_sort(self):
        cases = []
        cases.append(self._graph_from_figure_22_7())
        cases.append(self._graph_from_figure_22_8())
        methods = (topological_sort_dfs, topological_sort_kahn)
        for method in methods:
            for graph in cases:
                result = method(graph)
                self._check_topological_sort_result(graph, result)
                result_transposed = method(get_transpose(graph))
                result_transposed.reverse()
                self._check_topological_sort_result(graph, result_transposed)

    def test_topological_sort_with_loop(self):
        cases = []
        graph = Graph()
        graph.add_vertex(Vertex(0))
        graph.add_edge(0, 0)
        cases.append(graph)

        graph = self._graph_from_figure_22_8()
        graph.add_edge("v", "p")  # Add an edge to form a loop
        cases.append(graph)

        for graph in cases:
            self.assertLess(len(topological_sort_kahn(graph)), graph.vertex_len)


    def test_count_simple_path(self):
        graph = self._graph_from_figure_22_8()
        self.assertEqual(4, count_simple_path(graph, "p", "v"))

    def _graph_from_figure_22_7(self):
        graph = Graph()
        graph.add_vertex(Vertex("undershorts"))
        graph.add_vertex(Vertex("socks"))
        graph.add_vertex(Vertex("watch"))
        graph.add_vertex(Vertex("pants"))
        graph.add_vertex(Vertex("shoes"))
        graph.add_vertex(Vertex("belt"))
        graph.add_vertex(Vertex("shirt"))
        graph.add_vertex(Vertex("tie"))
        graph.add_vertex(Vertex("jacket"))
        graph.add_edge("undershorts", "pants")
        graph.add_edge("undershorts", "shoes")
        graph.add_edge("socks", "shoes")
        graph.add_edge("pants", "shoes")
        graph.add_edge("pants", "belt")
        graph.add_edge("shirt", "belt")
        graph.add_edge("shirt", "tie")
        graph.add_edge("tie", "jacket")
        graph.add_edge("belt", "jacket")
        return graph

    def _graph_from_figure_22_8(self):
        graph = Graph()
        graph.add_vertex(Vertex("m"))
        graph.add_vertex(Vertex("n"))
        graph.add_vertex(Vertex("o"))
        graph.add_vertex(Vertex("p"))
        graph.add_vertex(Vertex("q"))
        graph.add_vertex(Vertex("r"))
        graph.add_vertex(Vertex("s"))
        graph.add_vertex(Vertex("t"))
        graph.add_vertex(Vertex("u"))
        graph.add_vertex(Vertex("v"))
        graph.add_vertex(Vertex("w"))
        graph.add_vertex(Vertex("x"))
        graph.add_vertex(Vertex("y"))
        graph.add_vertex(Vertex("z"))
        graph.add_edge("m", "q")
        graph.add_edge("m", "r")
        graph.add_edge("m", "x")
        graph.add_edge("n", "o")
        graph.add_edge("n", "q")
        graph.add_edge("n", "u")
        graph.add_edge("o", "r")
        graph.add_edge("o", "s")
        graph.add_edge("o", "v")
        graph.add_edge("p", "o")
        graph.add_edge("p", "s")
        graph.add_edge("p", "z")
        graph.add_edge("q", "t")
        graph.add_edge("r", "u")
        graph.add_edge("r", "y")
        graph.add_edge("s", "r")
        graph.add_edge("u", "t")
        graph.add_edge("v", "w")
        graph.add_edge("v", "x")
        graph.add_edge("w", "z")
        graph.add_edge("y", "v")
        return graph

    def _check_topological_sort_result(self, graph: Graph, result: Sequence):
        # result = list(result)
        self.assertEqual(graph.vertex_len, len(result))
        for i in range(len(result) - 1):
            for j in range(i + 1, len(result)):
                # print('edge "%s" -> "%s" does not exist.' % (result[j], result[i]))
                self.assertFalse(graph.has_edge(result[j], result[i]))
