from typing import Tuple, Any, Callable
from P6_Graph.directed_graph import Graph, Vertex


def extract_min(open_set: dict, heuristic_func: Callable[[Any], float]=None) -> Tuple[Any, float]:
    """
    Viewing open_set as a priority queue, this function retrieves the item with the minimum cost.
    :param open_set:
    :param heuristic_func:
    :return:
    """
    assert open_set
    if not heuristic_func:
        def heuristic_func(_): return 0
    min_cost = float('inf')
    min_vertex_key = None
    for vertex_key, cost in open_set.items():
        if cost + heuristic_func(vertex_key) < min_cost + heuristic_func(min_vertex_key):
            min_cost = cost
            min_vertex_key = vertex_key
    open_set.pop(min_vertex_key)
    return min_vertex_key, min_cost


def reconstruct_path(came_from: dict, src_key, dst_key) -> list:
    """
    Reconstruct path from the came_from dictionary.
    :param came_from:
    :param src_key:
    :param dst_key:
    :return:
    """
    path: list = []
    while dst_key != src_key:
        path.append(dst_key)
        dst_key = came_from[dst_key] if dst_key in came_from else None
        if not dst_key:
            return []
    path.append(src_key)
    path.reverse()
    return path


def dijkstra_basic_test_case():
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

    expected_results = {
        1: (1,),
        2: (1, 2),
        3: (1, 3),
        4: (1, 3, 4),
        5: (1, 3, 6, 5),
        6: (1, 3, 6),
        7: (),
    }
    return graph, src, expected_results
