import unittest
from Common.sort_utilities import get_cases, check_sorting_result
from Common.common import default_key
from P2_Sorting.HeapSort.heap import build_max_heap, max_heapify
from typing import List, TypeVar, Callable


T = TypeVar('T')
K = TypeVar('K')


def heap_sort(array: List[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    """
    Standard heap sort algorithm that works in place in O(n log n) time, where n = len(array) - offset.
    :param array: The input array (list).
    :param offset: Where to start sorting.
    :param length: P2_Sorting length.
    :param key: The key getter.
    """
    assert array is not None
    assert offset >= 0
    heap_size = length if length is not None else (len(array) - offset)
    assert len(array) >= heap_size >= 0

    key = key or default_key

    build_max_heap(array, offset=offset, heap_size=heap_size, key=key)
    while heap_size > 1:
        array[offset + heap_size - 1], array[offset] = array[offset], array[offset + heap_size - 1]
        heap_size -= 1
        max_heapify(array, offset=offset, root_index=offset, heap_size=heap_size, key=key)


class TestHeapSort(unittest.TestCase):
    def test_heap_sort(self):
        for case in get_cases():
            before_sorting = list(case.array)
            # print('Before: %r' % before_sorting)
            heap_sort(case.array, offset=case.offset, length=case.length, key=case.key)
            # print('After: %r' % case.array)
            self.assertTrue(check_sorting_result(
                before_sorting, case.array, offset=case.offset, length=case.length, key=case.key),
                msg='Wrong result: %s' % case.desc)
