from P6_Graph.directed_graph import Graph, Vertex
from typing import Callable, Tuple
from collections import deque
from unittest import TestCase


def bfs(graph: Graph, visit_func: Callable[[Vertex], bool]=None) -> dict:
    open_set = deque()
    came_from = {}
    visited = set()   # Gray or black nodes
    if not visit_func:
        def visit_func(_): return True

    for v in graph.vertex_keys():
        if v in visited:
            continue
        _bfs_internal(graph, v, visit_func, open_set, came_from, visited)
    return came_from


def bfs_with_src(graph: Graph, src_key, visit_func: Callable[[Vertex], bool]=None) -> dict:
    open_set = deque()
    came_from = {}
    visited = set()   # Gray or black nodes
    if not visit_func:
        def visit_func(_): return True

    _bfs_internal(graph, src_key, visit_func, open_set, came_from, visited)
    return came_from


def _bfs_internal(graph: Graph, src_key, visit_func: Callable[[Vertex], bool],
                  open_set: deque, came_from: dict, visited: set):
    open_set.appendleft(src_key)
    visited.add(src_key)

    while open_set:
        u = open_set.pop()
        if not visit_func(u):
            break
        for v, _ in graph.get_vertex(u).successors():
            if v in visited:
                continue
            came_from[v] = u
            open_set.appendleft(v)
            visited.add(v)


class TestBFS(TestCase):
    def test_bfs(self):
        # Figure 22-3
        graph = Graph()
        graph.add_vertex(Vertex('r'))
        graph.add_vertex(Vertex('s'))
        graph.add_vertex(Vertex('t'))
        graph.add_vertex(Vertex('u'))
        graph.add_vertex(Vertex('v'))
        graph.add_vertex(Vertex('w'))
        graph.add_vertex(Vertex('x'))
        graph.add_vertex(Vertex('y'))
        graph.add_2_edges('r', 's')
        graph.add_2_edges('r', 'v')
        graph.add_2_edges('s', 'w')
        graph.add_2_edges('t', 'u')
        graph.add_2_edges('t', 'w')
        graph.add_2_edges('t', 'x')
        graph.add_2_edges('u', 'x')
        graph.add_2_edges('u', 'y')
        graph.add_2_edges('w', 'x')
        graph.add_2_edges('x', 'y')

        came_from = bfs_with_src(graph, 's')
        self.assertDictEqual({
            'v': 'r',
            'r': 's',
            'w': 's',
            't': 'w',
            'x': 'w',
            'y': 'x',
            'u': 't',
        }, came_from)
