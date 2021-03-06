import unittest
from typing import List, Tuple, Callable, TypeVar
from P2_Sorting.OrderStatistics.min_max import min_max
from collections import namedtuple
from Common.common import default_key


T = TypeVar('T')


def _cumulative_counts(array: List[T], _min: int, _max: int, key: Callable[[T], int]=None):
    key = key or default_key
    counter_len = _max - _min + 1
    counters = [0] * counter_len
    for v in array:
        counters[key(v) - _min] += 1
    for i in range(1, counter_len):
        counters[i] += counters[i - 1]
    return counters


def counting_sort(array: List[T], key: Callable[[T], int]=None):
    """
    Counting sort. Running time is \Theta(n + k) and space is \Theta(n) where n = len(array) and k is the
    range of the input values. Stable.
    :param array: Input array.
    :param key: Key getter.
    :return: Sorted version of the array.
    """
    assert array is not None
    n = len(array)
    if n == 0:
        return []
    ret = [None] * n
    key = key or default_key
    _min, _max = min_max(array, 0, n, key)
    _min, _max = key(_min), key(_max)
    counters = _cumulative_counts(array, _min, _max, key)
    for j in range(n - 1, -1, -1):
        k = key(array[j])
        counters[k - _min] -= 1
        ret[counters[k - _min]] = array[j]
    return ret


def counting_sort_in_place(array: List[T], key: Callable[[T], int]=None):
    """
    Problem 8-2(e) Counting sort 'in place'. Running time is \Theta(n + k) and space is \Theta(k) where n = len(array)
    and k is the range of the input values. Not stable.
    :param array: Input array.
    :param key: Key getter.
    :return:
    """
    assert array is not None
    n = len(array)
    if n == 0:
        return []
    ret = [None] * n
    key = key or default_key
    _min, _max = min_max(array, 0, n, key)
    _min, _max = key(_min), key(_max)
    counters = _cumulative_counts(array, _min, _max, key)
    counters2 = list(counters)
    j = n - 1
    current_key = _max
    while True:
        # Put element to right place, swap out another element, until its key is equal to current key.
        elem = array[j]
        k = key(elem)
        while k != current_key:
            counters[k - _min] -= 1
            index = counters[k - _min]
            elem, array[index] = array[index], elem
            k = key(elem)
        counters[k - _min] -= 1
        array[counters[k - _min]] = elem
        j -= 1

        # Skip positions that have already got the right values.
        while current_key == _min and j < 0 or current_key != _min and j < counters2[current_key - _min - 1]:
            if current_key == _min:
                break
            current_key -= 1
            j = counters[current_key - _min] - 1
        if j < 0:
            break

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
        for case in self._get_counting_sort_cases():
            self.assertEqual(case.sorted_array, counting_sort(case.array, key=case.key))

    def test_counting_sort_in_place(self):
        for case in self._get_counting_sort_cases():
            counting_sort_in_place(case.array, key=case.key)
            self.assertEqual(case.sorted_array, case.array)

    def test_query_count_in_range(self):
        case_class = namedtuple('case_class', 'array queries expected_res')
        cases = (
            case_class(array=(), queries=((1, 2), (3, 4)), expected_res=[0, 0]),
            case_class(array=(6, 4, 2, 1, 2, 3, 4, 5, 7, 2, 1),
                       queries=((0, 3), (1, 5), (5, 8), (4, 3)), expected_res=[6, 9, 3, 0]),
        )
        for case in cases:
            self.assertEqual(case.expected_res, query_count_in_range(case.array, case.queries))

    def _get_counting_sort_cases(self):
        case_class = namedtuple('case_class', 'array sorted_array key')
        cases = (
            case_class(array=[], sorted_array=[], key=None),
            case_class(array=[1], sorted_array=[1], key=None),
            case_class(array=[4, 4, 4], sorted_array=[4, 4, 4], key=None),
            case_class(array=[1, 3, 7, 5, 3, 5, 1, 1, 4], sorted_array=[1, 1, 1, 3, 3, 4, 5, 5, 7], key=None),
            case_class(array=[1, 3, 7, 5, 3, 5, 1, 1, 4], sorted_array=[7, 5, 5, 4, 3, 3, 1, 1, 1], key=lambda x: -x),
        )
        return cases
