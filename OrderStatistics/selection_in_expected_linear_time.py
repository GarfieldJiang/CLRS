from typing import TypeVar, List, Callable
from Common.common import default_key, rand_permutate
from QuickSort.quick_sort import partition
from unittest import TestCase
from collections import namedtuple
from random import randint


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


def select(array: List[T], i: int, key: Callable[[T], K]=None) -> T:
    """
    Ex. 9.2-3. Select the i'th smallest element in the sorted version of the given array, iteratively.
    Runs in expected O(n) time, and will modify the input.
    :param array: Input array.
    :param i: Element rank, starting from 0.
    :param key: Key getter.
    :return: The i'th smallest element
    """
    assert array
    n = len(array)
    assert 0 <= i < n
    key = key or default_key
    return _rand_select(array, i, key)


class TestSelection(TestCase):
    def test_selection(self):
        case_class = namedtuple('case_class', 'array i key expected_res')
        cases = (
            case_class(array=[1], i=0, key=None, expected_res=1),
            case_class(array=[1, 3, 5, 4, 2, 7, 6], i=4, key=None, expected_res=5),
            case_class(array=[1, 3, 5, 4, 2, 7, 6], i=2, key=None, expected_res=3),
            case_class(array=[1, 3, 5, 4, 2, 7, 6], i=6, key=lambda x: -x, expected_res=1),
        )

        for case in cases:
            # print(case.array, case.i)
            self.assertEqual(case.expected_res, select(case.array, case.i, case.key))

        for length in range(1, 100):
            i = randint(0, length - 1)
            array = [x * x for x in range(0, length)]
            rand_permutate(array)
            case = case_class(array=array, i=i, key=None, expected_res=i * i)
            # print(case.array, case.i)
            self.assertEqual(case.expected_res, select(case.array, case.i, case.key))
