from typing import TypeVar, List, Callable
from Common.common import default_key, rand_permutate
from QuickSort.quick_sort import partition
from unittest import TestCase
from collections import namedtuple
from random import randint
from OrderStatistics.min_max import min_max

_COUNT_PER_GROUP_IN_SELECTION = 5

T = TypeVar('T')
K = TypeVar('K')


def _rand_select(array: List[T], i: int, key: Callable[[T], K]):
    lo = 0
    hi = len(array) - 1
    while True:
        if lo == hi:
            return array[lo]
        pivot_index = partition(array, lo, hi, key)
        if i == pivot_index:
            return array[pivot_index]
        if pivot_index < i:
            lo = pivot_index + 1
        else:
            hi = pivot_index - 1


def rand_select(array: List[T], rank: int, key: Callable[[T], K]=None) -> T:
    """
    Ex. 9.2-3. Select the i'th smallest element (i = rank) in the sorted version of the given array, iteratively.
    Runs in expected O(n) time, and will modify the input.
    :param array: Input array.
    :param rank: Element rank, starting from 0.
    :param key: Key getter.
    :return: The i'th smallest element.
    """
    assert array
    n = len(array)
    assert 0 <= rank < n
    key = key or default_key
    return _rand_select(array, rank, key)


def _insertion_sort(array: List[T], lo: int, hi: int, key: Callable[[T], K]):
    if lo >= hi:
        return
    for i in range(lo + 1, hi + 1):
        for j in range(i - 1, lo - 1, -1):
            if key(array[j]) <= key(array[j + 1]):
                break
            array[j], array[j + 1] = array[j + 1], array[j]


def _partition_by_value(array: List[T], i: int, j: int, key: Callable[[T], K], val: T) -> int:
    assert(i < j)
    small = 0
    large = 0

    pivot = None
    while small + large < j - i + 1:
        cur = small + large + i
        if key(array[cur]) <= key(val):
            if pivot is None and key(array[cur]) == key(val):
                pivot = small + i
            array[cur], array[small + i] = array[small + i], array[cur]
            small += 1
        else:
            large += 1

    array[pivot], array[small + i - 1] = array[small + i - 1], array[pivot]
    return small + i - 1


