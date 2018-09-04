from unittest import TestCase
from typing import List, Callable, TypeVar
from collections import namedtuple
from Common.common import default_key
from Common.sort_utilities import check_sorting_result
from LinearTimeSorting.couting_sort import counting_sort


T = TypeVar('T')


class _DigitsView(object):
    """
    Simple class to maintain an array of digits of the given value (positive integer).
    """

    def __init__(self, val: int, radix: int, satellite_data):
        assert radix > 1
        assert val > 0
        self._val = val
        digits = []
        while True:
            digits.append(val % radix)
            val //= radix
            if val == 0:
                break
        self._digits = digits
        self._satellite_data = satellite_data

    def __repr__(self):
        return str(self._val)

    def __str__(self):
        return str(self._val)

    @property
    def negative(self):
        return self._negative

    @property
    def satellite_data(self):
        return self._satellite_data

    @property
    def digit_count(self):
        digits = self._digits
        return 0 if not digits else len(digits)

    def digit(self, index):
        digits = self._digits
        return 0 if not digits or index >= len(digits) else digits[index]


def radix_sort(array: List[T], radix: int, key: Callable[[T], int] = None):
    """
    Naive implementation that deals with only positive integers.
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
    digits_views = [None] * n
    max_digit_count = 0
    for i in range(n):
        digits_views[i] = _DigitsView(key(array[i]), radix, array[i])
        digit_count = digits_views[i].digit_count
        if digit_count > max_digit_count:
            max_digit_count = digit_count

    for i in range(max_digit_count):
        digits_views = counting_sort(digits_views, lambda dv: dv.digit(i))

    for i in range(n):
        array[i] = digits_views[i].satellite_data


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
