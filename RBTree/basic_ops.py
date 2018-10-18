from Common.tree import BinaryTreeNode
from Common.common import default_key, rand_permutate
from unittest import TestCase


_BLACK = True
_RED = False


class RBTreeNode(BinaryTreeNode):
    def __init__(self, data, black_or_red: bool):
        super().__init__(data)
        self.black_or_red = black_or_red


class RBTree(object):
    def __init__(self, key=None):
        self.nil = RBTreeNode(None, _BLACK)
        self.key = key or default_key
        self.root = self.nil


def bst_left_rotate(bst, node: BinaryTreeNode):
    r = node.right
    p = node.parent
    r.parent = p
    if p:
        if node == p.left:
            p.left = r
        else:
            p.right = r
    node.parent = r
    node.right = r.left
    node.right.parent = node
    r.left = node
    if node == bst.root:
        bst.root = r


def bst_right_rotate(bst, node: BinaryTreeNode):
    l = node.left
    p = node.parent
    l.parent = p
    if p:
        if node == p.left:
            p.left = l
        else:
            p.right = l
    node.parent = l
    node.left = l.right
    node.left.parent = node
    l.right = node
    if node == bst.root:
        bst.root = l


def rb_min(rbt: RBTree, root: RBTreeNode):
    if root == rbt.nil:
        raise ValueError('Empty tree.')
    while root.left != rbt.nil:
        root = root.left
    return root


def rb_max(rbt: RBTree, root: RBTreeNode):
    if root == rbt.nil:
        raise ValueError('Empty tree.')
    while root.right != rbt.nil:
        root = root.right
    return root


def rb_successor(rbt: RBTree, node: RBTreeNode):
    if node.right != rbt.nil:
        return rb_min(rbt, node.right)
    while node != rbt.nil:
        if node.parent != rbt.nil and node == node.parent.left:
            return node.parent
        node = node.parent
    return rbt.nil


def rb_predecessor(rbt: RBTree, node: RBTreeNode):
    if node.left != rbt.nil:
        return rb_max(rbt, node.left)
    while node != rbt.nil:
        if node.parent != rbt.nil and node == node.parent.right:
            return node.parent
        node = node.parent
    return rbt.nil


def rb_iter(rbt: RBTree):
    if rbt.root == rbt.nil:
        return
    node = rb_min(rbt, rbt.root)
    while node != rbt.nil:
        yield(node.data)
        node = rb_successor(rbt, node)


def bst_iter_reversed(rbt: RBTree):
    if rbt.root == rbt.nil:
        return
    node = rb_max(rbt, rbt.root)
    while node != rbt.nil:
        yield(node.data)
        node = rb_predecessor(node)


def rb_search(rbt: RBTree, k):
    node = rbt.root
    key = rbt.key
    while node != rbt.nil:
        if k == key(node.data):
            return node
        if k < key(node.data):
            node = node.left
        else:
            node = node.right
    return rbt.nil


def _rb_insert_fixup(rbt: RBTree, node: RBTreeNode):
    # If the newly added node becomes the root, then its parent is nil (and therefore black).
    while node.parent.black_or_red == _RED:  # Red node has a red parent, so needs fixing.
        # Grandparent exists since parent is red. And of course grand parent is black.
        gparent = node.parent.parent
        if node.parent == gparent.left:
            uncle = gparent.right
            if uncle.black_or_red == _RED:
                # Case 1:
                #
                #                GP                 gp <-- node
                #              /    \             /    \
                #             p      u    -->    P      U             OR
                #            / \    / \         / \    / \
                #  node --> x                      x
                #
                #                GP                 gp <-- node
                #              /    \             /    \
                #             p      u    -->    P      U
                #            / \    / \         / \    / \
                #      node --> x                  x
                node.parent.black_or_red = uncle.black_or_red = _BLACK
                gparent.black_or_red = _RED
                node = gparent
            else:
                if node == node.parent.right:
                    # Case 2: Convert to Case 3
                    #
                    #             GP                        GP
                    #           /    \                    /    \
                    #          p      U    -->           x      U
                    #         / \    / \                / \    / \
                    #   node --> x            node --> p   B
                    #           / \                   / \
                    #          A   B                     A
                    node = node.parent
                    bst_left_rotate(rbt, node)
                # Case 3:
                #
                #               GP                        P
                #             /    \                    /   \
                #            p      U    -->  node --> x     gp
                #           / \    / \                      /  \
                # node --> x   A                           A    U
                #
                node.parent.black_or_red = _BLACK
                gparent.black_or_red = _RED
                bst_right_rotate(rbt, gparent)
        else:  # Symmetric to the corresponding if block
            uncle = gparent.left
            if uncle.black_or_red == _RED:
                node.parent.black_or_red = uncle.black_or_red = _BLACK
                gparent.black_or_red = _RED
                node = gparent
            else:
                if node == node.parent.left:
                    node = node.parent
                    bst_right_rotate(rbt, node)
                node.parent.black_or_red = _BLACK
                gparent.black_or_red = _RED
                bst_left_rotate(rbt, gparent)

    # Fix the color of the root node.
    rbt.root.black_or_red = True


def rb_insert(rbt: RBTree, data, allow_dup_key=False) -> bool:
    node = rbt.root
    key = rbt.key
    p = rbt.nil
    k = key(data)
    while node != rbt.nil:
        p = node
        node_key = key(node.data)
        if k == node_key and not allow_dup_key:
            return False
        if k <= node_key:
            node = node.left
        elif k > node_key:
            node = node.right

    new_node = RBTreeNode(data, _RED)
    new_node.left = new_node.right = new_node.parent = rbt.nil

    if p == rbt.nil:
        rbt.root = new_node
    elif k <= key(p.data):
        p.left = new_node
    else:
        p.right = new_node
    new_node.parent = p

    _rb_insert_fixup(rbt, new_node)
    return True


def rb_black_height(rbt: RBTree, node: RBTreeNode):
    if node == rbt.nil:
        return 0
    lh = rb_black_height(rbt, node.left) + (1 if node.left.black_or_red == _BLACK else 0)
    rh = rb_black_height(rbt, node.right) + (1 if node.right.black_or_red == _BLACK else 0)
    if lh != rh:
        raise ValueError("Left and right subtree have different black height values.")
    return lh


def _rb_assert_properties(rbt: RBTree, node: RBTreeNode):
    assert node.black_or_red in (_RED, _BLACK)

    if node.black_or_red == _RED:
        assert node.left.black_or_red == _BLACK
        assert node.right.black_or_red == _BLACK
    if node.left != rbt.nil:
        _rb_assert_properties(rbt, node.left)
    if node.right != rbt.nil:
        _rb_assert_properties(rbt, node.right)


def rb_assert_properties(rbt: RBTree):
    node = rbt.root
    assert node.black_or_red == _BLACK
    rb_black_height(rbt, rbt.root)
    _rb_assert_properties(rbt, rbt.root)


class TestRBTreeBasicOps(TestCase):
    def test_basic(self):
        rbt = RBTree()
        insertion_seq = (41, 38, 31, 12, 19, 8)
        for i in insertion_seq:
            rb_insert(rbt, i)
            rb_assert_properties(rbt)
        self.assertSequenceEqual(sorted(insertion_seq), list(rb_iter(rbt)))

    def test_rand_insert(self):
        rbt = RBTree()
        insertion_seq = list(range(1, 100))
        rand_permutate(insertion_seq)
        for i in insertion_seq:
            rb_insert(rbt, i)
            rb_assert_properties(rbt)
        self.assertSequenceEqual(sorted(insertion_seq), list(rb_iter(rbt)))

