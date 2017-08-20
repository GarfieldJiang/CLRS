from unittest import TestCase


class YoungTableu(object):
    """
    Simple implementation of a Young tableu
    """
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.matrix = [[float('inf') for _ in xrange(0, n)] for _ in range(0, m)]

    def get(self, i, j):
        return self.matrix[i][j]

    def extract_min(self):
        """
        O(m + n) time algorithm to extract the minimum value.
        """
        if self.empty():
            ValueError('Young tableus is empty')

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
        :param val:
        :return:
        """
        if self.full():
            OverflowError('This Young tableu is full.')

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


def _check_young_properties(young_tableu):
    m = young_tableu.m
    n = young_tableu.n

    for i in xrange(0, m):
        for j in xrange(0, n):
            if i < m - 1 and young_tableu.get(i, j) > young_tableu.get(i + 1, j):
                return False
            if j < n - 1 and young_tableu.get(i, j) > young_tableu.get(i, j + 1):
                return False
    return True


class TestYoungTableus(TestCase):
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

            young_tableu = YoungTableu(m, n)
            for val in l:
                young_tableu.insert(val)
                self.assertTrue(_check_young_properties(young_tableu))

            sorted_list = []
            while not young_tableu.empty():
                sorted_list.append(young_tableu.extract_min())
                self.assertTrue(_check_young_properties(young_tableu))

            self.assertEqual(sorted_list, sorted(l))
