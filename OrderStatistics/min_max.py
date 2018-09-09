from typing import Sequence, TypeVar, Callable
from unittest import TestCase
from collections import namedtuple
from Common.common import default_key

T = TypeVar('T')
K = TypeVar('K')


def min_max(array: Sequence[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    assert array
    n = len(array)
    assert offset >= 0
    length = length if length is not None else n - offset
    assert length >= 0 and offset + length <= n
    key = key or default_key

    if length % 2 == 1:
        my_min = my_max = array[offset]
        i = offset + 1
    else:
        my_min, my_max = array[offset], array[offset + 1]
        if key(my_min) > key(my_max):
            my_min, my_max = my_max, my_min
        i = offset + 2
    right = offset + length - 1
    while i < right:
        local_min = array[i]
        local_max = array[i + 1]
        if key(local_min) > key(local_max):
            local_min, local_max = local_max, local_min
        if my_min is None or key(local_min) <= key(my_min):
            my_min = local_min
        if my_max is None or key(local_max) >= key(my_max):
            my_max = local_max
        i += 2
    return my_min, my_max


class TestMinMax(TestCase):
    def test_min_max(self):
        case_class = namedtuple('case_class', 'array offset length min max key')
        cases = (
            case_class(array=(1,), offset=0, length=1, min=1, max=1, key=None),
            case_class(array=(1, 2), offset=0, length=2, min=1, max=2, key=None),
            case_class(array=(2, 1), offset=0, length=2, min=1, max=2, key=None),
            case_class(array=(1, 5, 4, 2, 3), offset=0, length=5, min=1, max=5, key=None),
            case_class(array=(1, 5, 4, 2, 3), offset=1, length=3, min=2, max=5, key=None),
            case_class(array=(4, 4, 3, 3, 5, 5, 4), offset=0, length=7, min=3, max=5, key=None),
            case_class(array=(1, 5, 4, 2, 3), offset=0, length=5, key=lambda x: -x, min=5, max=1),
            case_class(array=(4, 2, 3, 1, 1, 3), offset=0, length=6, key=lambda x: -x, min=4, max=1),
        )
        for case in cases:
            self.assertEqual(min_max(case.array, case.offset, case.length, case.key), (case.min, case.max))
