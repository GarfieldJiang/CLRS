from P6_Graph.ElementaryGraphAlgorithms.representation import get_transpose
from P6_Graph.ElementaryGraphAlgorithms.dfs import dfs, dfs_internal, DFSResult, TimeCounter
from P6_Graph.directed_graph import Graph, Vertex
from unittest import TestCase
from typing import List


def scc_dfs(graph: Graph) -> List[List]:
    post_visit_array = []

    def post_visit_first_round(_v_key):
        post_visit_array.append(_v_key)
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
        while v_key is not None:
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


class TarjanCache(object):
    def __init__(self):
        self.discover_times = {}
        self.finish_times = {}
        self.low = {}
        self.in_stack = set()
        self.stack = []


def _tarjan_internal(graph: Graph, src_key, sccs: List[List], cache: TarjanCache, time: TimeCounter):
    cache.in_stack.add(src_key)
    cache.stack.append(src_key)
    cache.discover_times[src_key] = cache.low[src_key] = time.next()
    for v_key, _ in graph.get_vertex(src_key).successors():
        if v_key not in cache.discover_times:
            _tarjan_internal(graph, v_key, sccs, cache, time)
            cache.low[src_key] = min(cache.low[src_key], cache.low[v_key])
        elif v_key not in cache.finish_times:
            cache.low[src_key] = min(cache.low[src_key], cache.discover_times[v_key])
    cache.finish_times[src_key] = time.next()

    if cache.low[src_key] == cache.discover_times[src_key]:
        scc = []
        while True:
            v_key = cache.stack.pop()
            cache.in_stack.remove(v_key)
            scc.append(v_key)
            if v_key == src_key:
                break
        sccs.append(scc)


def scc_tarjan(graph: Graph) -> List[List]:
    sccs = []
    cache = TarjanCache()
    time = TimeCounter()
    for v_key in graph.vertex_keys():
        if v_key not in cache.discover_times:
            _tarjan_internal(graph, v_key, sccs, cache, time)
    return sccs


class TestScc(TestCase):
    def test_scc(self):
        graph = self._graph_from_figure_22_9()
        methods = (scc_dfs, scc_tarjan)
        for method in methods:
            result = method(graph)
            expected_result = self._expected_sccs_from_figure_22_9()
            self._check_scc_result(expected_result, result)

    @staticmethod
    def _expected_sccs_from_figure_22_9() -> List[List]:
        return [
            ['a', 'b', 'e'],
            ['c', 'd'],
            ['f', 'g'],
            ['h'],
        ]

    @staticmethod
    def _graph_from_figure_22_9() -> Graph:
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
        result.sort(key=lambda _scc: _scc[0])
        self.assertListEqual(expected_result, result)
