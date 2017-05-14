import unittest
import sys


def get_optimal_bst(p, q):
    """
    \Theta(n^3) method to calculate the expected cost of the optimal BST.
    :param p: key probabilities. p[i] refers to p_{i} in the text.
    :param q: dummny node probabilities. q[i] refers to q{i} in the text.
    :return: the optimal cost and the root matrix for the optimal BST.
    """

    assert p is not None
    assert q is not None
    assert len(p) == len(q)
    n = len(p) - 1
    assert n >= 0

    if n == 0:
        return 1.0, []

    e = [[-1 for _ in xrange(0, n + 1)] for _ in xrange(0, n + 1)]
    root = [[-1 for _ in xrange(0, n)] for _ in xrange(0, n)]

    for i in xrange(1, n + 1):
        e[i][i] = (q[i - 1] + q[i]) * 2 + p[i]
        root[i - 1][i - 1] = i

    for i in xrange(n + 1, 0, -1):
        for j in xrange(i + 1, n + 1):
            w = sum(q[i - 1:j + 1]) + sum(p[i:j + 1])
            min_cost = sys.maxint
            current_root = -1
            for r in xrange(i, j + 1):
                assert (r == i or e[i][r - 1] > 0) and (r == j or e[r + 1][j] > 0)
                e_left = q[i - 1] if r == i else e[i][r - 1]
                e_right = q[j] if r == j else e[r + 1][j]
                e_cost = w + e_left + e_right

                if e_cost < min_cost:
                    min_cost = e_cost
                    current_root = r

            e[i][j] = min_cost
            root[i - 1][j - 1] = current_root

    return e[1][n], root


def __construct_bst(root, i, j):
    if i == j + 1:
        return 'd_%d' % j

    current_root = root[i - 1][j - 1]
    left = __construct_bst(root, i, current_root - 1)
    right = __construct_bst(root, current_root + 1, j)
    return ['k_%d' % current_root, left, right]


# ex 15.5-1
def construct_bst(root):
    """
    :param root: the root matrix.
    :return: the constructed BST.
    """

    assert root is not None
    n = len(root)
    return __construct_bst(root, 1, n)


# ex 15.5-4
def get_optimal_bst_fast(p, q):
    """
    \Theta(n^2) method to calculate the expected cost of the optimal BST. Takes use of Knuth's conlusion that a root
    matrix exists so that root[i][j-1] <= root[i][j] <= root[i+1][j] for all i < j.
    :param p: key probabilities. p[i] refers to p_{i} in the text.
    :param q: dummny node probabilities. q[i] refers to q{i} in the text.
    :return: the optimal cost and the root matrix for the optimal BST.
    """

    assert p is not None
    assert q is not None
    assert len(p) == len(q)
    n = len(p) - 1
    assert n >= 0

    e = [[-1 for _ in xrange(0, n + 1)] for _ in xrange(0, n + 2)]
    w = [[-1 for _ in xrange(0, n + 1)] for _ in xrange(0, n + 2)]
    root = [[-1 for _ in xrange(0, n)] for _ in xrange(0, n)]

    for i in xrange(1, n + 1):
        root[i - 1][i - 1] = i

    for i in xrange(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    # Calculate w matrix first.
    for i in xrange(n + 1, 0, -1):
        for j in xrange(i, n + 1):
            w[i][j] = w[i][j - 1] + p[j] + q[j]

    for i in xrange(1, n + 1):
        e[i][i] = e[i][i - 1] + e[i + 1][i] + w[i][i]

    for j_i_diff in xrange(1, n):
        i = 1
        r = root[0][j_i_diff - 1]
        while i + j_i_diff <= n:
            j = i + j_i_diff
            e_cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
            if e[i][j] < 0 or e_cost < e[i][j]:
                e[i][j] = e_cost
                root[i - 1][j - 1] = r
            if r == root[i][j - 1]:
                i += 1
            else:
                r += 1

    return e[1][n], root


class TestOptimalBinarySearchTree(unittest.TestCase):
    def test_optimal_bst(self):
        for get_optimal_bst_method in [get_optimal_bst, get_optimal_bst_fast]:
            p = (0, .15, .10, .05, .10, .20)
            q = (.05, .10, .05, .05, .05, .10)
            e, root = get_optimal_bst_method(p, q)
            self.assertAlmostEqual(e, 2.75)
            bst = construct_bst(root)
            self.assertTrue(bst == [
                'k_2', ['k_1', 'd_0', 'd_1'], ['k_5', ['k_4', ['k_3', 'd_2', 'd_3'], 'd_4'], 'd_5']
            ] or bst == [
                'k_4', ['k_2', ['k_1', 'd_0', 'd_1'], ['k_3', 'd_2', 'd_3']], ['k_5', 'd_4', 'd_5']
            ])

            p = (0,)
            q = (1,)
            e, root = get_optimal_bst_method(p, q)
            self.assertAlmostEqual(e, 1)
            bst = construct_bst(root)
            self.assertEqual(bst, 'd_0')
