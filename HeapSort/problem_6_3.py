from unittest import TestCase
from collections import namedtuple


def _check_young_properties(young_tableau):
    m = young_tableau.m
    n = young_tableau.n

    for i in xrange(0, m):
        for j in xrange(0, n):
            if i < m - 1 and young_tableau.get(i, j) > young_tableau.get(i + 1, j):
                return False
            if j < n - 1 and young_tableau.get(i, j) > young_tableau.get(i, j + 1):
                return False
    return True


class YoungTableau(object):
    """
    Simple implementation of a Young tableau.
    """
    def __init__(self, m=0, n=0, matrix=None):
        if not matrix:
            self.m = m
            self.n = n
            self.matrix = [[float('inf') for _ in xrange(0, n)] for _ in xrange(0, m)]
            return

        self.m = len(matrix)
        self.n = len(matrix[0])
        self.matrix = [[matrix[i][j] for j in xrange(0, self.n)] for i in xrange(0, self.m)]
        if not _check_young_properties(self):
            raise ValueError('Matrix provided does not comply with the Young tableau properties')

    def get(self, i, j):
        return self.matrix[i][j]

    def extract_min(self):
        """
        O(m + n) time algorithm to extract the minimum value.
        """
        if self.empty():
            ValueError('Young tableau is empty')

        min_val = self.matrix[0][0]
        self.matrix[0][0] = float('inf')
        self._update_young_properties(0, 0)
        return min_val

    def empty(self):
        return self.matrix[0][0] == float('inf')

    def full(self):
        return self.matrix[self.m - 1][self.n - 1] < float('inf')

    def insert(self, val):
        """
        O(m + n) time algorithm to insert a new value.
        :param val: Value to insert.
        """
        if self.full():
            OverflowError('This Young tableau is full.')

        if val == float('inf'):
            ValueError('val must be less than positive infinity')

        i = self.m - 1
        j = self.n - 1
        while val < self._get_upper(i, j) or val < self._get_left(i, j):
            if self._get_left(i, j) < self._get_upper(i, j):
                self.matrix[i][j] = self._get_upper(i, j)
                i -= 1
            else:
                self.matrix[i][j] = self._get_left(i, j)
                j -= 1

        self.matrix[i][j] = val

    def find(self, val):
        """
        O(m + n) time algorithm to find a value. Problem 6-3(f). Why THE HELL cannot I think of it myself?
        :param val: Value to find.
        :return: Indices of the value. If not find, returns -1, -1.
        """
        i = 0
        j = self.n - 1
        while i < self.m and j >= 0:
            if self.matrix[i][j] == val:
                return i, j
            if self.matrix[i][j] > val:
                j -= 1
            else:
                i += 1

        return -1, -1

    def _get_upper(self, i, j):
        return self.matrix[i - 1][j] if i > 0 else float('-inf')

    def _get_lower(self, i, j):
        return self.matrix[i + 1][j] if i < self.m - 1 else float('inf')

    def _get_left(self, i, j):
        return self.matrix[i][j - 1] if j > 0 else float('-inf')

    def _get_right(self, i, j):
        return self.matrix[i][j + 1] if j < self.n - 1 else float('inf')

    def __str__(self):
        return str(self.matrix)

    def _update_young_properties(self, i, j):
        if self._get_lower(i, j) >= self.matrix[i][j] and self._get_right(i, j) >= self.matrix[i][j]:
            return

        if self._get_lower(i, j) < self._get_right(i, j):
            self.matrix[i][j], self.matrix[i + 1][j] = self.matrix[i + 1][j], self.matrix[i][j]
            self._update_young_properties(i + 1, j)
        else:
            self.matrix[i][j], self.matrix[i][j + 1] = self.matrix[i][j + 1], self.matrix[i][j]
            self._update_young_properties(i, j + 1)


class TestYoungTableaux(TestCase):
    def test_basic_operations(self):
        m = 3
        n = 4
        original_lists = (
            [_ for _ in xrange(0, m * n)],
            [_ for _ in xrange(m * n, 0, -1)],
            [1, 3, 1, 4, 1, 5, 2, 3, 2, 0, 2, -1],
        )

        for l in original_lists:
            self.assertEqual(len(l), m * n)

            young_tableau = YoungTableau(m, n)
            for val in l:
                young_tableau.insert(val)
                self.assertTrue(_check_young_properties(young_tableau))

            sorted_list = []
            while not young_tableau.empty():
                sorted_list.append(young_tableau.extract_min())
                self.assertTrue(_check_young_properties(young_tableau))

            self.assertEqual(sorted_list, sorted(l))

    def test_find(self):
        case_class = namedtuple('case', 'desc matrix value possible_indices')
        cases = (
            case_class(desc='empty', matrix=[], value=100, possible_indices=((-1, -1),)),
            case_class(desc='single found', matrix=[[0]], value=0, possible_indices=((0, 0),)),
            case_class(desc='single not found', matrix=[[0]], value=100, possible_indices=((-1, -1),)),
            case_class(desc='3x4 unique found', matrix=(
                (1, 2, 3, 4),
                (5, 6, 7, 8),
                (9, 10, 11, 12),
            ), value=7, possible_indices=((1, 2),)),
            case_class(desc='3x4 unique not found', matrix=(
                (1, 2, 3, 4),
                (5, 6, 7, 8),
                (9, 10, 11, 12),
            ), value=13, possible_indices=((-1, -1),)),
            case_class(desc='3x4 non-unique found', matrix=(
                (1, 2, 3),
                (2, 3, 4),
                (3, 4, 5),
                (4, 5, 6),
            ), value=4, possible_indices=((1, 2), (2, 1), (3, 0))),
        )

        for case in cases:
            index_tuple = YoungTableau(matrix=case.matrix).find(case.value)
            self.assertTrue(index_tuple in case.possible_indices,
                            msg='index %s not found in possible indices %s' % (index_tuple, case.possible_indices))
