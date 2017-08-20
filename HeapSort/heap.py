import unittest
import logging
from collections import namedtuple
from Common.common import default_key


logging.basicConfig(level=logging.DEBUG)


def heap_left_child(i):
    return 2 * i + 1


def heap_right_child(i):
    return 2 * i + 2


def heap_parent(i):
    return (i - 1) / 2


def max_heapify(array, root_index, heap_size=None, key=None):
    """
    Ex 6.2-5. Iterative version of the Max-Heapify algorithm. O(log n) time, where n = heap_size <= len(array).
    :param array: The input array.
    :param root_index: The given index of the heap root.
    :param heap_size: array[0 .. heap_size - 1] will be considered a heap.
    :param key: function to get the sorting key.
    """
    heap_size = heap_size if heap_size is not None else len(array)
    assert heap_size <= len(array), 'Heap size cannot exceed array length'
    key = key or default_key
    n = heap_size
    while True:
        left = heap_left_child(root_index)
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


def build_max_heap(array, heap_size=None, key=None):
    """
    The standard heap building algorithm that miraculously runs in O(n) time where n = len(array).
    :param array: The input array.
    :param heap_size: array[0 .. heap_size - 1] will be considered a heap.
    :param key: function to get the sorting key.
    """
    if not array:
        return

    heap_size = heap_size or len(array)
    assert heap_size <= len(array), 'Heap size cannot exceed array length'
    key = key or default_key
    for i in xrange(heap_size / 2 - 1, -1, -1):
        max_heapify(array, i, heap_size, key)


def heap_insert(array, new_elem, key=None):
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
    while parent >= 0 and key(array[parent]) < key(array[current]):
        array[current] = array[parent]
        current = parent
        parent = heap_parent(current)
    array[current] = new_elem


def heap_delete(array, i, key=None):
    """
    Ex 6.5-8 Delete elements at index i in a max heap in O(log n) time.
    :param array: The input array.
    :param i: the index of the element to delete.
    :param key: function to get the sorting key.
    :returns: The deleted element.
    """
    deleted = array[i]
    array[i] = array[-1]
    del array[-1]
    max_heapify(array, i, key=key)
    return deleted


def check_max_heap(array, root_index, heap_size=None, key=None):
    """
    Utility method to check whether an array rooted at the given index is a max heap. O(n) time, where n = len(array).
    :param array: The input array.
    :param root_index: The given index of the heap root.
    :param heap_size: array[0 .. heap_size - 1] will be considered a heap.
    :param key: function to get the sorting key.
    """

    key = key or default_key
    heap_size = heap_size or len(array)
    n = heap_size
    if root_index >= n:
        return True

    left = heap_left_child(root_index)
    if left >= n:
        return True

    if key(array[root_index]) < key(array[left]) or not check_max_heap(array, left, heap_size, key):
        return False

    right = left + 1
    if right >= n:
        return True

    return key(array[root_index]) >= key(array[right]) and check_max_heap(array, right, heap_size, key)


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
            self.assertEqual(check_max_heap(case.array, case.root_index), case.expected_res,
                             msg='Result is wrong: %s' % case.desc)

    def test_max_heapify(self):
        case_class = namedtuple('Case', 'desc array root_index')
        cases = (
            case_class(desc='CLRS Example', array=[16, 4, 10, 14, 7, 9, 3, 2, 8, 1], root_index=1),
        )
        for case in cases:
            self.assertTrue(check_max_heap(case.array, heap_left_child(case.root_index)),
                            msg='Invalid input')
            self.assertTrue(check_max_heap(case.array, heap_right_child(case.root_index)),
                            msg='Invalid input')
            max_heapify(case.array, case.root_index)
            self.assertTrue(check_max_heap(case.array, case.root_index, len(case.array)),
                            msg='Heap is not max: %s' % case.desc)

    def test_build_max_heap(self):
        case_class = namedtuple('Case', 'desc array key')
        need_key_item_class = namedtuple('NeedKeyItem', 'key value')
        cases = (
            case_class(desc='Empty', array=[], key=None),
            case_class(desc='Big sorted', array=[i for i in xrange(0, 8192)], key=None),
            case_class(desc='Big inversely sorted', array=[999 - i for i in xrange(0, 1000)], key=None),
            case_class(desc='Need another key',
                       array=[need_key_item_class(key=999-i, value=i) for i in xrange(0, 1000)], key=lambda x: x.key)
        )
        for case in cases:
            build_max_heap(case.array, key=case.key)
            self.assertTrue(check_max_heap(case.array, 0, key=case.key),
                            msg='Heap is not max: %s' % case.desc)

    def test_heap_delete(self):
        case_class = namedtuple('Case', 'desc array key')
        need_key_item_class = namedtuple('NeedKeyItem', 'key value')
        cases = (
            case_class(desc='Single', array=[1], key=None),
            case_class(desc='Big sorted', array=[i for i in xrange(0, 100)], key=None),
            case_class(desc='Big inversely sorted', array=[99 - i for i in xrange(0, 100)], key=None),
            case_class(desc='Need another key',
                       array=[need_key_item_class(key=99-i, value=i) for i in xrange(0, 100)], key=lambda x: x.key)
        )
        for case in cases:
            len_array = len(case.array)
            for i in xrange(0, len_array):
                array_copy = list(case.array)
                build_max_heap(array_copy, key=case.key)
                expected_deleted = array_copy[i]
                deleted = heap_delete(array_copy, i, key=case.key)
                self.assertEqual(deleted, expected_deleted,
                                 msg='Wrong deletion: %s != %s' % (deleted, expected_deleted))
                self.assertTrue(check_max_heap(array_copy, 0, key=case.key),
                                msg='Heap is not max: %s' % case.desc)
