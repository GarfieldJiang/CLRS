import unittest
from typing import List, Tuple
from OrderStatistics.min_max import min_max
from collections import namedtuple


def _cumulative_counts(array: List[int], _min: int, _max: int):
    counter_len = _max - _min + 1
    counters = [0] * counter_len
    for v in array:
        counters[v - _min] += 1
    for i in range(1, counter_len):
        counters[i] += counters[i - 1]
    return counters


def counting_sort(array: List[int]):
    """
    Counting sort. Running time is \Theta(n + k) and space is \Theta(k) where n = len(array) and k is the
    range of the input values.
    :param array: Input array.
    :return: Sorted version of the array.
    """
    assert array is not None
    n = len(array)
    if n == 0:
        return []
    ret = [None] * n
    _min, _max = min_max(array, 0, n)
    counters = _cumulative_counts(array, _min, _max)
    for j in range(n - 1, -1, -1):
        counters[array[j] - _min] -= 1
        ret[counters[array[j] - _min]] = array[j]
    return ret


def query_count_in_range(array: List[int], queries: Tuple[(int, int)]):
    """
    Ex 8.2-4.
    :param array: Input array.
    :param queries: Range queries. For each query, the first element is the lower bound while the second the upper.
    :return: Count in range.
    """
    assert array is not None
    assert queries is not None
    n = len(array)
    qc = len(queries)
    if n == 0:
        return [0] * qc
    _min, _max = min_max(array, 0, n)
    counters = _cumulative_counts(array, _min, _max)

    ret = [None] * qc
    for i in range(qc):
        lo, hi = queries[i][0], queries[i][1]
        if lo > hi:
            ret[i] = 0
        else:
            lo = _min if lo < _min else lo
            hi = _max if hi > _max else hi
            ret[i] = counters[hi - _min] - (0 if lo == _min else counters[lo - _min - 1])
    return ret


class TestCountingSort(unittest.TestCase):
    def test_counting_sort(self):
        case_class = namedtuple('case_class', 'array sorted_array')
        cases = (
            case_class(array=[], sorted_array=[]),
            case_class(array=[1], sorted_array=[1]),
            case_class(array=[1, 3, 7, 5, 3, 5, 1, 1, 4], sorted_array=[1, 1, 1, 3, 3, 4, 5, 5, 7]),
        )
        for case in cases:
            self.assertEqual(case.sorted_array, counting_sort(case.array))

    def test_query_count_in_range(self):
        case_class = namedtuple('case_class', 'array queries expected_res')
        cases = (
            case_class(array=(), queries=((1, 2), (3, 4)), expected_res=[0, 0]),
            case_class(array=(6, 4, 2, 1, 2, 3, 4, 5, 7, 2, 1),
                       queries=((0, 3), (1, 5), (5, 8), (4, 3)), expected_res=[6, 9, 3, 0]),
        )
        for case in cases:
            self.assertEqual(case.expected_res, query_count_in_range(case.array, case.queries))
