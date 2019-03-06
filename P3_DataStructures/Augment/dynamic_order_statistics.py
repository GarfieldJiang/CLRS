"""
- OS stands for 'Order Statistic'.
- Ranks start from 1.
"""


from P3_DataStructures.RBTree.basic_ops import RBTreeNode, RBTree, rb_insert_raw, rb_insert_fixup, rb_search, rb_pop_raw, rb_pop_fixup,\
    RB_BLACK
from unittest import TestCase
from Common.common import rand_permutate
from random import randint, uniform


class OSTreeNodeAugment(object):
    def __init__(self, size=0):
        self.size = size


def os_tree_create(key=None):
    """Create an OS tree based on a red-black tree."""
    rbt = RBTree(key)
    rbt.nil.aug = OSTreeNodeAugment()
    return rbt


def os_select(ost: RBTree, i: int):
    """
    Ex 14.1-3. Select an order statistic iteratively.
    :param ost: The OS tree.
    :param i: The rank.
    :return: The node whose key is the i'th smallest.
    """
    assert ost.root != ost.nil and ost.root is not None
    assert 1 <= i <= ost.root.aug.size
    node = ost.root
    while i != node.left.aug.size + 1:
        if i < node.left.aug.size + 1:
            node = node.left
        else:
            i -= node.left.aug.size + 1
            node = node.right
    return node


def os_rank(ost: RBTree, node: RBTreeNode):
    """
    Given a node in an OS tree, find its rank.
    :param ost: The OS tree.
    :param node: The node.
    :return: The rank of the node.
    """
    assert node != ost.nil
    i = node.left.aug.size + 1
    while node != ost.root:
        if node == node.parent.right:
            i += node.parent.left.aug.size + 1
        node = node.parent
    return i


def _os_key_rank(ost, node, k):
    assert node
    if node == ost.nil:
        return -1
    key = ost.key
    if k == key(node.data):
        return node.left.aug.size + 1
    if k < key(node.data):
        return _os_key_rank(ost, node.left, k)
    return node.left.aug.size + 1 + _os_key_rank(ost, node.right, k)


def os_key_rank(ost: RBTree, k):
    return _os_key_rank(ost, ost.root, k)


def os_on_left_rotation_complete(root: RBTreeNode):
    left = root.left
    root.aug.size = left.aug.size
    left.aug.size = left.left.aug.size + left.right.aug.size + 1


def os_on_right_rotation_complete(root: RBTreeNode):
    right = root.right
    root.aug.size = right.aug.size
    right.aug.size = right.left.aug.size + right.right.aug.size + 1


def os_update_size_upward(ost: RBTree, node: RBTreeNode):
    while node != ost.nil:
        node.aug.size = node.left.aug.size + node.right.aug.size + 1
        node = node.parent


def os_insert(ost: RBTree, data) -> RBTreeNode:
    """
    Insert a new element to the given OS tree.
    """
    new_node = rb_insert_raw(ost, data)
    new_node.aug = OSTreeNodeAugment(1)
    os_update_size_upward(ost, new_node)
    rb_insert_fixup(ost, new_node, os_on_left_rotation_complete, os_on_right_rotation_complete)
    return new_node


def os_pop(ost: RBTree, node: RBTreeNode):
    """
    Remove a node from the OS tree.
    """
    color_for_check, fix_from = rb_pop_raw(ost, node)
    os_update_size_upward(ost, fix_from if fix_from != ost.nil else fix_from.parent)
    if color_for_check == RB_BLACK:
        rb_pop_fixup(ost, fix_from, os_on_left_rotation_complete, os_on_right_rotation_complete)


class TestOSTree(TestCase):
    def test_rand_insert(self):
        _len = 100
        insertion_seq = list(range(_len))
        rand_permutate(insertion_seq)
        ost = os_tree_create()
        cnt = 0
        for i in insertion_seq:
            os_insert(ost, i)
            cnt += 1
            self.assertEqual(cnt, ost.root.aug.size)
        for i in range(_len):
            node = rb_search(ost, i)
            self.assertEqual(i + 1, os_rank(ost, node))
            node1 = os_select(ost, i + 1)
            self.assertEqual(node, node1)

    def test_rand_insert_delete(self):
        def key(x):
            return -x
        ost = os_tree_create(key=key)
        insertion_seq = list(range(1000))
        rand_permutate(insertion_seq)
        values = []
        i = 0
        while i < len(insertion_seq):
            if len(values) > 0:
                rand = uniform(0, 1)
            else:
                rand = 0
            if rand > 0.5:
                rand_index = randint(0, len(values) - 1)
                value = values[rand_index]
                # print("delete %d" % value)
                values.pop(rand_index)
                node = rb_search(ost, key(value))
                os_pop(ost, node)
            else:
                value = insertion_seq[i]
                i += 1
                # print("insert %d" % value)
                values.append(value)
                values.sort(key=key)
                os_insert(ost, value)
            for j in range(len(values)):
                self.assertEqual(j + 1, os_rank(ost, rb_search(ost, key(values[j]))))
                self.assertEqual(values[j], os_select(ost, j + 1).data)
                self.assertEqual(j + 1, os_key_rank(ost, key(values[j])))
