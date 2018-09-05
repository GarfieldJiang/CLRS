from unittest import TestCase
from typing import List, Callable, TypeVar
from OrderStatistics.min_max import min_max
from collections import namedtuple
from Common.common import default_key
from Common.sort_utilities import check_sorting_result


T = TypeVar('T')


class _LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class _BucketItem:
    def __init__(self):
        self.head = self.tail = _LinkedListNode(None)


def bucket_sort(array: List[T], key: Callable[[T], int]):
    """
    Bucket sort for integers.
    :param array:
    :param key:
    :return:
    """
    assert array is not None
    if not array:
        return
    key = key or default_key
    n = len(array)
    _min, _max = min_max(array, key=key)
    min_val, max_val = key(_min), key(_max)
    bucket = [_BucketItem() for _ in range(n)]
    for i in range(n):
        current_key = key(array[i])
        j = (current_key - min_val) * n // (max_val - min_val + 1)
        assert 0 <= j < n
        tail = bucket[j].tail
        while tail:
            prev = tail.prev
            if prev is None or key(prev.data) <= current_key:
                new_node = _LinkedListNode(array[i])
                tail.prev = new_node
                new_node.next = tail
                new_node.prev = prev
                if prev is None:
                    bucket[j].head = new_node
                else:
                    prev.next = new_node
                break
            tail = tail.prev

    i = 0
    for j in range(n):
        head, tail = bucket[j].head, bucket[j].tail
        while head != tail:
            array[i] = head.data
            head = head.next
            i += 1


class TestBucketSort(TestCase):
    def test_bucket_sort(self):
        case_class = namedtuple('case_class', 'array key')
        cases = (
            case_class(array=[], key=None),
            case_class(array=[1], key=None),
            case_class(array=[-329, 457, -657, 839, -436, 720, -355], key=None),
            case_class(array=[-329, 457, -657, 839, -436, 720, -355], key=lambda x: -x),
            case_class(array=[100, 31, 32, 35, 34, 34, 36, 32, 39, 1], key=None),
        )
        for case in cases:
            before_sorting = list(case.array)
            # print('Before sorting: %r' % before_sorting)
            bucket_sort(case.array, case.key)
            # print('After sorting: %r' % case.array)
            self.assertTrue(check_sorting_result(before_sorting, case.array, key=case.key))
