import unittest
from Common.sort_utilities import get_cases, check_is_sorted
from Common.common import default_key
from typing import TypeVar, Sequence, Callable
from random import randint

T = TypeVar('T')
K = TypeVar('K')


def _partition(array: Sequence[T], i: int, j: int, key: Callable[[T], K]) -> int:
    assert(i < j)
    small = 0
    large = 0

    pivot = randint(i, j)
    tmp = array[j]
    array[j] = array[pivot]
    array[pivot] = tmp

    while small + large < j - i:
        cur = small + large + i
        if key(array[cur]) <= key(array[j]):
            tmp = array[cur]
            array[cur] = array[small + i]
            array[small + i] = tmp
            small += 1
        else:
            large += 1

    tmp = array[j]
    pivot = small + i
    array[j] = array[pivot]
    array[pivot] = tmp
    return pivot


def _quick_sort(array: Sequence[T], i: int, j: int, key: Callable[[T], K]):
    if i >= j:
        return

    k = _partition(array, i, j, key)
    _quick_sort(array, i, k - 1, key)
    _quick_sort(array, k + 1, j, key)


def quick_sort(array: Sequence, key: Callable[[T], K]):
    if not array:
        return
    _quick_sort(array, 0, len(array) - 1, key or default_key)


class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        for case in get_cases():
            if len(case.array) >= 102:
                continue
            before_sorting = list(case.array)
            print("Before: %r" % before_sorting)
            quick_sort(case.array, case.key)
            print("After: %r" % case.array)
            self.assertTrue(check_is_sorted(case.array, case.key),
                            "Before: %r, After: %r" % (before_sorting, case.array))
