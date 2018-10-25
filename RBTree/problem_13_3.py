from Common.tree import BinaryTreeNode
from Common.common import default_key, rand_permutate
from typing import Optional
from unittest import TestCase
from BST.basic_ops import bst_iter, bst_search, bst_transplant, bst_min
from random import uniform, randint


class AVLTreeNode(BinaryTreeNode):
    def __init__(self, data):
        super().__init__(data)
        self.height = 0

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self)


class AVLTree(object):
    def __init__(self, key=None):
        self.root = None
        self.key = key or default_key

    def _to_str(self, root: Optional[AVLTreeNode]):
        if not root:
            return "Empty"
        return "{%r: [%s, %s]}" % (root.data, self._to_str(root.left), self._to_str(root.right))

    def __str__(self):
        return self._to_str(self.root)

    def __repr__(self):
        return str(self)


def avl_node_height(node: Optional[AVLTreeNode]):
    if not node:
        return -1
    return node.height


def avl_update_node_height(node: AVLTreeNode):
    node.height = max(avl_node_height(node.left), avl_node_height(node.right)) + 1


def avl_right_rotation(avl: AVLTree, node: AVLTreeNode):
    p = node.parent
    l = node.left
    node.parent = l
    if not p:
        avl.root = l
    elif node == p.left:
        p.left = l
    else:
        p.right = l
    l.parent = p

    node.left = l.right
    if l.right:
        l.right.parent = node
    l.right = node
    avl_update_node_height(node)
    avl_update_node_height(l)


def avl_left_rotation(avl: AVLTree, node: AVLTreeNode):
    p = node.parent
    r = node.right
    node.parent = r
    if not p:
        avl.root = r
    elif node == p.left:
        p.left = r
    else:
        p.right = r
    r.parent = p

    node.right = r.left
    if r.left:
        r.left.parent = node
    r.left = node
    avl_update_node_height(node)
    avl_update_node_height(r)


def avl_balance(avl: AVLTree, node: AVLTreeNode):
    """Problem 13-3(b)"""
    lh = avl_node_height(node.left)
    rh = avl_node_height(node.right)
    if abs(lh - rh) <= 1:
        avl_update_node_height(node)
        return
    if lh > rh:  # lh - rh == 2
        lr = node.left.right
        ll = node.left.left
        if avl_node_height(lr) > avl_node_height(ll):
            avl_left_rotation(avl, node.left)
        avl_right_rotation(avl, node)
    else:  # rh - lh == 2
        rl = node.right.left
        rr = node.right.right
        if avl_node_height(rl) > avl_node_height(rr):
            avl_right_rotation(avl, node.right)
        avl_left_rotation(avl, node)


def _avl_insert(avl: AVLTree, root: AVLTreeNode, data) -> AVLTreeNode:
    key = avl.key
    if key(data) <= key(root.data):
        if not root.left:
            root.left = AVLTreeNode(data)
            root.left.parent = root
            ret = root.left
        else:
            ret = _avl_insert(avl, root.left, data)
    else:
        if not root.right:
            root.right = AVLTreeNode(data)
            root.right.parent = root
            avl_update_node_height(root)
            ret = root.right
        else:
            ret = _avl_insert(avl, root.right, data)

    avl_balance(avl, root)
    return ret


def avl_insert(avl: AVLTree, data):
    """Problem 13-3(c)"""
    if not avl.root:
        avl.root = AVLTreeNode(data)
        return
    return _avl_insert(avl, avl.root, data)


def avl_pop(avl: AVLTree, k):
    """Modified from BST.basic_ops.bst_pop."""
    node = bst_search(avl, k)
    if not node:
        raise ValueError()
    if not node.left:
        fix_from = node.parent
        bst_transplant(avl, node, node.right)
    elif not node.right:
        fix_from = node.parent
        bst_transplant(avl, node, node.left)
    else:
        min_node = bst_min(node.right)
        right = node.right
        left = node.left
        if right != min_node:
            fix_from = min_node.parent
            bst_transplant(avl, min_node, min_node.right)
            min_node.right = right
            right.parent = min_node
        else:
            fix_from = min_node
        bst_transplant(avl, node, min_node)
        min_node.left = left
        left.parent = min_node

    while fix_from:
        p = fix_from.parent
        avl_balance(avl, fix_from)
        fix_from = p


class TestAVLTree(TestCase):
    def _assert_avl_properties_internal(self, root: AVLTreeNode, key):
        lh = avl_node_height(root.left)
        rh = avl_node_height(root.right)
        self.assertLessEqual(abs(lh - rh), 2)
        self.assertEqual(max(lh, rh) + 1, root.height)
        if root.left:
            self._assert_avl_properties_internal(root.left, key)
            self.assertLessEqual(key(root.left.data), key(root.data))
            self.assertEqual(root.left.parent, root)
        if root.right:
            self._assert_avl_properties_internal(root.right, key)
            self.assertLessEqual(key(root.data), key(root.right.data))
            self.assertEqual(root.right.parent, root)

    def _assert_avl_properties(self, avl: AVLTree):
        if not avl.root:
            return
        self._assert_avl_properties_internal(avl.root, avl.key)

    def test_basic(self):
        avl = AVLTree()
        insertion_seq = (41, 38, 31, 12, 19, 8)
        for i in insertion_seq:
            avl_insert(avl, i)
            self._assert_avl_properties(avl)
        self.assertSequenceEqual(sorted(insertion_seq), list(bst_iter(avl)))

        deletion_seq = (8, 12, 19, 31, 38, 41)
        for i in deletion_seq:
            avl_pop(avl, i)
            self._assert_avl_properties(avl)
        self.assertSequenceEqual((), list(bst_iter(avl)))

    def test_rand_insertions(self):
        avl = AVLTree()
        insertion_seq = list(range(1, 129))
        rand_permutate(insertion_seq)
        cnt = 0
        for i in insertion_seq:
            avl_insert(avl, i)
            self._assert_avl_properties(avl)
            self.assertSequenceEqual(sorted(insertion_seq[:cnt + 1]), list(bst_iter(avl)))
            cnt += 1
        self.assertSequenceEqual(sorted(insertion_seq), list(bst_iter(avl)))

    def test_special(self):
        avl = AVLTree()
        avl_insert(avl, 793)
        avl_insert(avl, 757)
        avl_pop(avl, 757)
        avl_insert(avl, 604)
        avl_insert(avl, 451)
        avl_insert(avl, 4)
        avl_pop(avl, 604)
        avl_insert(avl, 811)
        avl_insert(avl, 976)
        avl_pop(avl, 793)
        avl_insert(avl, 638)
        avl_insert(avl, 932)
        self._assert_avl_properties(avl)
        avl_pop(avl, 811)
        self._assert_avl_properties(avl)

    def test_rand_insert_delete(self):
        avl = AVLTree()
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
                avl_pop(avl, value)
            else:
                value = insertion_seq[i]
                i += 1
                # print("insert %d" % value)
                values.append(value)
                values.sort()
                avl_insert(avl, value)
            self._assert_avl_properties(avl)
            # print(len(values))
            self.assertSequenceEqual(values, list(bst_iter(avl)))
