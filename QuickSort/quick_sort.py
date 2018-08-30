import unittest
from Common.sort_utilities import get_cases, check_sorting_result
from Common.common import default_key
from typing import TypeVar, List, Callable
from random import randint
from HeapSort.heap_sort import heap_sort

T = TypeVar('T')
K = TypeVar('K')

_DEPTH_LIMIT = 32


def _partition(array: List[T], i: int, j: int, key: Callable[[T], K]) -> int:
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
    k = _partition(array, i, j, key)
    _quick_sort(array, i, k - 1, key, depth_limit)
    _quick_sort(array, k + 1, j, key, depth_limit)


def quick_sort(array: List[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    assert array is not None
    assert offset >= 0
    if length is None:
        length = len(array) - offset
    assert length >= 0
    _quick_sort(array, offset, offset + length - 1, key or default_key, _DEPTH_LIMIT)


class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        for case in get_cases():
            before_sorting = list(case.array)
            # print("Before: %r" % before_sorting)
            quick_sort(case.array, case.offset, case.length, case.key)
            # print("After: %r" % case.array)
            self.assertTrue(check_sorting_result(before_sorting, case.array, case.offset, case.length, case.key),
                            "Before: %r, After: %r" % (before_sorting, case.array))
