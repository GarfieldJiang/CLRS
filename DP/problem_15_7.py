import unittest


PROBABILITY_PRECISION = 15


class AdjMatrixElem(object):
    """
    Class whose instance denotes an edge of a directed graph.
    """
    def __init__(self, label_id, probability):
        """
        Initalizer.
        :param label_id: The id that the current edge is labeled with.
        :param probability: The probability of the edge. The sum of the probabilities of all outgoing edges of a node
        should be equal to 1.
        """
        assert isinstance(label_id, int) and label_id > 0, "label_id must be a positive integer."
        assert 0.0 < probability <= 1.0, "probability must be a number in the interval (0, 1]"
        self.label_id = label_id
        self.probability = probability


NO_SUCH_PATH = ()


def viterbi(adj_matrix, label_sequence, starting_vertex):
    """
    DP algorithm to calculate the most probable path starting at starting_vertex and labeled with label_sequence in a
    graph represented by adj_matrix. Running time is O(n * n * k) and space is O(n * k)
    :param adj_matrix: The adjacent matrix of the given directed graph, whose element is AdjMatrixElem.
    :param label_sequence: The sequence labeling the desired path.
    :param starting_vertex: The starting vertex of the desired path.
    :return: The probability of the most probable path and the path itself.
    """

    assert adj_matrix, "adj_matrix is None or empty."
    n = len(adj_matrix)  # vertex count.
    for row in adj_matrix:
        assert len(row) == n, "adj_matrix is not square."

    assert 0 <= starting_vertex <= n - 1, "starting_vertex out of range."

    assert label_sequence, "label_sequence is None or empty."
    k = len(label_sequence)
    for l in label_sequence:
        assert isinstance(l, int) and l > 0, "label ids must be positive integers."

    p = [[0 for _ in xrange(0, k)] for _ in xrange(0, n)]
    for j in xrange(k - 1, -1, -1):
        for beg in xrange(0, n):
            for end in xrange(0, n):
                if not adj_matrix[beg][end]:  # No edge from i to r.
                    continue

                assert isinstance(adj_matrix[beg][end], AdjMatrixElem),\
                    "adj_matrix[%d][%r] is not an AdjMatrixElem" % (beg, end)
                elem = adj_matrix[beg][end]
                if elem.label_id != label_sequence[j]:
                    continue

                later_prob = 1 if j == k - 1 else p[end][j + 1]
                if elem.probability * later_prob > p[beg][j]:
                    p[beg][j] = elem.probability * later_prob

    if round(p[starting_vertex][0] - 0.0, PROBABILITY_PRECISION) == 0:
        return 0, NO_SUCH_PATH

    path = [starting_vertex]
    for j in xrange(0, k):
        beg = path[j]
        for end in xrange(0, n):
            later_prob = 1 if j == k - 1 else p[end][j + 1]
            if adj_matrix[beg][end] and adj_matrix[beg][end].label_id == label_sequence[j]\
                    and round(p[beg][j] - adj_matrix[beg][end].probability * later_prob, PROBABILITY_PRECISION) == 0:
                path.append(end)
                break

    return p[starting_vertex][0], tuple(path)


class TestViterbiAlgorithm(unittest.TestCase):
    def test_viterbi(self):
        cases = (
            (
                "Single node, no edge",
                ((None,),),
                (1, 2, 3, 4, 5, 6, 7),
                0, 0, NO_SUCH_PATH
            ),
            (
                "Single node, one edge, simple cycle path",
                ((AdjMatrixElem(10, 1),),),
                (10,),
                0, 1, (0, 0)
            ),
            (
                "Single node, one edge, no path",
                ((AdjMatrixElem(10, 1),),),
                (10, 9),
                0, 0, NO_SUCH_PATH
            ),
            (
                "2 nodes, unique path, #0",
                (
                    (AdjMatrixElem(1, 0.1), AdjMatrixElem(2, 0.9)),
                    (AdjMatrixElem(2, 0.9), AdjMatrixElem(1, 0.1)),
                ),
                (1, 2),
                0, 0.09, (0, 0, 1)
            ),
            (
                "2 nodes, unique path, #1",
                (
                    (AdjMatrixElem(1, 0.1), AdjMatrixElem(2, 0.9)),
                    (AdjMatrixElem(2, 0.9), AdjMatrixElem(1, 0.1)),
                ),
                (2, 1),
                0, 0.09, (0, 1, 1)
            ),
            (
                "2 nodes, 2 paths",
                (
                    (AdjMatrixElem(10, 0.1), AdjMatrixElem(10, 0.9)),
                    (AdjMatrixElem(20, 0.9), AdjMatrixElem(20, 0.1)),
                ),
                (20, 10),
                1, 0.81, (1, 0, 1)
            ),
            (
                "2 nodes, no path",
                (
                    (AdjMatrixElem(10, 0.1), AdjMatrixElem(10, 0.9)),
                    (AdjMatrixElem(20, 0.9), None),
                ),
                (10, 30),
                0, 0, NO_SUCH_PATH
            ),
            (
                "4 nodes, 2 possible paths",
                (
                    (None, None, None, AdjMatrixElem(100, 1)),
                    (AdjMatrixElem(2, 0.01), None, None, AdjMatrixElem(100, 0.99)),
                    (AdjMatrixElem(2, 0.1), AdjMatrixElem(1, 0.8), AdjMatrixElem(1, 0.1), None),
                    (AdjMatrixElem(100, 0.25),) * 4,
                ),
                (1, 2),
                2, 0.01, (2, 2, 0)
            ),
            (
                "5 nodes, 3 possible paths",
                (
                    (None, AdjMatrixElem(3, 0.5), AdjMatrixElem(3, 0.5), None, None),
                    (None, AdjMatrixElem(2, 0.2), AdjMatrixElem(2, 0.2), AdjMatrixElem(1, 0.6), None),
                    (None, AdjMatrixElem(2, 0.4), AdjMatrixElem(2, 0.1), AdjMatrixElem(1, 0.5), None),
                    (None, None, None, None, AdjMatrixElem(4, 1)),
                    (None, None, None, None, AdjMatrixElem(4, 1)),
                ),
                (3, 2, 1),
                0, 0.12, (0, 2, 1, 3)
            ),
        )
        for desc, adj_matrix, label_sequence, starting_vertex, expected_probability, expected_path in cases:
            probability, path = viterbi(adj_matrix, label_sequence, starting_vertex)
            self.assertAlmostEqual(probability, expected_probability, places=PROBABILITY_PRECISION,
                                   msg="%s, probability %e != %e" % (desc, probability, expected_probability))
            self.assertEqual(path, expected_path, msg="%s, path %s != %s" % (desc, path, expected_path))
