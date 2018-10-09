from Common.tree import BinaryTreeNode
from Common.common import default_key


class _BinaryTreeNode(BinaryTreeNode):
    def __init__(self, val):
        super().__init__()
        self.value = val


class BST(object):
    def __init__(self, key):
        self._root = None
        self._key = key or default_key

    @staticmethod
    def _min(root):
        if not root:
            raise ValueError('Empty tree.')
        ret = root.value
        root = root.left
        while root:
            ret = root.value
            root = root.left
        return ret

    @staticmethod
    def _max(root):
        if not root:
            raise ValueError('Empty tree.')
        ret = root.value
        root = root.right
        while root:
            ret = root.value
            root = root.right
        return ret

    def min(self):
        return BST._min(self._root)

    def max(self):
        return BST._max(self._root)

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
            min_node = BST._min(node)
            r = node.right
            l = node.left
            if r != min_node:
                self._transplant(min_node, min_node.right)
                min_node.right = r
                r.parent = min_node
            self._transplant(node, min_node)
            min_node.left = l
            l.parent = min_node

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
