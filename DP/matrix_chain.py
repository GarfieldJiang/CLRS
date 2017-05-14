import unittest
import sys


def matrix_chain_order_memoized(dims):
    matrix_count = __assert_dims_and_fetch_matrix_count(dims)
    cache = [[None for _ in xrange(0, matrix_count)] for _ in xrange(0, matrix_count)]
    solution = [[None for _ in xrange(0, matrix_count)] for _ in xrange(0, matrix_count)]
    optimal = __matrix_chain_order_memoized_internal(dims, 0, matrix_count - 1, cache, solution)
    return optimal, solution


def __matrix_chain_order_memoized_internal(dims, beg, end, cache, solution):
    count = end - beg + 1
    if cache[beg][end] is not None:
        return cache[beg][end]

    if count == 1:  # one matrix
        cache[beg][end] = 0
        return cache[beg][end]

    optimal = sys.maxint
    new_solution = None

    for i in xrange(beg, end):
        left = __matrix_chain_order_memoized_internal(dims, beg, i, cache, solution)
        right = __matrix_chain_order_memoized_internal(dims, i + 1, end, cache, solution)
        concat = dims[beg] * dims[i + 1] * dims[end + 1]
        res = left + right + concat

        if optimal > res:
            optimal = res
            new_solution = i

    cache[beg][end] = optimal
    solution[beg][end] = new_solution
    return optimal


def matrix_chain_order_bottom_up(dims):
    matrix_count = __assert_dims_and_fetch_matrix_count(dims)

    cache = [[None for _ in xrange(0, matrix_count)] for _ in xrange(0, matrix_count)]
    solution = [[None for _ in xrange(0, matrix_count)] for _ in xrange(0, matrix_count)]

    for end in xrange(0, matrix_count):
        cache[end][end] = 0
        for beg in xrange(end - 1, -1, -1):
            for i in xrange(beg, end):
                val = cache[beg][i] + cache[i + 1][end] + dims[beg] * dims[i + 1] * dims[end + 1]
                if cache[beg][end] is None or cache[beg][end] > val:
                    cache[beg][end] = val
                    solution[beg][end] = i

    return cache[0][matrix_count - 1], solution


def __assert_dims_and_fetch_matrix_count(dims):
    assert dims and len(dims) >= 2

    for dim in dims:
        assert isinstance(dim, int) and dim > 0

    return len(dims) - 1


def gen_solution_txt(solution):
    matrix_count = len(solution)
    return __generate_solution_txt_internal(solution, 0, matrix_count - 1)


def __generate_solution_txt_internal(solution, beg, end):
    if beg == end:
        return 'A_%d' % beg

    i = solution[beg][end]
    left = __generate_solution_txt_internal(solution, beg, i)
    right = __generate_solution_txt_internal(solution, i + 1, end)
    return '(%s * %s)' % (left, right)


class TestMatrixChain(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMatrixChain, self).__init__(*args, **kwargs)

        # Suppose matrices A0, A1, ..., A5 have dimensions:
        # A0: 30 x 35
        # A1: 35 x 15
        # A2: 15 x 5
        # A3: 5 x 10
        # A4: 10 x 20
        # A5: 20 x 25
        self.dims = (30, 35, 15, 5, 10, 20, 25)
        self.res = 15125

    def test_matrix_chain_order_memoized(self):
        res, solution = matrix_chain_order_memoized(self.dims)
        self.assertEqual(self.res, res)
        print gen_solution_txt(solution)

    def test_matrix_chain_order_bottom_up(self):
        res, solution = matrix_chain_order_bottom_up(self.dims)
        self.assertEqual(self.res, res)
        print gen_solution_txt(solution)