def _select(array: List[T], lo: int, hi: int, rank: int, key: Callable[[T], K]) -> T:
    if lo == hi:
        return array[lo]

    length = hi - lo + 1
    group_count = length // _COUNT_PER_GROUP_IN_SELECTION if length % _COUNT_PER_GROUP_IN_SELECTION == 0\
        else length // _COUNT_PER_GROUP_IN_SELECTION + 1
    medians = [None] * group_count
    for i in range(group_count):
        sub_length = min(_COUNT_PER_GROUP_IN_SELECTION, length - i * _COUNT_PER_GROUP_IN_SELECTION)
        _insertion_sort(array, lo + i * _COUNT_PER_GROUP_IN_SELECTION,
                        lo + i * _COUNT_PER_GROUP_IN_SELECTION + sub_length - 1, key)
        medians[i] = array[lo + i * _COUNT_PER_GROUP_IN_SELECTION + (sub_length - 1) // 2]
    median_of_medians = _select(medians, 0, group_count - 1, (group_count - 1) // 2, key)
    pivot = _partition_by_value(array, lo, hi, key, median_of_medians)
    if pivot == rank:
        return array[rank]
    if pivot < rank:
        return _select(array, pivot + 1, hi, rank, key)
    return _select(array, lo, pivot - 1, rank, key)


def select(array: List[T], rank: int, key: Callable[[T], K]=None) -> T:
    """
    Section 9.3. Select the i'th smallest element (i = rank) in the sorted version of the given array.
    Runs in worst-case O(n) time.
    :param array: Input array.
    :param rank: Element rank, starting from 0.
    :param key: Key getter.
    :return: The i'th smallest element.
    """
    assert array
    n = len(array)
    assert 0 <= rank < n
    key = key or default_key
    return _select(array, 0, n - 1, rank, key)


def _get_quantile_index(n, subset_count, i):
    return round((i + 1) * n / subset_count) - 1


def _calc_quantiles(array: List[T], lo: int, hi: int, subset_count: int, quantile_lo: int, quantile_hi: int,
                    key: Callable[[T], K], quantiles: List[T]):
    if quantile_lo > quantile_hi:
        return
    n = len(array)
    quantile_mid = quantile_lo + (quantile_hi - quantile_lo) // 2
    quantile_mid_pos = _get_quantile_index(n, subset_count, quantile_mid)
    v = _select(array, lo, hi, quantile_mid_pos, key)
    quantiles[quantile_mid] = v
    if quantile_lo == quantile_hi:
        return
    _calc_quantiles(array, lo, quantile_mid_pos - 1, subset_count, quantile_lo, quantile_mid - 1, key, quantiles)
    _calc_quantiles(array, quantile_mid_pos + 1, hi, subset_count, quantile_mid + 1, quantile_hi, key, quantiles)


def calc_quantiles(array: List[T], subset_count: int, key: Callable[[T], K]=None) -> List[T]:
    """
    Ex 9.3-6.
    :param array: Input array.
    :param subset_count: How many subsets we want.
    :param key: Key getter.
    :return: The quantiles.
    """
    assert array
    n = len(array)
    assert n >= 1
    assert 0 < subset_count <= n
    key = key or default_key
    ret: List[T] = [None] * subset_count
    _calc_quantiles(array, 0, n - 1, subset_count, 0, subset_count - 1, key, ret)
    return ret


class TestSelection(TestCase):
    def test_selection(self):
        case_class = namedtuple('case_class', 'array i key expected_res')
        for select_method in (rand_select, select,):
            cases = (
                case_class(array=[1], i=0, key=None, expected_res=1),
                case_class(array=[1, 3, 5, 4, 2, 7, 6], i=4, key=None, expected_res=5),
                case_class(array=[1, 3, 5, 4, 2, 7, 6], i=2, key=None, expected_res=3),
                case_class(array=[1, 3, 5, 4, 2, 7, 6], i=6, key=lambda x: -x, expected_res=1),
                case_class(array=[16, 196, 64, 121, 144, 9, 36, 0, 49, 100, 4, 81, 169, 1, 25], i=4, key=None,
                           expected_res=16)
            )

            for case in cases:
                # print(case.array, case.i)
                self.assertEqual(case.expected_res, select_method(case.array, case.i, case.key))

            for length in range(1, 100):
                i = randint(0, length - 1)
                array = [x * x for x in range(0, length)]
                rand_permutate(array)
                case = case_class(array=array, i=i, key=None, expected_res=i * i)
                # print(case.array, case.i)
                self.assertEqual(case.expected_res, select_method(case.array, case.i, case.key))

    def test_quantiles(self):
        case_class = namedtuple('case_class', 'array subset_count key expected_res')
        cases = (
            case_class(array=[100], subset_count=1, key=None, expected_res=[100]),
            case_class(array=[1, 3, 5, 4, 2, 7, 6], subset_count=3, key=None, expected_res=[2, 5, 7]),
            case_class(array=[1, 3, 5, 4, 2, 7, 6], subset_count=4, key=None, expected_res=[2, 4, 5, 7]),
            case_class(array=[1, 3, 5, 4, 2, 7, 6], subset_count=7, key=None, expected_res=[1, 2, 3, 4, 5, 6, 7]),
            case_class(array=[8, 2, 1, 3, 7, 5, 4, 6], subset_count=1, key=None, expected_res=[8]),
            case_class(array=[8, 2, 1, 3, 7, 5, 4, 6], subset_count=2, key=None, expected_res=[4, 8]),
            case_class(array=[8, 2, 1, 3, 7, 5, 4, 6], subset_count=3, key=None, expected_res=[3, 5, 8]),
            case_class(array=[8, 2, 1, 3, 7, 5, 4, 6], subset_count=3, key=lambda x: -x, expected_res=[6, 4, 1]),
            case_class(array=[8, 2, 1, 3, 7, 5, 4, 6], subset_count=4, key=None, expected_res=[2, 4, 6, 8]),
        )

        for case in cases:
            # print(case.array, case.subset_count)
            res = calc_quantiles(case.array, case.subset_count, case.key)
            self.assertEqual(case.expected_res, res)

        for length in range(1, 100):
            subset_count = randint(1, length)
            array = [x * 2 for x in range(0, length)]
            rand_permutate(array)
            # print(array, subset_count)
            res = calc_quantiles(array, subset_count)
            # print(res)
            self.assertEqual(subset_count, len(res))
            if subset_count > 1:
                diffs = []
                for i in range(0, subset_count - 1):
                    self.assertEqual(0, res[i] % 2)
                    diffs.append(res[i + 1] - res[i])
                min_diff, max_diff = min_max(diffs)
                self.assertTrue(max_diff - min_diff <= 2)
            self.assertEqual(array[length - 1], res[subset_count - 1])
