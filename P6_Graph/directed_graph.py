from typing import Any
from collections import OrderedDict


class Vertex(object):
    def __init__(self, key):
        assert key is not None
        self._key = key
        self._successors = OrderedDict()

    def _add_successor(self, successor_key, weight: float):
        self._successors[successor_key] = weight

    @property
    def key(self):
        return self._key

    def successors(self):
        for key, weight in self._successors.items():
            yield key, weight

    def has_successor(self, successor_key):
        return successor_key in self._successors.keys()

    def _weight(self, successor_key) -> float:
        if successor_key in self._successors.keys():
            return self._successors[successor_key]
        return float('inf')


class Graph(object):
    def __init__(self):
        self._vertices = OrderedDict()

    def add_vertex(self, v: Vertex):
        assert v
        assert v.key not in self._vertices
        self._vertices[v.key] = v

    def has_vertex(self, key):
        return key in self._vertices

    def get_vertex(self, key):
        return self._vertices[key]

    def vertex_keys(self):
        for v_key in self._vertices.keys(): yield v_key

    def vertices(self):
        for v in self._vertices.values(): yield v

    def has_vertex(self, key):
        return key in self._vertices

    @property
    def vertex_len(self):
        return len(self._vertices)

    def add_edge(self, srcKey, dstKey, weight: float = 0):
        assert srcKey in self._vertices
        assert dstKey in self._vertices
        src = self._vertices[srcKey]
        assert not src.has_successor(dstKey)
        src._add_successor(dstKey, weight)

    def add_2_edges(self, vertexKey1, vertexKey2, weight: float = 0):
        assert vertexKey1 != vertexKey2
        assert vertexKey1 in self._vertices
        assert vertexKey2 in self._vertices
        u = self._vertices[vertexKey1]
        v = self._vertices[vertexKey2]
        assert not u.has_successor(v) and not v.has_successor(u)
        u._add_successor(vertexKey2, weight)
        v._add_successor(vertexKey1, weight)


    def has_edge(self, srcKey: Vertex, dstKey: Vertex):
        assert srcKey in self._vertices
        assert dstKey in self._vertices
        src = self._vertices[srcKey]
        return src.has_successor(dstKey)

    def edge_weight(self, srcKey, dstKey):
        assert srcKey in self._vertices
        assert dstKey in self._vertices
        src = self._vertices[srcKey]
        assert src.has_successor(dstKey)
        return src._weight(dstKey)
