from unittest import TestCase


class GenericTreeNode(object):
    def __init__(self, child_capacity):
        assert isinstance(child_capacity, int) and child_capacity > 0
        self._children = [None for _ in range(0, child_capacity)]
        self._parent = None

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
    def __init__(self):
        super(BinaryTreeNode, self).__init__(2)

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
    def __init__(self):
        super(TernaryTreeNode, self).__init__(3)

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
    class TernaryTreeNodeWithValue(TernaryTreeNode):
        def __init__(self, value):
            super(TestTree.TernaryTreeNodeWithValue, self).__init__()
            self._value = value

        @property
        def value(self):
            return self._value

    def test_pre_order_traverse_ternary_tree(self):
        root = self.TernaryTreeNodeWithValue(1)

        left = self.TernaryTreeNodeWithValue(2)
        root.left = left
        left.parent = root
        node_3 = self.TernaryTreeNodeWithValue(3)
        node_4 = self.TernaryTreeNodeWithValue(4)
        node_5 = self.TernaryTreeNodeWithValue(5)
        left.left = node_3
        node_3.parent = left
        left.middle = node_4
        node_4.parent = left
        left.right = node_5
        node_5.parent = left

        right = self.TernaryTreeNodeWithValue(6)
        root.right = right
        right.parent = root
        node_7 = self.TernaryTreeNodeWithValue(7)
        node_8 = self.TernaryTreeNodeWithValue(8)
        right.left = node_7
        node_7.parent = right
        right.middle = node_8
        node_8.parent = right

        result = []

        def visit(node):
            result.append(node.value)

        pre_order_traverse_tree(root, visit)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8])
