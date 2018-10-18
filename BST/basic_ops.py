from Common.tree import BinaryTreeNode
from Common.common import default_key
from unittest import TestCase


class BST(object):
    def __init__(self, key=None):
        self.root = None
        self.key = key or default_key


def bst_min(root):
    if not root:
        raise ValueError('Empty tree.')
    while root.left:
        root = root.left
    return root


def bst_max(root):
    if not root:
        raise ValueError('Empty tree.')
    while root.right:
        root = root.right
    return root


def bst_successor(node):
    if node.right:
        return bst_min(node.right)
    while node:
        if node.parent and node == node.parent.left:
            return node.parent
        node = node.parent
    return None


def bst_predecessor(node):
    if node.left:
        return bst_max(node.left)
    while node:
        if node.parent and node == node.parent.right:
            return node.parent
        node = node.parent
    return None


def bst_search(bst, k):
    node = bst.root
    key = bst.key
    if not node:
        return None
    while node:
        if k == key(node.data):
            return node
        if k < key(node.data):
            node = node.left
        else:
            node = node.right
    return None


def bst_insert(bst, data):
    if data is None:
        raise ValueError('None')
    node = bst.root
    new_node = BinaryTreeNode(data)
    key = bst.key
    p = None
    while node:
        p = node
        key_node = key(node.data)
        if key(data) < key_node:
            node = node.left
        else:
            node = node.right
    if not p:
        bst.root = new_node
    elif key(data) < key(p.data):
        p.left = new_node
    else:
        p.right = new_node
    new_node.parent = p


def bst_pop(bst, k):
    node = bst_search(bst, k)
    if not node:
        raise ValueError()
    if not node.left:
        bst_transplant(bst, node, node.right)
    elif not node.right:
        bst_transplant(bst, node, node.left)
    else:
        min_node = bst_min(node.right)
        right = node.right
        left = node.left
        if right != min_node:
            bst_transplant(bst, min_node, min_node.right)
            min_node.right = right
            right.parent = min_node
        bst_transplant(bst, node, min_node)
        min_node.left = left
        left.parent = min_node


def bst_transplant(bst, u, v):
    up = u.parent
    u.parent = None
    if not up:
        bst.root = v
    elif u == up.left:
        up.left = v
    else:
        up.right = v
    if v:
        v.parent = up


def bst_iter(bst):
    if not bst.root:
        return
    node = bst_min(bst.root)
    while node:
        yield(node.data)
        node = bst_successor(node)


def bst_iter_reversed(bst):
    if not bst.root:
        return
    node = bst_max(bst.root)
    while node:
        yield(node.data)
        node = bst_predecessor(node)


class TestBST(TestCase):
    def test_basic(self):
        bst = BST()
        bst_insert(bst, 12)
        bst_insert(bst, 5)
        bst_insert(bst, 2)
        bst_insert(bst, 9)
        bst_insert(bst, 18)
        bst_insert(bst, 15)
        bst_insert(bst, 19)
        bst_insert(bst, 17)
        self.assertListEqual(list(bst_iter(bst)), [2, 5, 9, 12, 15, 17, 18, 19])
        bst_insert(bst, 13)
        self.assertListEqual(list(bst_iter(bst)), [2, 5, 9, 12, 13, 15, 17, 18, 19])
        self.assertListEqual(list(bst_iter_reversed(bst)), [19, 18, 17, 15, 13, 12, 9, 5, 2])
        self.assertEqual(2, bst_min(bst.root).data)
        self.assertEqual(19, bst_max(bst.root).data)
        self.assertIsNotNone(bst_search(bst, 5))
        self.assertIsNotNone(bst_search(bst, 5))
        self.assertIsNotNone(bst_search(bst, 19))
        self.assertIsNone(bst_search(bst, 20))
        self.assertRaises(ValueError, lambda: bst_pop(bst, 20))
        bst_pop(bst, 9)
        self.assertListEqual(list(bst_iter_reversed(bst)), [19, 18, 17, 15, 13, 12, 5, 2])
        self.assertIsNone(bst_search(bst, 9))
        bst_pop(bst, 5)
        self.assertListEqual(list(bst_iter(bst)), [2, 12, 13, 15, 17, 18, 19])
        self.assertEqual(12, bst.root.data)
        bst_pop(bst, 12)
        self.assertListEqual(list(bst_iter(bst)), [2, 13, 15, 17, 18, 19])
        self.assertEqual(13, bst.root.data)
        bst_pop(bst, 15)
        bst_pop(bst, 17)
        self.assertListEqual(list(bst_iter(bst)), [2, 13, 18, 19])
        bst_pop(bst, 18)
        self.assertListEqual(list(bst_iter(bst)), [2, 13, 19])
        bst_pop(bst, 13)
        self.assertEqual(19, bst.root.data)
        bst_pop(bst, 2)
        bst_pop(bst, 19)
        self.assertIsNone(bst.root)
