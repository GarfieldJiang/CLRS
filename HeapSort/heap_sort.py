import unittest
from Common.sort_utilities import get_cases, check_is_sorted
from Common.common import default_key
from HeapSort.heap import build_max_heap, max_heapify


def heap_sort(array, key=None):
    """
    Standard heap sort algorithm that works in place in O(n log n) time, where n = len(array).
    :param array: The input array (list).
    :param key: The key getter.
    """
    if not array:
        return

    key = key or default_key
    heap_size = len(array)

    build_max_heap(array, heap_size=heap_size, key=key)
    while heap_size > 1:
        array[heap_size - 1], array[0] = array[0], array[heap_size - 1]
        heap_size -= 1
        max_heapify(array, 0, heap_size=heap_size, key=key)


class TestHeapSort(unittest.TestCase):
    def test_heap_sort(self):
        for case in get_cases():
            heap_sort(case.array, case.key)
            self.assertTrue(check_is_sorted(case.array, case.key), msg='Not sorted: %s' % case.desc)
