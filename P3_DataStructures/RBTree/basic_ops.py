from Common.tree import BinaryTreeNode
from Common.common import default_key, rand_permutate
from unittest import TestCase
from random import uniform, randint
from typing import Callable, Optional


RB_BLACK = True
RB_RED = False


class RBTreeNode(BinaryTreeNode):
    def __init__(self, data, color: bool):
        super().__init__(data)
        self.color = color

        # For convenience of code reuse.
        self.aug = None


class RBTree(object):
    def __init__(self, key=None):
        nil = self.nil = RBTreeNode(None, RB_BLACK)
        nil.left = nil.right = nil.parent = nil
        self.key = key or default_key
        self.root = nil
        # Problem 13-2(a)
        self.bh = 0


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


def rb_iter_reversed(rbt: RBTree):
    if rbt.root == rbt.nil:
        return
    node = rb_max(rbt, rbt.root)
    while node != rbt.nil:
        yield(node.data)
        node = rb_predecessor(rbt, node)


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


def rb_left_rotate(rbt, node, on_complete):
    r = node.right
    p = node.parent
    r.parent = p
    if p != rbt.nil:
        if node == p.left:
            p.left = r
        else:
            p.right = r
    node.parent = r
    node.right = r.left
    node.right.parent = node
    r.left = node
    if node == rbt.root:
        rbt.root = r
    if on_complete:
        on_complete(r)


def rb_right_rotate(rbt, node, on_complete):
    l = node.left
    p = node.parent
    l.parent = p
    if p != rbt.nil:
        if node == p.left:
            p.left = l
        else:
            p.right = l
    node.parent = l
    node.left = l.right
    node.left.parent = node
    l.right = node
    if node == rbt.root:
        rbt.root = l
    if on_complete:
        on_complete(l)


def rb_insert_fixup(rbt: RBTree, node: RBTreeNode,
                    on_left_rotation_complete: Optional[Callable[[RBTreeNode], None]]=None,
                    on_right_rotation_complete: Optional[Callable[[RBTreeNode], None]]=None):
    # If the newly added node becomes the root, then its parent is nil (and therefore black).
    while node.parent.color == RB_RED:  # Red node has a red parent, so needs fixing.
        # Grandparent exists since parent is red. And of course grand parent is black.
        gparent = node.parent.parent
        if node.parent == gparent.left:
            uncle = gparent.right
            if uncle.color == RB_RED:
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
                node.parent.color = uncle.color = RB_BLACK
                gparent.color = RB_RED
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
                    rb_left_rotate(rbt, node, on_left_rotation_complete)
                # Case 3:
                #
                #               GP                        P
                #             /    \                    /   \
                #            p      U    -->  node --> x     gp
                #           / \    / \                      /  \
                # node --> x   A                           A    U
                #
                node.parent.color = RB_BLACK
                gparent.color = RB_RED
                rb_right_rotate(rbt, gparent, on_right_rotation_complete)
        else:  # Symmetric to the corresponding if block
            uncle = gparent.left
            if uncle.color == RB_RED:
                node.parent.color = uncle.color = RB_BLACK
                gparent.color = RB_RED
                node = gparent
            else:
                if node == node.parent.left:
                    node = node.parent
                    rb_right_rotate(rbt, node, on_right_rotation_complete)
                node.parent.color = RB_BLACK
                gparent.color = RB_RED
                rb_left_rotate(rbt, gparent, on_left_rotation_complete)

    # Fix the color of the root node.
    if rbt.root.color == RB_RED:
        rbt.bh += 1
        rbt.root.color = RB_BLACK


def rb_insert(rbt: RBTree, data) -> RBTreeNode:
    new_node = rb_insert_raw(rbt, data)
    rb_insert_fixup(rbt, new_node)
    return new_node


def rb_insert_raw(rbt: RBTree, data) -> RBTreeNode:
    new_node = RBTreeNode(data, RB_RED)
    node = rbt.root
    key = rbt.key
    p = rbt.nil
    k = key(data)
    while node != rbt.nil:
        p = node
        node_key = key(node.data)
        if k <= node_key:
            node = node.left
        elif k > node_key:
            node = node.right
    new_node.left = new_node.right = new_node.parent = rbt.nil
    if p == rbt.nil:
        rbt.root = new_node
    elif k <= key(p.data):
        p.left = new_node
    else:
        p.right = new_node
    new_node.parent = p
    return new_node


def rb_transplant(rbt: RBTree, u: RBTreeNode, v: RBTreeNode):
    """
    The red-black tree version of transplant operation. Replacing the subtree rooted at u with that rooted at v.
    When v == rbt.nil, its parent will also be set to u.parent.
    :param rbt:
    :param u:
    :param v: Can be rbt.nil.
    :return:
    """
    if u == rbt.root:
        rbt.root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v

    # Even if v is rbt.nil, its parent will also be set. The function _rb_pop_fixup will utilize this.
    v.parent = u.parent


