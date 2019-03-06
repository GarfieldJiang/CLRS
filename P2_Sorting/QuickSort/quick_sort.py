import unittest
from Common.sort_utilities import get_cases, check_sorting_result
from Common.common import default_key
from typing import TypeVar, List, Callable
from random import randint
from P2_Sorting.HeapSort.heap_sort import heap_sort

T = TypeVar('T')
K = TypeVar('K')

_DEPTH_LIMIT = 32


def partition(array: List[T], i: int, j: int, key: Callable[[T], K]) -> int:
    assert(i < j)
    small = 0
    large = 0

    pivot = randint(i, j)
    array[j], array[pivot] = array[pivot], array[j]

    while small + large < j - i:
        cur = small + large + i
        if key(array[cur]) <= key(array[j]):
            array[cur], array[small + i] = array[small + i], array[cur]
            small += 1
        else:
            large += 1

    pivot = small + i
    array[j], array[pivot] = array[pivot], array[j]
    return pivot


def _quick_sort(array: List[T], i: int, j: int, key: Callable[[T], K], depth_limit: int):
    if i >= j:
        return

    if depth_limit <= 0:
        heap_sort(array, i, j - i + 1, key)
        return

    depth_limit -= 1
    k = partition(array, i, j, key)
    _quick_sort(array, i, k - 1, key, depth_limit)
    _quick_sort(array, k + 1, j, key, depth_limit)


def quick_sort(array: List[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    assert array is not None
    assert offset >= 0
    if length is None:
        length = len(array) - offset
    assert length >= 0
    _quick_sort(array, offset, offset + length - 1, key or default_key, _DEPTH_LIMIT)


def _tail_recursion_quick_sort(array: List[T], i: int, j: int, key: Callable[[T], K]):
    while i < j:
        q = partition(array, i, j, key)
        if 2 * q > i + j:
            i1 = q + 1
            j1 = j
            j = q - 1
        else:
            i1 = i
            j1 = q - 1
            i = q + 1
        _tail_recursion_quick_sort(array, i1, j1, key)


def tail_recursion_quick_sort(array: List[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    """
    Problem 7-4(c). Worst stack depth is \Theta(\lg length).
    :param array:
    :param offset:
    :param length:
    :param key:
    :return:
    """
    assert array is not None
    assert offset >= 0
    if length is None:
        length = len(array) - offset
    assert length >= 0
    _tail_recursion_quick_sort(array, offset, offset + length - 1, key or default_key)


class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        for method in quick_sort, tail_recursion_quick_sort:
            for case in get_cases():
                before_sorting = list(case.array)
                # print("Before: %r" % before_sorting)
                method(case.array, case.offset, case.length, case.key)
                # print("After: %r" % case.array)
                self.assertTrue(check_sorting_result(before_sorting, case.array, case.offset, case.length, case.key),
                                "Before: %r, After: %r" % (before_sorting, case.array))
