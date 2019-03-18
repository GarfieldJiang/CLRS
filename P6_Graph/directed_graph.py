from P3_DataStructures.RBTree.sorted_map import SortedMap

class Vertex(object):
    def __init__(self, key):
        assert key is not None
        self._key = key
        self._successors = SortedMap()

    def add_successor(self, successor_key, weight: float):
        assert successor_key not in self._successors
        self._successors[successor_key] = weight

    def remove_successor(self, successor_key):
        assert successor_key in self._successors
        self._successors.pop(successor_key)

    @property
    def key(self):
        return self._key

    def successors(self):
        for key, weight in self._successors.items():
            yield key, weight

    def has_successor(self, successor_key):
        return successor_key in self._successors.keys()

    def weight(self, successor_key) -> float:
        if successor_key in self._successors.keys():
            return self._successors[successor_key]
        return float('inf')

    @property
    def successor_len(self):
        return len(self._successors)


class Graph(object):
    def __init__(self):
        self._vertices = SortedMap()

    def add_vertex(self, v: Vertex):
        assert v
        assert v.key not in self._vertices
        self._vertices[v.key] = v

    def has_vertex(self, key):
        return key in self._vertices

    def get_vertex(self, key) -> Vertex:
        return self._vertices[key]

    def vertex_keys(self):
        for v_key in self._vertices.keys():
            yield v_key

    def vertices(self):
        for v in self._vertices.values():
            yield v


    @property
    def vertex_len(self):
        return len(self._vertices)

    def add_edge(self, src_key, dst_key, weight: float = 0):
        assert src_key in self._vertices
        assert dst_key in self._vertices
        src = self._vertices[src_key]
        assert not src.has_successor(dst_key)
        src.add_successor(dst_key, weight)

    def remove_edge(self, src_key, dst_key):
        assert self.has_edge(src_key, dst_key)
        src: Vertex = self._vertices[src_key]
        src.remove_successor(dst_key)

    def add_2_edges(self, vert_key1, vert_key2, weight: float = 0):
        assert vert_key1 != vert_key2
        assert vert_key1 in self._vertices
        assert vert_key2 in self._vertices
        u = self._vertices[vert_key1]
        v = self._vertices[vert_key2]
        assert not u.has_successor(v) and not v.has_successor(u)
        u.add_successor(vert_key2, weight)
        v.add_successor(vert_key1, weight)

    def has_edge(self, src_key: Vertex, dst_key: Vertex):
        assert src_key in self._vertices
        assert dst_key in self._vertices
        src = self._vertices[src_key]
        return src.has_successor(dst_key)

    def edge_weight(self, src_key, dst_key):
        assert src_key in self._vertices
        assert dst_key in self._vertices
        src = self._vertices[src_key]
        assert src.has_successor(dst_key)
        return src.weight(dst_key)
