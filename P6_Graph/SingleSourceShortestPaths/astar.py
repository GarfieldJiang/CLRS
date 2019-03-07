from P6_Graph.directed_graph import Graph, Vertex
from typing import Callable, Any
from P6_Graph.SingleSourceShortestPaths.common import extract_min, reconstruct_path, dijkstra_basic_test_case
from unittest import TestCase
from sys import stdout


def astar(graph: Graph, src_key, dst_key, heuristic_func: Callable[[Any], float]=None) -> dict:
    open_set = {src_key: 0}
    closed_set = set()
    came_from = {src_key: None}

    while open_set:
        u, u_cost = extract_min(open_set, heuristic_func)  # Diff from Dijkstra
        closed_set.add(u)

        if u == dst_key:  # Diff from dijkstra
            break

        for v, w in graph.get_vertex(u).successors():
            if v in closed_set:
                continue
            new_cost = u_cost + graph.edge_weight(u, v)
            if v not in open_set or open_set[v] > new_cost:
                open_set[v] = new_cost
                came_from[v] = u
    return came_from


class TestAStar(TestCase):
    def test_astar_as_dijkstra(self):
        graph, src, expected_results = dijkstra_basic_test_case()
        came_from = astar(graph, src, None, None)
        for dst, expected in expected_results.items():
            self.assertSequenceEqual(reconstruct_path(came_from, src, dst), expected)


def terrain_to_graph(terrain):
    graph = Graph()
    if not terrain or not terrain[0]:
        return graph
    h = len(terrain)
    w = len(terrain[0])
    for x in range(0, w):
        for y in range(0, h):
            graph.add_vertex(Vertex((x, y)))

    for x in range(0, w):
        for y in range(0, h):
            if terrain[y][x] < 0:
                continue
            if x - 1 >= 0 and terrain[y][x - 1] >= 0:
                graph.add_edge((x, y), (x - 1, y), terrain[y][x])
            if y - 1 >= 0 and terrain[y - 1][x] >= 0:
                graph.add_edge((x, y), (x, y - 1), terrain[y][x])
            if x + 1 < w and terrain[y][x + 1] >= 0:
                graph.add_edge((x, y), (x + 1, y), terrain[y][x])
            if y + 1 < h and terrain[y + 1][x] >= 0:
                graph.add_edge((x, y), (x, y + 1), terrain[y][x])
    return graph


def calc_cost(graph, came_from, cur_key, costs):
    if cur_key in costs:
        return costs[cur_key]

    if cur_key in came_from:
        costs[cur_key] = calc_cost(graph, came_from, came_from[cur_key], costs) \
                         + graph.edge_weight(came_from[cur_key], cur_key)
    else:
        costs[cur_key] = float('inf')
    return costs[cur_key]


def draw_path(graph, terrain, came_from, src_key, dst_key):
    h = len(terrain)
    w = len(terrain[0])
    costs = {src_key: 0}
    for x in range(0, w):
        for y in range(0, h):
            calc_cost(graph, came_from, (x, y), costs)

    path = reconstruct_path(came_from, src_key, dst_key)

    print('-' * (w * 4 - 1))
    for y in range(0, h):
        for x in range(0, w):
            if (x, y) == src_key:
                stdout.write('\033[1;31m')
            elif (x, y) == dst_key:
                stdout.write('\033[1;32m')
            elif (x, y) in path:
                stdout.write('\033[1;35m')
            if terrain[y][x] < 0:
                stdout.write('###')
            else:
                stdout.write(('%3d' % costs[(x, y)]) if (x, y) in costs and costs[(x, y)] < float('inf') else '   ')
            stdout.write('\033[0;0m ')
        if y != h - 1:
            stdout.write('\n\n')
    stdout.write('\n')
    stdout.flush()
    print('-' * (w * 4 - 1))


def _main():
    terrain = (
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    )

    src = (2, 7)
    dst = (16, 3)

    graph = terrain_to_graph(terrain)

    def h(key):
        return abs(key[0] - dst[0]) + abs(key[1] - dst[1]) if key else 0

    came_from = astar(graph, src, dst, h)
    draw_path(graph, terrain, came_from, src, dst)


if __name__ == '__main__':
    _main()
