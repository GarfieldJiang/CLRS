import math
import unittest


def __get_longest_path_internal(path_nodes, src, dst, i, j):
    k = path_nodes[i - src][j - src - 1]
    if k == j:
        return [i, ]

    return __get_longest_path_internal(path_nodes, src, dst, i, k)\
        + __get_longest_path_internal(path_nodes, src, dst, k, j)


def __get_longest_path(path_nodes, src, dst):
    if path_nodes[0][dst - src - 1] < 0:
        return []

    return __get_longest_path_internal(path_nodes, src, dst, src, dst) + [dst]


def longest_simple_path_directed_acyclic_graph(adj, src, dst):
    """
    Problem 15-1.
    :param adj: adjacent matrix. adj[i][j] can only have value for 0 <= i < j <= n.
    :param src: the source vertex index.
    :param dst: the destination vertex index.
    :return: the length of the longest path or float('nan') is no path exists, and the path itself containing src and
    dst as a tuple.
    """
    assert adj is not None
    n = len(adj)
    if n == 0:
        return float('nan'), ()

    for i in xrange(0, n):
        assert n == len(adj[i])

    if src < 0 or dst >= n or src >= dst:
        return float('nan'), ()

    path_lens = [[float('nan') for _ in xrange(src + 1, dst + 1)] for _ in xrange(src, dst)]
    path_nodes = [[-1 for _ in xrange(src + 1, dst + 1)] for _ in xrange(src, dst)]
    for i in xrange(dst, src - 1, -1):
        for j in xrange(i + 1, dst + 1):
            assert math.isnan(path_lens[i - src][j - src - 1])
            path_lens[i - src][j - src - 1] = adj[i][j]
            if not math.isnan(path_lens[i - src][j - src - 1]):
                path_nodes[i - src][j - src - 1] = j

            if j == i + 1:
                continue

            for k in xrange(i + 1, j):
                pik = path_lens[i - src][k - src - 1]
                pkj = path_lens[k - src][j - src - 1]
                pij = path_lens[i - src][j - src - 1]

                if not math.isnan(pik) and not math.isnan(pkj) and (math.isnan(pij) or pij < pik + pkj):
                    path_lens[i - src][j - src - 1] = pik + pkj
                    path_nodes[i - src][j - src - 1] = k

    return path_lens[0][dst - src - 1], tuple(__get_longest_path(path_nodes, src, dst))


class TestLongestSimplePathOfDirectedAcyclicGraph(unittest.TestCase):
    nan = float("nan")

    def test_empty_graph(self):
        path_len, path = longest_simple_path_directed_acyclic_graph((), 0, 0)
        self.assertTrue(math.isnan(path_len))
        self.assertEqual(path, ())

    def test_simple_graphs(self):
        path_len, path = longest_simple_path_directed_acyclic_graph(((self.nan, ), ), 0, 0)
        self.assertTrue(math.isnan(path_len))
        self.assertEqual(path, ())

        adj = (
            (self.nan, 1, 3),
            (self.nan, self.nan, 1),
            (self.nan, self.nan, self.nan),
        )

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 1)
        self.assertEqual(path_len, 1)
        self.assertEqual(path, (0, 1))

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 1, 2)
        self.assertEqual(path_len, 1)
        self.assertEqual(path, (1, 2))

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 2)
        self.assertEqual(path_len, 3)
        self.assertEqual(path, (0, 2))

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 3)
        self.assertTrue(math.isnan(path_len))
        self.assertEqual(path, ())

        adj = (
            (self.nan, 1, 1),
            (self.nan, self.nan, 1),
            (self.nan, self.nan, self.nan),
        )

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 1)
        self.assertEqual(path_len, 1)
        self.assertEqual(path, (0, 1))

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 1, 2)
        self.assertEqual(path_len, 1)
        self.assertEqual(path, (1, 2))

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 2)
        self.assertEqual(path_len, 2)
        self.assertEqual(path, (0, 1, 2))

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 3)
        self.assertTrue(math.isnan(path_len))
        self.assertEqual(path, ())

    def test_bigger_graph(self):
        adj = (
            (self.nan, 1, 2, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, 3, 4, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, 5, 6, self.nan, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, 7, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, 8, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, 9, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, 10),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, 11, 12, 13),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan),
            (self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan, self.nan),
        )

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 8, 10)
        self.assertTrue(math.isnan(path_len))
        self.assertEqual(path, ())

        path_len, path = longest_simple_path_directed_acyclic_graph(adj, 0, 10)
        self.assertEqual(path_len, 29)
        self.assertEqual(path, (0, 2, 5, 7, 10))

    def test_a_complete_graph(self):
        adj = [[self.nan if i >= j else 1 for j in range(0, 30)] for i in range(0, 30)]

        for i in xrange(0, len(adj)):
            for j in xrange(i + 1, len(adj[0])):
                path_len, path = longest_simple_path_directed_acyclic_graph(adj, i, j)
                self.assertEqual(path_len, j - i)
                self.assertEqual(len(path), j - i + 1)
                for k in xrange(i, j + 1):
                    self.assertEqual(path[k - i], k)
