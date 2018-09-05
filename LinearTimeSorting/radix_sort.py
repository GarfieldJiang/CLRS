from unittest import TestCase
from typing import List, Callable, TypeVar
from collections import namedtuple
from Common.common import default_key
from Common.sort_utilities import check_sorting_result
from LinearTimeSorting.couting_sort import counting_sort


T = TypeVar('T')


def _get_digit_count(val: int, radix: int):
    ret = 0
    while val > 0:
        val = val // radix
        ret += 1
    return ret


def _get_digit_factors(digit_count: int, radix: int):
    ret = [0] * (digit_count + 1)
    factor = 1
    for i in range(digit_count + 1):
        ret[i] = factor
        factor *= radix
    return ret


def radix_sort(array: List[T], radix: int, key: Callable[[T], int] = None):
    """
    Simple implementation of radix sort that deals with only positive integers.
    :param array: Input array.
    :param radix: Radix.
    :param key: Key getter.
    :return:
    """
    assert array is not None
    assert radix > 1
    if not array:
        return
    n = len(array)
    key = key or default_key
    max_digit_count = 0
    for i in range(n):
        assert key(array[i]) > 0
        digit_count = _get_digit_count(key(array[i]), radix)
        if digit_count > max_digit_count:
            max_digit_count = digit_count
    factors = _get_digit_factors(max_digit_count, radix)
    sorted_array = array
    for i in range(max_digit_count):
        digit_key: Callable[[T], int] = lambda v: key(v) % factors[i + 1] // factors[i]
        sorted_array = counting_sort(sorted_array, digit_key)
    for i in range(n):
        array[i] = sorted_array[i]


class TestRadixSort(TestCase):
    def test_radix_sort(self):
        case_class = namedtuple('case_class', 'array radix key')
        cases = (
            case_class(array=[], radix=101, key=None),
            case_class(array=[329, 457, 657, 839, 436, 720, 355], radix=10, key=None),
            case_class(array=[-329, -457, -657, -839, -436, -720, -355], radix=10, key=lambda x: -x),
            case_class(array=[13, 3, 113, 910113, 10113], radix=10, key=None),
        )

        for case in cases:
            before_sorting = list(case.array)
            # print('Before sorting: %r' % before_sorting)
            radix_sort(case.array, case.radix, case.key)
            # print('After sorting: %r' % case.array)
            self.assertTrue(check_sorting_result(before_sorting, case.array, key=case.key))
