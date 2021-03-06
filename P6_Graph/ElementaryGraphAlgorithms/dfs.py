from P6_Graph.directed_graph import Graph, Vertex
from typing import Callable, Any
from unittest import TestCase

class DFSResult:
    def __init__(self):
        self.came_from = {}
        self.discover_times = {}
        self.finish_times = {}

    def __repr__(self):
        return 'came_from: %r, discover_times: %r, finish_times: %r' %\
               (self.came_from, self.discover_times, self.finish_times)

    def __eq__(self, other):
        if not isinstance(other, DFSResult):
            return False
        return (self.came_from == other.came_from and self.discover_times == other.discover_times
                and self.finish_times == other.finish_times)

class TimeCounter:
    def __init__(self):
        self._time = 0

    def next(self):
        self._time += 1
        return self._time


def dfs(graph: Graph, pre_visit_func: Callable[[Any], bool]=None, post_visit_func: Callable[[Any], bool]=None)\
        -> DFSResult:
    """Ex. 22.3-7"""
    if not pre_visit_func:
        def pre_visit_func(_): return True
    if not post_visit_func:
        def post_visit_func(_): return True
    result = DFSResult()
    time = TimeCounter()
    for v in graph.vertex_keys():
        if v not in result.discover_times and not dfs_internal(
                graph, v, pre_visit_func, post_visit_func, result, time):
            break
    return result


def dfs_with_src(graph: Graph, src_key, pre_visit_func: Callable[[Any], bool]=None,
                 post_visit_func: Callable[[Any], bool]=None) -> DFSResult:
    """Ex. 22.3-7"""
    if not pre_visit_func:
        def pre_visit_func(_): return True
    if not post_visit_func:
        def post_visit_func(_): return True
    result = DFSResult()
    dfs_internal(graph, src_key, pre_visit_func, post_visit_func, result, TimeCounter())
    return result


def dfs_internal(graph: Graph, src_key,
                 pre_visit_func: Callable[[Any], bool],
                 post_visit_func: Callable[[Any], bool],
                 result: DFSResult, time: TimeCounter) -> bool:
    if not pre_visit_func(src_key):
        return False
    stack = [(src_key, graph.get_vertex(src_key).successors())]
    result.came_from[src_key] = None
    result.discover_times[src_key] = time.next()
    default_next_item = object()
    while stack:
        cur_key, iter = stack[-1]
        next_item = next(iter, default_next_item)
        if next_item == default_next_item:
            stack.pop(-1)
            result.finish_times[cur_key] = time.next()
            if not post_visit_func(cur_key):
                return False
            continue
        successor_key = next_item[0]
        if successor_key in result.discover_times:
            continue
        if not pre_visit_func(successor_key):
            return False
        result.came_from[successor_key] = cur_key
        result.discover_times[successor_key] = time.next()
        stack.append((successor_key, graph.get_vertex(successor_key).successors()))
    return True


class TestDFS(TestCase):
    def test_dfs(self):
        graph = Graph()
        graph.add_vertex(Vertex('s'))
        graph.add_vertex(Vertex('t'))
        graph.add_vertex(Vertex('u'))
        graph.add_vertex(Vertex('v'))
        graph.add_vertex(Vertex('w'))
        graph.add_vertex(Vertex('x'))
        graph.add_vertex(Vertex('y'))
        graph.add_vertex(Vertex('z'))
        graph.add_edge('z', 'y')
        graph.add_edge('s', 'z')
        graph.add_edge('y', 'x')
        graph.add_edge('x', 'z')
        graph.add_edge('z', 'w')
        graph.add_edge('s', 'w')
        graph.add_edge('v', 's')
        graph.add_edge('t', 'v')
        graph.add_edge('t', 'u')
        graph.add_edge('u', 't')
        graph.add_edge('w', 'x')
        graph.add_edge('v', 'w')
        graph.add_edge('u', 'v')

        pre_visit_array = []
        def pre_visit(v):
            pre_visit_array.append(v)
            return True
        post_visit_array = []
        def post_visit(v):
            post_visit_array.append(v)
            return True

        result = dfs(graph, pre_visit, post_visit)

        expected_result = DFSResult()
        expected_result.discover_times = {'s': 1, 'w': 2, 'x': 3, 'z': 4, 'y': 5, 't': 11, 'u': 12, 'v': 13}
        expected_result.finish_times = {'y': 6, 'z': 7, 'x': 8, 'w': 9, 's': 10, 'v': 14, 'u': 15, 't': 16}
        expected_result.came_from = {'s': None, 'w': 's', 'x': 'w', 'z': 'x', 'y': 'z', 't': None, 'u': 't', 'v': 'u'}
        expected_pre_visit_array = ['s', 'w', 'x', 'z', 'y', 't', 'u', 'v']
        expected_post_visit_array = ['y', 'z', 'x', 'w', 's', 'v', 'u', 't']
        self.assertEqual(expected_result, result)
        self.assertSequenceEqual(expected_pre_visit_array, pre_visit_array)
        self.assertSequenceEqual(expected_post_visit_array, post_visit_array)
