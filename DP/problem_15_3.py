# This Python file uses the following encoding: utf-8
import math
import unittest


def get_shortest_bitonic_path(points):
    """
    Problem 15-3.
    :param points: the points from left to right.
    :return: the length of the optimal path, and an optimal path.
    """

    if not points:
        return 0, ()

    if len(points) == 1:
        return 0, (points[0],)

    n = len(points)
    distances = [[0 for _ in xrange(n)] for _ in xrange(n)]
    for i in xrange(0, n - 1):
        for j in xrange(i + 1, n):
            distances[i][j] = distances[j][i] = __get_euclidean_distance(points[i], points[j])

    lengths = [-1 for _ in xrange(n - 1)]
    second_right_most_l2r = [-1 for _ in xrange(n - 1)]
    right_most_r2l = [-1 for _ in xrange(n - 1)]
    right_most_r2l[0] = 0
    lengths[0] = 2 * distances[0][n - 1]

    # At the end of the following loop for each i:
    # - length[k] (k = 0..i) is the shortest path length made of points[0..i] and points[n - 1], and points[k] as the
    #   right most point of the L2R part.
    # - right_most_r2l[k] (k = 0..i) is the right most point of the R2L part of the shortest path made of points[0..k]
    #   and points[n - 1], and points[k] as the right most point of the L2R part.
    # - second_right_most_l2r[k] (k = 0..i) is the second right most point of the L2R part of the shortest path made of
    #   points[0..k] and points[n - 1], and points[k] as the right msot points of the L2R part.
    for i in xrange(1, n - 1):
        for j in xrange(0, i):
            new_length = lengths[j] + distances[j][i] + distances[i][n - 1] - distances[j][n - 1]
            if lengths[i] < 0 or new_length < lengths[i]:
                lengths[i] = new_length
                second_right_most_l2r[i] = j
                right_most_r2l[i] = i - 1 if j < i - 1 else right_most_r2l[i - 1]
        for j in xrange(0, i - 1):
            lengths[j] += distances[i - 1][i] + distances[i][n - 1] - distances[i - 1][n - 1]
        w = right_most_r2l[i - 1]
        lengths[i - 1] += distances[w][i] + distances[i][n - 1] - distances[w][n - 1]

    # print second_right_most_l2r
    # print right_most_r2l

    l2r_indices = []
    r2l_indices = []

    i = n - 2
    while i > 0:
        j = second_right_most_l2r[i]
        l2r_indices.insert(0, i)

        for k in xrange(i - 1, j, -1):
            r2l_indices.append(k)

        i = j

    path_indices = [0] + l2r_indices + [n - 1] + r2l_indices + [0]
    return lengths[len(lengths) - 1], tuple([points[i] for i in path_indices])


def get_shortest_bitonic_path_naive(points):
    """
    For unit test of Problem 15-3.
    :param points: the points from left to right.
    :return: the length of the optimal path, and an optimal path.
    """
    if not points:
        return 0, ()

    if len(points) == 1:
        return 0, (points[0],)

    if len(points) == 2:
        return __get_euclidean_distance(points[0], points[1]) * 2, (points[0], points[1], points[0])

    n = len(points)
    r2l_flags = [False] * (n - 2)
    shortest_path_l2r_path = []
    shortest_path_r2l_path = []
    shortest_path_len = -1

    true_count = 0
    while true_count < n - 2:
        l2r_path = [0]
        l2r = 0
        r2l_path = [0]
        r2l = 0
        for i in xrange(1, n - 1):
            if not r2l_flags[i - 1]:
                l2r += __get_euclidean_distance(points[i], points[l2r_path[len(l2r_path) - 1]])
                l2r_path.append(i)
            else:
                r2l += __get_euclidean_distance(points[i], points[r2l_path[len(r2l_path) - 1]])
                r2l_path.append(i)

        l2r += __get_euclidean_distance(points[n - 1], points[l2r_path[len(l2r_path) - 1]])
        r2l += __get_euclidean_distance(points[n - 1], points[r2l_path[len(r2l_path) - 1]])

        # print 'l2r', l2r_path, l2r
        # print 'r2l', r2l_path, r2l

        if shortest_path_len < 0 or l2r + r2l < shortest_path_len:
            shortest_path_len = l2r + r2l
            shortest_path_l2r_path = l2r_path
            shortest_path_r2l_path = r2l_path

        carry = True
        true_count = 0
        for i in xrange(n - 2):
            if carry:
                r2l_flags[i] = not r2l_flags[i]
                carry = not r2l_flags[i]
            true_count += 1 if r2l_flags[i] else 0

    path = []
    for index in shortest_path_l2r_path:
        path.append(points[index])
    path.append(points[n - 1])
    for i in xrange(len(shortest_path_r2l_path) - 1, -1, -1):
        path.append(points[shortest_path_r2l_path[i]])
    # print path
    return shortest_path_len, tuple(path)


def __get_euclidean_distance(a, b):
    delta_x = a[0] - b[0]
    delta_y = a[1] - b[1]
    return math.sqrt(delta_x * delta_x + delta_y * delta_y)


class TestProblems(unittest.TestCase):
    def test_get_shortest_bitonic_path(self):
        cases = (
            (),
            ((0, 0),),
            ((0, 0), (1, 1)),
            ((0, 0), (1, -1), (2, 1), (3, 0)),
            ((0, 0), (1, -6), (2, -3), (5, -2), (6, -5), (7, -1), (8, -4)),
            ((0, 0), (1, 1), (2, -1), (3, 1), (4, -1), (5, 0)),
            ((0, 0), (1, 2), (2, 1), (3, 5), (4, 0)),
            ((0, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 5), (6, 0)),
            ((0, 0), (1, 5), (2, 1), (3, 1), (4, 1), (5, 1), (6, 0)),
        )

        for case in cases:
            print "points: ", case
            length, path = get_shortest_bitonic_path(case)
            print "path: ", path
            length_ref, path_ref = get_shortest_bitonic_path_naive(case)
            # print "path ref: ", path_ref
            self.assertAlmostEqual(length, length_ref)
            self.assertEqual(path, path_ref)
