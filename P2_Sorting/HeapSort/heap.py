import unittest
import logging
from collections import namedtuple
from Common.common import default_key
from typing import List, Callable, TypeVar


T = TypeVar('T')
K = TypeVar('K')


logging.basicConfig(level=logging.DEBUG)


def heap_left_child(i: int, offset: int=0):
    return 2 * i + 1 - offset


def heap_right_child(i: int, offset: int=0):
    return 2 * i + 2 - offset


def heap_parent(i: int, offset: int=0):
    return (i - 1 + offset) // 2


def max_heapify(array: List[T], offset: int, root_index: int, heap_size: int=None, key: Callable[[T], K]=None):
    """
    Ex 6.2-5. Iterative version of the Max-Heapify algorithm. O(log n) time, where n = heap_size <= len(array).
    :param array: The input array.
    :param offset: Where the heap starts.
    :param root_index: The given index of the heap root.
    :param heap_size: array[offset .. offset + heap_size - 1] will be considered a heap.
    :param key: function to get the sorting key.
    """
    assert offset >= 0
    heap_size = heap_size if heap_size is not None else (len(array) - offset)
    assert len(array) >= heap_size >= 0
    key = key or default_key
    n = offset + heap_size
    while True:
        left = heap_left_child(root_index, offset)
        if left >= n:
            break

        right = left + 1
        if key(array[root_index]) > key(array[left]) and (right >= n or key(array[root_index]) > key(array[right])):
            break

        if right >= n or key(array[left]) > key(array[right]):
            max_node = left
        else:
            max_node = right

        array[root_index], array[max_node] = array[max_node], array[root_index]
        root_index = max_node


