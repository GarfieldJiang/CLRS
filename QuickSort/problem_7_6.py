"""
Ref problem_7_2.py without considering stack depth.
"""

from typing import List
from random import randint


class Interval(object):
    """
    Simple class to denote a close interval.
    """
    def __init__(self, a: int, b: int):
        if a > b:
            raise ValueError()

        self._a = a
        self._b = b

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def __repr__(self):
        return '[%d, %d]' % (self.a, self.b)

    def __str__(self):
        return '%r' % self


def _partition_intervals(array: List[Interval], points: List[int], i: int, j: int, pivot: int=None) -> (int, int):
    assert(i < j)
    small = 0
    middle = 0
    large = 0

    pivot = randint(i, j) if pivot is None else pivot
    array[j], array[pivot] = array[pivot], array[j]
    pivot_val = array[j]

    while small + middle + large < j - i:
        cur = small + middle + large + i
        after_small = small + i
        after_middle = small + middle + i
        if array[cur].b < pivot_val.a:
            array[cur], array[after_small] = array[after_small], array[cur]
            if middle > 0:
                array[cur], array[after_middle] = array[after_middle], array[cur]
            small += 1
        elif array[cur].a > pivot_val.b:
            large += 1
        else:
            array[cur], array[after_middle] = array[after_middle], array[cur]
            pivot_val = Interval(max(pivot_val.a, array[after_middle].a), min(pivot_val.b, array[after_middle].b))
            middle += 1

    left = small + i
    array[j], array[i + small + middle] = array[i + small + middle], array[j]
    middle += 1
    right = i + small + middle - 1

    if small == 1:
        points[i] = array[i].a
    if large == 1:
        points[j] = array[j].a

    for i in range(small + i, small + middle + i):
        points[i] = pivot_val.a

    return left, right


def _fuzzy_sort_intervals(array: List[Interval], points: List[int], i: int, j: int):
    if i >= j:
        return

    left, right = _partition_intervals(array, points, i, j)
    _fuzzy_sort_intervals(array, points, i, left - 1)
    _fuzzy_sort_intervals(array, points, right + 1, j)


def fuzzy_sort_intervals(array: List[Interval]):
    assert array is not None
    n = len(array)
    assert n >= 0
    points = [None] * n
    _fuzzy_sort_intervals(array, points, 0, n - 1)
    return points


def _main():
    intervals = [
        Interval(3, 6),
        Interval(4, 11),
        Interval(13, 16),
        Interval(12, 17),
        Interval(1, 9),
        Interval(10, 11),
        Interval(2, 8),
        Interval(5, 18),
        Interval(6, 6),
        Interval(7, 7),
        Interval(8, 9),
        Interval(12, 18),
        Interval(13, 15),
        Interval(16, 18),
    ]

    print('Before sorting: %r' % intervals)
    points = fuzzy_sort_intervals(intervals)
    print('After sorting: %r' % intervals)
    print('Points: %r' % points)

if __name__ == '__main__':
    _main()
