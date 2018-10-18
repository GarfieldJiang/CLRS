from unittest import TestCase


class GenericTreeNode(object):
    def __init__(self, child_capacity, data):
        assert isinstance(child_capacity, int) and child_capacity > 0
        self._children = [None for _ in range(0, child_capacity)]
        self._parent = None
        self.data = data

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        assert value is None or type(value) == type(self)
        self._parent = value

    @property
    def child_capacity(self):
        return len(self._children)

    def __getitem__(self, key):
        return self._children[key]

    def __setitem__(self, key, value):
        self._children[key] = value


class BinaryTreeNode(GenericTreeNode):
    def __init__(self, data):
        super().__init__(2, data)

    @property
    def left(self):
        return self[0]

    @left.setter
    def left(self, value):
        assert value is None or type(value) == type(self)
        self[0] = value

    @property
    def right(self):
        return self[1]

    @right.setter
    def right(self, value):
        assert value is None or type(value) == type(self)
        self[1] = value


class TernaryTreeNode(GenericTreeNode):
    def __init__(self, data):
        super().__init__(3, data)

    @property
    def left(self):
        return self[0]

    @left.setter
    def left(self, value):
        assert value is None or type(value) == type(self)
        self[0] = value

    @property
    def middle(self):
        return self[1]

    @middle.setter
    def middle(self, value):
        assert value is None or type(value) == type(self)
        self[1] = value

    @property
    def right(self):
        return self[2]

    @right.setter
    def right(self, value):
        assert value is None or type(value) == type(self)
        self[2] = value


def pre_order_traverse_tree(root, visit):
    if not root:
        return

    visit(root)
    for i in range(0, root.child_capacity):
        pre_order_traverse_tree(root[i], visit)


class TestTree(TestCase):
    def test_pre_order_traverse_ternary_tree(self):
        root = TernaryTreeNode(1)

        left = TernaryTreeNode(2)
        root.left = left
        left.parent = root
        node_3 = TernaryTreeNode(3)
        node_4 = TernaryTreeNode(4)
        node_5 = TernaryTreeNode(5)
        left.left = node_3
        node_3.parent = left
        left.middle = node_4
        node_4.parent = left
        left.right = node_5
        node_5.parent = left

        right = TernaryTreeNode(6)
        root.right = right
        right.parent = root
        node_7 = TernaryTreeNode(7)
        node_8 = TernaryTreeNode(8)
        right.left = node_7
        node_7.parent = right
        right.middle = node_8
        node_8.parent = right

        result = []

        def visit(node):
            result.append(node.data)

        pre_order_traverse_tree(root, visit)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8])
