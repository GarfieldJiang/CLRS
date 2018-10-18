from Common.tree import BinaryTreeNode
from unittest import TestCase


def traverse_binary_tree_with_stack(root: BinaryTreeNode, visit):
    """Exercise 10.4-3. Pre-order. Pointer to parent is NOT needed."""
    assert visit
    s = []
    node = root
    while node or s:
        if node:
            visit(node)
            s.append(node)
            node = node.left
        else:
            node = s.pop()
            node = node.right


def traverse_binary_tree_in_place(root: BinaryTreeNode, visit):
    """Exercise 10.4-5. Pre-order. Pointer to parent is very much needed."""
    assert visit
    node = root
    from_top = 0
    from_left = 1
    from_right = 2
    state = from_top
    while node:
        if state == from_top:
            visit(node)
            if node.left:
                node = node.left
            else:
                state = from_left
        elif state == from_left:
            if node.right:
                node = node.right
                state = from_top
            else:
                state = from_right
        else:  # state == from_right
            parent = node.parent
            if parent:
                if node == parent.left:
                    state = from_left
                if node == parent.right:
                    state = from_right
            node = parent


class TestRootedTree(TestCase):
    def test_traverse_binary_tree_with_stack(self):
        root = BinaryTreeNode(1)
        left = root.left = BinaryTreeNode(2)
        right = root.right = BinaryTreeNode(3)
        left.right = BinaryTreeNode(4)
        right.left = BinaryTreeNode(5)
        right.right = BinaryTreeNode(6)
        right.left.right = BinaryTreeNode(7)
        right.left.right.left = BinaryTreeNode(8)

        array = []
        traverse_binary_tree_with_stack(root, lambda node: array.append(node.data))
        self.assertEqual([1, 2, 4, 3, 5, 7, 8, 6], array)

    def test_traverse_binary_tree_in_place(self):
        root = BinaryTreeNode(1)
        left = root.left = BinaryTreeNode(2)
        left.parent = root
        right = root.right = BinaryTreeNode(3)
        right.parent = root
        left.right = BinaryTreeNode(4)
        left.right.parent = left
        right.left = BinaryTreeNode(5)
        right.left.parent = right
        right.right = BinaryTreeNode(6)
        right.right.parent = right
        right.left.right = BinaryTreeNode(7)
        right.left.right.parent = right.left
        right.left.right.left = BinaryTreeNode(8)
        right.left.right.left.parent = right.left.right

        array = []
        traverse_binary_tree_in_place(root, lambda node: array.append(node.data))
        self.assertEqual([1, 2, 4, 3, 5, 7, 8, 6], array)
