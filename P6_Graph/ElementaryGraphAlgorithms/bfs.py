from P6_Graph.directed_graph import Graph, Vertex
from typing import Callable, Tuple, Any
from collections import deque
from unittest import TestCase


def bfs(graph: Graph, visit_func: Callable[[Any], bool]=None) -> Tuple[dict, dict]:
    open_set = deque()
    came_from = {}
    depths = {}
    visited = set()   # Gray or black nodes
    if not visit_func:
        def visit_func(_): return True

    for v in graph.vertex_keys():
        if v in visited:
            continue
        _bfs_internal(graph, v, visit_func, open_set, came_from, depths, visited)
    return came_from, depths


def bfs_with_src(graph: Graph, src_key, visit_func: Callable[[Any], bool]=None) -> Tuple[dict, dict]:
    open_set = deque()
    came_from = {}
    depths = {}
    visited = set()   # Gray or black nodes
    if not visit_func:
        def visit_func(_): return True

    _bfs_internal(graph, src_key, visit_func, open_set, came_from, depths, visited)
    return came_from, depths


def _bfs_internal(graph: Graph, src_key, visit_func: Callable[[Any], bool],
                  open_set: deque, came_from: dict, depths: dict, visited: set):
    open_set.appendleft(src_key)
    visited.add(src_key)
    depths[src_key] = 0

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
            depths[v] = depths[u] + 1


def tree_diameter_recur(tree: Graph, root_key) -> int:
    """Ex 22.2-8. Recursive method. Without support of empty tree."""
    return _tree_diameter_recur_internal(tree, root_key, set())[0]


def _tree_diameter_recur_internal(tree: Graph, root_key, parents: set) -> Tuple[int, int]:
    diameter, depth = 0, 0
    root = tree.get_vertex(root_key)
    parents.add(root_key)
    successor_len = 0
    for v_key, _ in root.successors():
        if v_key not in parents:
            successor_len += 1
    if successor_len <= 0:
        # print('root_key=%d, diameter=%d, depth=%d (leaf)' % (root_key, diameter, depth))
        return diameter, depth
    max_sub_diameter, max_sub_depth, second_sub_depth = 0, -1, -1
    for v_key, _ in root.successors():
        if v_key in parents:
            continue
        sub_diameter, sub_depth = _tree_diameter_recur_internal(tree, v_key, parents)
        max_sub_diameter = max(max_sub_diameter, sub_diameter)
        if max_sub_depth < 0:
            max_sub_depth = sub_depth
        elif sub_depth >= max_sub_depth:
            second_sub_depth = max_sub_depth
            max_sub_depth = sub_depth
        elif sub_depth >= second_sub_depth:
            second_sub_depth = sub_depth
    depth = max_sub_depth + 1
    diameter = max(max_sub_depth + 1 if second_sub_depth < 0 else max_sub_depth + second_sub_depth + 2,
                   max_sub_diameter)

    # print('root_key=%d, diameter=%d, depth=%d' % (root_key, diameter, depth))
    return diameter, depth


def tree_diameter_bfs(tree: Graph, root_key) -> int:
    """Ex 22.2-8. Use BFS twice. Without support of empty tree."""
    _, depths = bfs_with_src(tree, root_key)
    max_depth, max_depth_v_key = -1, None
    for v_key, depth in depths.items():
        if depth > max_depth:
            max_depth = depth
            max_depth_v_key = v_key
    if max_depth_v_key is None:
        return 0
    _, depths = bfs_with_src(tree, max_depth_v_key)
    max_depth = -1
    for v_key, depth in depths.items():
        if depth > max_depth:
            max_depth = depth
    assert max_depth >= 0
    return max_depth


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

        came_from = bfs_with_src(graph, 's')[0]
        self.assertDictEqual({
            'v': 'r',
            'r': 's',
            'w': 's',
            't': 'w',
            'x': 'w',
            'y': 'x',
            'u': 't',
        }, came_from)

    def test_tree_diameter(self):
        methods = (tree_diameter_recur, tree_diameter_bfs)
        tree = Graph()
        for i in range(0, 16):
            tree.add_vertex(Vertex(i))
        tree.add_2_edges(0, 1)
        tree.add_2_edges(0, 2)
        tree.add_2_edges(0, 3)
        tree.add_2_edges(1, 4)
        tree.add_2_edges(1, 5)
        tree.add_2_edges(2, 6)
        tree.add_2_edges(3, 7)
        tree.add_2_edges(3, 8)
        tree.add_2_edges(4, 9)
        tree.add_2_edges(5, 10)
        tree.add_2_edges(5, 11)
        tree.add_2_edges(6, 12)
        tree.add_2_edges(6, 13)
        tree.add_2_edges(6, 14)
        tree.add_2_edges(14, 15)
        for tree_diameter_method in methods:
            for root in range(0, 16):
                # print('root: %d' % root)
                self.assertEqual(7, tree_diameter_method(tree, root))