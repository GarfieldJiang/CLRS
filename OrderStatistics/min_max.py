from typing import Sequence, TypeVar, Callable
from unittest import TestCase
from collections import namedtuple
from Common.common import default_key, rand_permutate
from Common.tree import BinaryTreeNode

T = TypeVar('T')
K = TypeVar('K')


def min_max(array: Sequence[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    """
    Simultaneous min and max.
    :param array:
    :param offset:
    :param length:
    :param key:
    :return:
    """
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


def two_smallest(array: Sequence[T], offset: int=0, length: int=None, key: Callable[[T], K]=None):
    """
    Exercise 9.1-1. Simultaneous min and second min.
    :param array:
    :param offset:
    :param length:
    :param key:
    :return:
    """
    assert array
    n = len(array)
    assert offset >= 0
    length = length if length is not None else n - offset
    assert length >= 2
    assert offset + length <= n
    key = key or default_key
    tree_nodes = [None] * (length // 2 if length % 2 == 0 else (length + 1) // 2)
    i = 0
    while i + 1 < length:
        node = tree_nodes[i // 2] = BinaryTreeNode()
        node.min_index = offset + i
        node.max_index = offset + i + 1
        if key(array[node.min_index]) > key(array[node.max_index]):  # Comparison
            node.min_index, node.max_index = node.max_index, node.min_index
        i += 2
    if i == length - 1:
        node = tree_nodes[len(tree_nodes) - 1] = BinaryTreeNode()
        node.min_index = node.max_index = offset + i
    tree_node_count = len(tree_nodes)

    while tree_node_count > 1:
        i = 0
        new_tree_node_count = 0
        while i + 1 < tree_node_count:
            node = BinaryTreeNode()
            left_min_index = tree_nodes[i].min_index
            right_min_index = tree_nodes[i + 1].min_index
            left_is_smaller = key(array[left_min_index]) <= key(array[right_min_index])  # Comparison
            if left_is_smaller:
                node.min_index = left_min_index
                node.max_index = right_min_index
                node.left = tree_nodes[i]
                node.right = tree_nodes[i + 1]
            else:
                node.min_index = right_min_index
                node.max_index = left_min_index
                node.left = tree_nodes[i + 1]
                node.right = tree_nodes[i]

            tree_nodes[i // 2] = node
            new_tree_node_count += 1
            i += 2
        if i == tree_node_count - 1:
            tree_nodes[new_tree_node_count] = tree_nodes[i]
            new_tree_node_count += 1
        tree_node_count = new_tree_node_count

    root = tree_nodes[0]
    min_elem = array[root.min_index]

    second_min_index = root.max_index
    root = root.left
    while root and root.min_index != root.max_index:
        if key(array[root.max_index]) < key(array[second_min_index]):
            second_min_index = root.max_index
        root = root.left
    second_min_elem = array[second_min_index]
    return min_elem, second_min_elem


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
            self.assertEqual((case.min, case.max), min_max(case.array, case.offset, case.length, case.key))

    def test_two_smallest(self):
        case_class = namedtuple('case_class', 'array offset length key min second_min')
        cases = (
            case_class(array=(1, 1), offset=0, length=None, key=None, min=1, second_min=1),
            case_class(array=(1, 2), offset=0, length=None, key=lambda x: -x, min=2, second_min=1),
            case_class(array=(2, 1), offset=0, length=None, key=lambda x: -x, min=2, second_min=1),
            case_class(array=(1, 3, 2), offset=0, length=None, key=None, min=1, second_min=2),
            case_class(array=(2, 3, 4, 5, 1), offset=0, length=None, key=None, min=1, second_min=2),
            case_class(array=(3, 8, 2, 5, 1, 7, 6, 4), offset=0, length=6, key=None, min=1, second_min=2),
            case_class(array=(3, 8, 2, 5, 1, 7, 6, 4), offset=0, length=None, key=None, min=1, second_min=2),
            case_class(array=(3, 8, 2, 5, 1, 7, 6, 4), offset=0, length=7, key=None, min=1, second_min=2),
            case_class(array=(2, 1, 3, 3, 2, 3, 1), offset=0, length=None, key=None, min=1, second_min=1),
            case_class(array=(1, 2, 3, 4, 5, 6, 7, 8, 9), offset=0, length=None, key=None, min=1, second_min=2),
        )

        for case in cases:
            self.assertEqual((case.min, case.second_min), two_smallest(case.array, case.offset, case.length, case.key))

        for length in range(2, 129):
            array = [x for x in range(1, length + 1)]
            rand_permutate(array)
            # print(array)
            case = case_class(array=array, offset=0, length=None, key=None, min=1, second_min=2)
            self.assertEqual((case.min, case.second_min), two_smallest(case.array, case.offset, case.length, case.key))
