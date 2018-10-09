from Common.tree import BinaryTreeNode
from Common.common import default_key
from unittest import TestCase


class _BinaryTreeNode(BinaryTreeNode):
    def __init__(self, val):
        super().__init__()
        self.value = val


class BST(object):
    def __init__(self, key=None):
        self._root = None
        self._key = key or default_key

    def root_value(self):
        if not self._root:
            raise ValueError('Empty tree.')
        return self._root.value

    @staticmethod
    def _min(root):
        if not root:
            raise ValueError('Empty tree.')
        while root.left:
            root = root.left
        return root

    @staticmethod
    def _max(root):
        if not root:
            raise ValueError('Empty tree.')
        while root.right:
            root = root.right
        return root

    def min(self):
        return BST._min(self._root).value

    def max(self):
        return BST._max(self._root).value

    def insert(self, val):
        if val is None:
            raise ValueError('None')
        node = self._root
        new_node = _BinaryTreeNode(val)
        key = self._key
        p = None
        while node:
            p = node
            key_node = key(node.value)
            if key(val) < key_node:
                node = node.left
            else:
                node = node.right
        if not p:
            self._root = new_node
        elif key(val) < key(p.value):
            p.left = new_node
        else:
            p.right = new_node
        new_node.parent = p

    def pop(self, val):
        node = self._search(val)
        if not node:
            raise ValueError()
        if not node.left:
            self._transplant(node, node.right)
        elif not node.right:
            self._transplant(node, node.left)
        else:
            min_node = BST._min(node.right)
            right = node.right
            left = node.left
            if right != min_node:
                self._transplant(min_node, min_node.right)
                min_node.right = right
                right.parent = min_node
            self._transplant(node, min_node)
            min_node.left = left
            left.parent = min_node

    def _search(self, val):
        node = self._root
        key = self._key
        if not node:
            return None
        while node:
            if key(val) == key(node.value):
                return node
            if key(val) < key(node.value):
                node = node.left
            else:
                node = node.right
        return None

    def values(self):
        if not self._root:
            return
        node = BST._min(self._root)
        while node:
            yield(node.value)
            node = BST._next(node)

    def values_reversed(self):
        if not self._root:
            return
        node = BST._max(self._root)
        while node:
            yield(node.value)
            node = BST._prev(node)

    @staticmethod
    def _next(node):
        if node.right:
            return BST._min(node.right)
        while node:
            if node.parent and node == node.parent.left:
                return node.parent
            node = node.parent
        return None

    @staticmethod
    def _prev(node):
        if node.left:
            return BST._max(node.left)
        while node:
            if node.parent and node == node.parent.right:
                return node.parent
            node = node.parent
        return None

    def __contains__(self, val):
        return self._search(val) is not None

    def _transplant(self, u, v):
        """
        Replace subtree rooted at u with subtree rooted at v.
        Will not change v's original parent.
        :param u: Root of subtree to remove.
        :param v: Root of subtree to replace.
        :return:
        """
        up = u.parent
        u.parent = None
        if not up:
            self._root = v
        elif u == up.left:
            up.left = v
        else:
            up.right = v
        if v:
            v.parent = up


class TestBST(TestCase):
    def test_basic(self):
        bst = BST()
        bst.insert(12)
        bst.insert(5)
        bst.insert(2)
        bst.insert(9)
        bst.insert(18)
        bst.insert(15)
        bst.insert(19)
        bst.insert(17)
        self.assertListEqual(list(bst.values()), [2, 5, 9, 12, 15, 17, 18, 19])
        bst.insert(13)
        self.assertListEqual(list(bst.values()), [2, 5, 9, 12, 13, 15, 17, 18, 19])
        self.assertListEqual(list(bst.values_reversed()), [19, 18, 17, 15, 13, 12, 9, 5, 2])
        self.assertEqual(2, bst.min())
        self.assertEqual(19, bst.max())
        self.assertTrue(5 in bst)
        self.assertTrue(18 in bst)
        self.assertTrue(19 in bst)
        self.assertFalse(20 in bst)
        self.assertRaises(ValueError, lambda: bst.pop(20))
        bst.pop(9)
        self.assertListEqual(list(bst.values_reversed()), [19, 18, 17, 15, 13, 12, 5, 2])
        self.assertFalse(9 in bst)
        bst.pop(5)
        self.assertListEqual(list(bst.values()), [2, 12, 13, 15, 17, 18, 19])
        self.assertEqual(12, bst.root_value())
        bst.pop(12)
        self.assertListEqual(list(bst.values()), [2, 13, 15, 17, 18, 19])
        self.assertEqual(13, bst.root_value())
        bst.pop(15)
        bst.pop(17)
        self.assertListEqual(list(bst.values()), [2, 13, 18, 19])
        bst.pop(18)
        self.assertListEqual(list(bst.values()), [2, 13, 19])
        bst.pop(13)
        self.assertEqual(19, bst.root_value())
        bst.pop(2)
        bst.pop(19)
        self.assertRaises(ValueError, lambda: bst.root_value())
