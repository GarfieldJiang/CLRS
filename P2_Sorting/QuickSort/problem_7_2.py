"""
Modified directly from quick_sort.py, dealing with duplicate values differently when selected as pivots.
"""

import unittest
from Common.sort_utilities import get_cases, check_sorting_result
from Common.common import default_key
from typing import TypeVar, List, Callable
from random import randint
from P2_Sorting.HeapSort.heap_sort import heap_sort
from collections import namedtuple

T = TypeVar('T')
K = TypeVar('K')

_DEPTH_LIMIT = 32


def _partition(array: List[T], i: int, j: int, key: Callable[[T], K], pivot: int=None) -> (int, int):
    assert(i < j)
    small = 0
    equal = 0
    large = 0

    pivot = randint(i, j) if pivot is None else pivot
    array[j], array[pivot] = array[pivot], array[j]

    while small + equal + large < j - i:
        cur = small + equal + large + i
        if key(array[cur]) < key(array[j]):
            array[cur], array[small + i] = array[small + i], array[cur]
            if equal > 0:
                array[cur], array[small + equal + i] = array[small + equal + i], array[cur]
            small += 1
        elif key(array[cur]) == key(array[j]):
            array[cur], array[small + equal + i] = array[small + equal + i], array[cur]
            equal += 1
        else:
            large += 1

    left = small + i
    array[j], array[i + small + equal] = array[i + small + equal], array[j]
    equal += 1
    right = i + small + equal - 1
    return left, right


def _quick_sort(array: List[T], i: int, j: int, key: Callable[[T], K], depth_limit: int):
    if i >= j:
        return

    if depth_limit <= 0:
        heap_sort(array, i, j - i + 1, key)
        return

    depth_limit -= 1
    left, right = _partition(array, i, j, key)
    _quick_sort(array, i, left - 1, key, depth_limit)
    _quick_sort(array, right + 1, j, key, depth_limit)


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

    def test_partition(self):
        case_class = namedtuple('case_class', 'name, array, i, j, pivot, left, right')
        cases = (
            case_class(name='2 elements #0', array=[0, 1], i=0, j=1, pivot=0, left=0, right=0),
            case_class(name='2 elements #1', array=[0, 1], i=0, j=1, pivot=1, left=1, right=1),
            case_class(name='2 elements #2', array=[0, 0], i=0, j=1, pivot=0, left=0, right=1),
            case_class(name='2 elements #3', array=[1, 1], i=0, j=1, pivot=1, left=0, right=1),
            case_class(name='5 different elements', array=[1, 2, 3, 4, 5], i=0, j=4, pivot=2, left=2, right=2),
            case_class(name='5 elements containing duplicates',
                       array=[5, 3, 3, 1, 2], i=0, j=4, pivot=2, left=2, right=3)
        )

        for case in cases:
            self.assertEqual((case.left, case.right), _partition(case.array, case.i, case.j, default_key, case.pivot),
                             'Wrong result for case \'%s\'' % case.name)