def rb_pop_fixup(rbt: RBTree, node: RBTreeNode,
                 on_left_rotation_complete: Optional[Callable[[RBTreeNode], None]]=None,
                 on_right_rotation_complete: Optional[Callable[[RBTreeNode], None]]=None):
    exit_from_case_2 = True
    while node != rbt.root and node.color == RB_BLACK:
        p = node.parent
        if node == p.left:
            sibling = p.right
            assert sibling != rbt.nil
            if sibling.color == RB_RED:
                sibling.color = RB_BLACK
                p.color = RB_RED
                rb_left_rotate(rbt, p, on_left_rotation_complete)
                p = node.parent
                sibling = p.right
                # print('left case 1')
            if sibling.left.color == RB_BLACK and sibling.right.color == RB_BLACK:
                sibling.color = RB_RED
                node = node.parent
                # print('left case 2')
            else:
                if sibling.right.color == RB_BLACK:
                    sibling.left.color = RB_BLACK
                    sibling.color = RB_RED
                    rb_right_rotate(rbt, sibling, on_right_rotation_complete)
                    sibling = sibling.parent
                    # print('left case 3')
                sibling.right.color = RB_BLACK
                sibling.color = p.color
                p.color = RB_BLACK
                rb_left_rotate(rbt, p, on_left_rotation_complete)
                node = rbt.root
                exit_from_case_2 = False
                # print('left case 4')
        else:
            sibling = p.left
            assert sibling != rbt.nil
            if sibling.color == RB_RED:
                sibling.color = RB_BLACK
                p.color = RB_RED
                rb_right_rotate(rbt, p, on_right_rotation_complete)
                p = node.parent
                sibling = p.left
                # print('right case 1')
            if sibling.right.color == RB_BLACK and sibling.left.color == RB_BLACK:
                sibling.color = RB_RED
                node = node.parent
                # print('right case 2')
            else:
                if sibling.left.color == RB_BLACK:
                    sibling.right.color = RB_BLACK
                    sibling.color = RB_RED
                    rb_left_rotate(rbt, sibling, on_left_rotation_complete)
                    sibling = sibling.parent
                    # print('right case 3')
                sibling.left.color = RB_BLACK
                sibling.color = p.color
                p.color = RB_BLACK
                rb_right_rotate(rbt, p, on_right_rotation_complete)
                node = rbt.root
                exit_from_case_2 = False
                # print('right case 4')

    if rbt.root == rbt.nil or (exit_from_case_2 and node.color == RB_BLACK):
        rbt.bh -= 1
    node.color = RB_BLACK


def rb_pop(rbt: RBTree, node: RBTreeNode):
    """
    Pop (delete) a node from a red-black tree.
    :param rbt:
    :param node:
    :return:
    """
    color_for_check, fix_from = rb_pop_raw(rbt, node)
    if color_for_check == RB_BLACK:
        rb_pop_fixup(rbt, fix_from)


def rb_pop_raw(rbt, node):
    color_for_check = node.color
    if node.left == rbt.nil:
        fix_from = node.right
        rb_transplant(rbt, node, node.right)
    elif node.right == rbt.nil:
        fix_from = node.left
        rb_transplant(rbt, node, node.left)
    else:
        y = rb_min(rbt, node.right)
        color_for_check = y.color
        fix_from = y.right
        if y.parent == node:
            fix_from.parent = y
        else:
            rb_transplant(rbt, y, y.right)
            y.right = node.right
            y.right.parent = y
        rb_transplant(rbt, node, y)
        y.color = node.color
        y.left = node.left
        y.left.parent = y
    return color_for_check, fix_from


def rb_black_height(rbt: RBTree, node: RBTreeNode):
    """
    Check and return the black height of a node in a red-black tree.
    :param rbt:
    :param node:
    :return: The black height of node.
    """
    if node == rbt.nil:
        return 0
    lh = rb_black_height(rbt, node.left) + (1 if node.left.color == RB_BLACK else 0)
    rh = rb_black_height(rbt, node.right) + (1 if node.right.color == RB_BLACK else 0)
    if lh != rh:
        raise AssertionError("Left and right subtree have different black height values.")
    return lh


def _rb_assert_properties(rbt: RBTree, node: RBTreeNode):
    assert node.color in (RB_RED, RB_BLACK)

    if node.color == RB_RED:
        assert node.left.color == RB_BLACK
        assert node.right.color == RB_BLACK
    if node.left != rbt.nil:
        _rb_assert_properties(rbt, node.left)
    if node.right != rbt.nil:
        _rb_assert_properties(rbt, node.right)


def rb_assert_properties(rbt: RBTree):
    node = rbt.root
    assert node.color == RB_BLACK
    assert rbt.nil.left == rbt.nil
    assert rbt.nil.right == rbt.nil
    bh = rb_black_height(rbt, rbt.root)
    assert rbt.bh == bh, "%d != %d" % (rbt.bh, bh)
    _rb_assert_properties(rbt, rbt.root)


def rb_node_count(rbt: RBTree, node: RBTreeNode):
    if node == rbt.nil:
        return 0
    return 1 + rb_node_count(rbt, node.left) + rb_node_count(rbt, node.right)


class TestRBTreeBasicOps(TestCase):
    def test_basic(self):
        rbt = RBTree()
        insertion_seq = (41, 38, 31, 12, 19, 8)
        for i in insertion_seq:
            rb_insert(rbt, i)
            rb_assert_properties(rbt)
        self.assertSequenceEqual(sorted(insertion_seq), list(rb_iter(rbt)))

        deletion_seq = (8, 12, 19, 31, 38, 41)
        for i in deletion_seq:
            node = rb_search(rbt, i)
            rb_pop(rbt, node)
            rb_assert_properties(rbt)
        self.assertSequenceEqual((), list(rb_iter(rbt)))

    def test_rand_insert_delete(self):
        rbt = RBTree()
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
                node = rb_search(rbt, value)
                rb_pop(rbt, node)
            else:
                value = insertion_seq[i]
                i += 1
                # print("insert %d" % value)
                values.append(value)
                values.sort()
                rb_insert(rbt, value)
            rb_assert_properties(rbt)
            node_count = rb_node_count(rbt, rbt.root)
            self.assertEqual(len(values), node_count)
            self.assertSequenceEqual(values, list(rb_iter(rbt)))