def build_max_heap(array: List[T], offset: int, heap_size: int=None, key: Callable[[T], K]=None):
    """
    The standard heap building algorithm that miraculously runs in O(n) time where n = len(array).
    :param array: The input array.
    :param offset: Where the heap starts.
    :param heap_size: array[offset .. offset + heap_size - 1] will be considered a heap.
    :param key: function to get the sorting key.
    """
    if not array:
        return

    assert offset >= 0
    heap_size = heap_size or len(array) - offset
    assert len(array) >= heap_size >= 0
    key = key or default_key
    for i in range(offset + heap_size // 2 - 1, offset - 1, -1):
        max_heapify(array, offset, i, heap_size, key)


def heap_insert(array: List[T], new_elem: T, key: Callable[[T], K]=None):
    """
    Inserts a new element into the max heap in O(log n) time, Optimized by Ex 6.5-6
    :param array: The input array.
    :param new_elem: The new element to insert.
    :param key: function to get the sorting key.
    """
    array.append(new_elem)
    heap_size = len(array)
    key = key or default_key
    current = heap_size - 1
    parent = heap_parent(current)
    while parent >= 0 and key(array[parent]) < key(new_elem):
        array[current] = array[parent]
        current = parent
        parent = heap_parent(current)
    array[current] = new_elem


def heap_delete(array: List[T], i: int, key=None):
    """
    Ex 6.5-8 Delete elements at index i in a max heap in O(log n) time.
    :param array: The input array.
    :param i: the index of the element to delete.
    :param key: function to get the sorting key.
    :return: The deleted element.
    """
    deleted = array[i]
    array[i] = array[-1]
    if i == len(array) - 1:
        del array[-1]
        return deleted

    del array[-1]
    key = key or default_key
    if i == 0 or key(array[heap_parent(i)]) >= key(array[i]):
        max_heapify(array, 0, i, key=key)
    else:
        while i > 0 and key(array[heap_parent(i)]) < key(array[i]):
            array[heap_parent(i)], array[i] = array[i], array[heap_parent(i)]
            i = heap_parent(i)
    return deleted


def check_max_heap(array: List[T], offset: int, root_index: int, heap_size: int=None, key: Callable[[T], K]=None):
    """
    Utility method to check whether an array rooted at the given index is a max heap. O(n) time, where n = len(array).
    :param array: The input array.
    :param offset: Where the heap starts.
    :param root_index: The given index of the heap root.
    :param heap_size: array[offset .. offset + heap_size - 1] will be considered a heap.
    :param key: function to get the sorting key.
    """

    key = key or default_key
    assert(offset >= 0)
    heap_size = heap_size or len(array) - offset
    assert(len(array) >= heap_size >= 0)
    n = offset + heap_size
    if root_index >= n:
        return True

    left = heap_left_child(root_index, offset)
    if left >= n:
        return True

    if key(array[root_index]) < key(array[left]) or not check_max_heap(array, offset, left, heap_size, key):
        return False

    right = left + 1
    if right >= n:
        return True

    return key(array[root_index]) >= key(array[right]) and check_max_heap(array, offset, right, heap_size, key)


class TestHeap(unittest.TestCase):
    def test_check_max_heap(self):
        case_class = namedtuple('Case', 'desc array root_index expected_res')
        cases = (
            case_class(desc='Empty', array=[], root_index=0, expected_res=True),
            case_class(desc='Singleton', array=[100], root_index=0, expected_res=True),
            case_class(desc='2 True', array=[2, 1], root_index=0, expected_res=True),
            case_class(desc='2 False', array=[1, 2], root_index=0, expected_res=False),
            case_class(desc='3 True #0', array=[3, 1, 2], root_index=0, expected_res=True),
            case_class(desc='3 True #1', array=[3, 2, 1], root_index=0, expected_res=True),
            case_class(desc='3 True #2 (even)', array=[1, 1, 1], root_index=0, expected_res=True),
            case_class(desc='3 False #0', array=[1, 2, 3], root_index=0, expected_res=False),
            case_class(desc='3 False #1', array=[2, 1, 3], root_index=0, expected_res=False),
            case_class(desc='3 False #2', array=[2, 3, 1], root_index=0, expected_res=False),
            case_class(desc='CLRS Example before max_heapify index at 2',
                       array=[16, 4, 10, 14, 7, 9, 3, 2, 8, 1], root_index=2, expected_res=True),
            case_class(desc='CLRS Example before max_heapify index at 1',
                       array=[16, 4, 10, 14, 7, 9, 3, 2, 8, 1], root_index=1, expected_res=False),
            case_class(desc='CLRS Example before max_heapify index at 0',
                       array=[16, 4, 10, 14, 7, 9, 3, 2, 8, 1], root_index=0, expected_res=False),
            case_class(desc='CLRS Example after max_heapify', array=[16, 14, 10, 8, 7, 9, 3, 2, 4, 1], root_index=1,
                       expected_res=True),
        )
        for case in cases:
            self.assertEqual(check_max_heap(case.array, 0, case.root_index), case.expected_res,
                             msg='Result is wrong: %s' % case.desc)

    def test_max_heapify(self):
        case_class = namedtuple('Case', 'desc array root_index')
        cases = (
            case_class(desc='CLRS Example', array=[16, 4, 10, 14, 7, 9, 3, 2, 8, 1], root_index=1),
        )
        for case in cases:
            self.assertTrue(check_max_heap(case.array, 0, heap_left_child(case.root_index)),
                            msg='Invalid input')
            self.assertTrue(check_max_heap(case.array, 0, heap_right_child(case.root_index)),
                            msg='Invalid input')
            max_heapify(case.array, 0, case.root_index)
            self.assertTrue(check_max_heap(case.array, 0, case.root_index, len(case.array)),
                            msg='Heap is not max: %s' % case.desc)

    def test_build_max_heap(self):
        case_class = namedtuple('Case', 'desc array key')
        need_key_item_class = namedtuple('NeedKeyItem', 'key value')
        cases = (
            case_class(desc='Empty', array=[], key=None),
            case_class(desc='Big sorted', array=[i for i in range(0, 8192)], key=None),
            case_class(desc='Big inversely sorted', array=[999 - i for i in range(0, 1000)], key=None),
            case_class(desc='Need another key',
                       array=[need_key_item_class(key=999-i, value=i) for i in range(0, 1000)], key=lambda x: x.key)
        )
        for case in cases:
            build_max_heap(case.array, 0, key=case.key)
            self.assertTrue(check_max_heap(case.array, 0, 0, key=case.key),
                            msg='Heap is not max: %s' % case.desc)

    def test_heap_delete(self):
        case_class = namedtuple('Case', 'desc array key')
        need_key_item_class = namedtuple('NeedKeyItem', 'key value')
        cases = (
            case_class(desc='Single', array=[1], key=None),
            case_class(desc='Big sorted', array=[i for i in range(0, 100)], key=None),
            case_class(desc='Big inversely sorted', array=[99 - i for i in range(0, 100)], key=None),
            case_class(desc='Need another key',
                       array=[need_key_item_class(key=99-i, value=i) for i in range(0, 100)], key=lambda x: x.key),
            case_class(desc='Unordered', array=[4, 8, 5, 7, 1, 2, 6, 3], key=None),
        )
        for case in cases:
            len_array = len(case.array)
            for i in range(0, len_array):
                array_copy = list(case.array)
                build_max_heap(array_copy, 0, key=case.key)
                expected_deleted = array_copy[i]
                deleted = heap_delete(array_copy, i, key=case.key)
                self.assertEqual(deleted, expected_deleted,
                                 msg='Wrong deletion: %s != %s' % (deleted, expected_deleted))
                self.assertTrue(check_max_heap(array_copy, 0, 0, key=case.key),
                                msg='Heap is not max: %s' % case.desc)

    def test_heap_delete_rand(self):
        from Common.common import rand_permutate
        from random import randint
        for i in range(100):
            len = randint(10, 100)
            array = list(range(1, len + 1))
            rand_permutate(array)
            build_max_heap(array, 0)
            self.assertTrue(check_max_heap(array, 0, 0))
            for j in range(len):
                array_copy = list(array)
                heap_delete(array_copy, j)
                self.assertTrue(check_max_heap(array_copy, 0, 0),
                                msg='Heap is not max %r. from %r deleting element at %d' % (array_copy, array, j))
