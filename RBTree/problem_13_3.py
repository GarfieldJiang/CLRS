from Common.tree import BinaryTreeNode
from Common.common import default_key, rand_permutate
from typing import Optional
from unittest import TestCase
from BST.basic_ops import bst_iter


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


def _avl_insert(avl: AVLTree, root: AVLTreeNode, data, allow_dup_keys) -> Optional[AVLTreeNode]:
    key = avl.key
    if key(data) == key(root.data) and not allow_dup_keys:
        return root
    ret = None
    if key(data) <= key(root.data):
        if not root.left:
            root.left = AVLTreeNode(data)
            root.left.parent = root
        else:
            ret = _avl_insert(avl, root.left, data, allow_dup_keys)
    else:
        if not root.right:
            root.right = AVLTreeNode(data)
            root.right.parent = root
            avl_update_node_height(root)
        else:
            ret = _avl_insert(avl, root.right, data, allow_dup_keys)
    if not ret:
        avl_balance(avl, root)
    return ret


def avl_insert(avl: AVLTree, data, allow_dup_keys=False):
    """Problem 13-3(c)"""
    if not avl.root:
        avl.root = AVLTreeNode(data)
        return
    return _avl_insert(avl, avl.root, data, allow_dup_keys)


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
            self.assertTrue(avl_insert(avl, i) is None)
            self.assertEqual(i, avl_insert(avl, i).data)
            self._assert_avl_properties(avl)
        self.assertSequenceEqual(sorted(insertion_seq), list(bst_iter(avl)))

    def test_rand_insertions(self):
        avl = AVLTree()
        insertion_seq = list(range(1, 129))
        rand_permutate(insertion_seq)
        cnt = 0
        for i in insertion_seq:
            self.assertTrue(avl_insert(avl, i) is None)
            self.assertEqual(i, avl_insert(avl, i).data)
            self._assert_avl_properties(avl)
            self.assertSequenceEqual(sorted(insertion_seq[:cnt + 1]), list(bst_iter(avl)))
            cnt += 1
        self.assertSequenceEqual(sorted(insertion_seq), list(bst_iter(avl)))
