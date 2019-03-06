from .selection_in_linear_time import select_internal
from typing import TypeVar, List, Callable
from unittest import TestCase
from collections import namedtuple

T = TypeVar('T')
K = TypeVar('K')


def weighted_median(array: List[T], lo: int, hi: int, key: Callable[[T], K]=None):
    """
    Problem 9-2 (c).
    :param array:
    :param lo:
    :param hi:
    :param key:
    :return:
    """
    assert array
    n = len(array)
    assert lo >= 0
    assert hi < n
    assert lo <= hi

    def _default_key(x):
        return x.data
    key = key or _default_key

    while True:
        mid = (lo + hi) // 2
        median = select_internal(array, lo, hi, mid, key)
        median_weight = median.weight
        left_weight = 0
        for i in range(lo, mid - 1):
            left_weight += array[i].weight
        right_weight = 0
        for i in range(mid + 1, hi):
            right_weight += array[i].weight
        total_weight = left_weight + median_weight + right_weight
        if 2 * left_weight < total_weight and 2 * right_weight <= total_weight:
            return median
        if 2 * left_weight < total_weight < 2 * right_weight:
            lo = mid + 1
        else:
            hi = mid - 1


class TestWeightedMedian(TestCase):
    def test_weighted_median(self):
        weighted_data_class = namedtuple('weighted_data_class', 'data weight')
        case_class = namedtuple('case_class', 'array expected_res')
        cases = (
            case_class(array=[weighted_data_class(data=1, weight=1)], expected_res=1),
            case_class(
                array=[
                    weighted_data_class(data=10, weight=10),
                    weighted_data_class(data=35, weight=35),
                    weighted_data_class(data=6, weight=5),
                    weighted_data_class(data=15, weight=15),
                    weighted_data_class(data=4, weight=5),
                    weighted_data_class(data=20, weight=20),
                ], expected_res=20
            ),
            case_class(
                array=[
                    weighted_data_class(data=10, weight=10),
                    weighted_data_class(data=35, weight=10),
                    weighted_data_class(data=6, weight=10),
                    weighted_data_class(data=15, weight=10),
                    weighted_data_class(data=4, weight=10),
                    weighted_data_class(data=20, weight=10),
                ], expected_res=10
            ),
        )

        for case in cases:
            median = weighted_median(case.array, 0, len(case.array) - 1).data
            self.assertEqual(case.expected_res, median)
