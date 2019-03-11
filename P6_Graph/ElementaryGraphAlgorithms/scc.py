from P6_Graph.ElementaryGraphAlgorithms.representation import get_transpose
from P6_Graph.ElementaryGraphAlgorithms.dfs import dfs, dfs_internal, DFSResult, TimeCounter
from P6_Graph.directed_graph import Graph, Vertex
from unittest import TestCase
from typing import List


def scc_dfs(graph: Graph) -> List[List]:
    post_visit_array = []

    def post_visit_first_round(v_key):
        post_visit_array.append(v_key)
        return True

    dfs(graph, None, post_visit_first_round)

    result = DFSResult()
    time = TimeCounter()
    for v_key in reversed(post_visit_array):
        if v_key not in result.discover_times:
            dfs_internal(get_transpose(graph), v_key, lambda _: True, lambda _: True, result, time)

    return _retrieve_sccs(result)


def _retrieve_sccs(result: DFSResult) -> List[List]:
    sccs: List[List] = []
    tackled_vertices = {}
    for child_key, parent_key in result.came_from.items():
        if child_key in tackled_vertices:
            continue
        newly_tackled_vertices = {child_key}
        scc_index = -1
        v_key = parent_key
        while v_key != None:
            if v_key in tackled_vertices:
                scc_index = tackled_vertices[parent_key]
                break
            newly_tackled_vertices.add(v_key)
            v_key = result.came_from[v_key]
        if scc_index < 0:
            sccs.append(list())
            scc_index = len(sccs) - 1
        l = sccs[scc_index]
        l.extend(newly_tackled_vertices)
        for v_key in newly_tackled_vertices:
            tackled_vertices[v_key] = scc_index
    return sccs


class TestScc(TestCase):
    def test_scc_dfs(self):
        graph = self._graph_from_figure_22_9()
        result = scc_dfs(graph)
        expected_result = self._expected_sccs_from_figure_22_9()
        self._check_scc_result(expected_result, result)


    def _expected_sccs_from_figure_22_9(self) -> List[List]:
        return [
            ['a', 'b', 'e'],
            ['c', 'd'],
            ['f', 'g'],
            ['h'],
        ]

    def _graph_from_figure_22_9(self) -> Graph:
        graph = Graph()
        graph.add_vertex(Vertex('a'))
        graph.add_vertex(Vertex('b'))
        graph.add_vertex(Vertex('c'))
        graph.add_vertex(Vertex('d'))
        graph.add_vertex(Vertex('e'))
        graph.add_vertex(Vertex('f'))
        graph.add_vertex(Vertex('g'))
        graph.add_vertex(Vertex('h'))
        graph.add_edge('a', 'b')
        graph.add_edge('b', 'c')
        graph.add_edge('b', 'e')
        graph.add_edge('b', 'f')
        graph.add_edge('c', 'd')
        graph.add_edge('c', 'g')
        graph.add_edge('d', 'c')
        graph.add_edge('d', 'h')
        graph.add_edge('e', 'a')
        graph.add_edge('e', 'f')
        graph.add_edge('f', 'g')
        graph.add_edge('g', 'f')
        graph.add_edge('g', 'h')
        graph.add_edge('h', 'h')
        return graph

    def _check_scc_result(self, expected_result, result):
        self.assertEqual(len(expected_result), len(result))
        for scc in result:
            scc.sort()
        result.sort(key=lambda scc: scc[0])
        self.assertListEqual(expected_result, result)
