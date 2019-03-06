from P3_DataStructures.RBTree.basic_ops\
    import RBTreeNode, RBTree, rb_insert_raw, rb_insert_fixup, rb_search, rb_pop_raw, rb_pop_fixup, RB_BLACK
from unittest import TestCase


class Interval(object):
    def __init__(self, lo: int, hi: int):
        assert 0 <= lo <= hi < (1 << 16)
        self._lo = lo
        self._hi = hi

    @property
    def lo(self):
        return self._lo

    @property
    def hi(self):
        return self._hi

    @staticmethod
    def are_overlapped(x: 'Interval', y: 'Interval'):
        return x and y and not x.hi < y.lo and not y.hi < x.lo

    def __eq__(self, other):
        if not other:
            return False
        return self.lo == other.lo and self.hi == other.hi

    def __str__(self):
        return "[%d, %d]" % (self.lo, self.hi)

    def __repr__(self):
        return str(self)


class IntervalTreeNodeAug(object):
    def __init__(self, max_hi=None):
        if not max_hi:
            max_hi = -float('inf')
        self.max_hi = max_hi


def interval_default_key(interval: Interval):
    """
    We use this key for the convenience of ex 14.3-5.
    """
    return (interval.lo << 16) + interval.hi


def interval_tree_create():
    """Create an interval tree based on a red-black tree."""
    rbt = RBTree(key=interval_default_key)
    rbt.nil.aug = IntervalTreeNodeAug()
    return rbt


def interval_update_aug_upwards(int_tree: RBTree, node: RBTreeNode):
    while node != int_tree.nil:
        node.aug.max_hi = max(node.left.aug.max_hi, node.right.aug.max_hi, node.data.hi)
        node = node.parent


def interval_on_left_rotation_complete(root: RBTreeNode):
    left = root.left
    root.aug.max_hi = left.aug.max_hi
    left.aug.max_hi = max(left.left.aug.max_hi, left.right.aug.max_hi, left.data.hi)


def interval_on_right_rotation_complete(root: RBTreeNode):
    right = root.right
    root.aug.max_hi = right.aug.max_hi
    right.aug.max_hi = max(right.left.aug.max_hi, right.right.aug.max_hi, right.data.hi)


def interval_insert(int_tree: RBTree, interval: Interval):
    """Insert a interval to the given interval tree."""
    new_node = rb_insert_raw(int_tree, interval)
    new_node.aug = IntervalTreeNodeAug()
    interval_update_aug_upwards(int_tree, new_node)
    rb_insert_fixup(int_tree, new_node, interval_on_left_rotation_complete, interval_on_right_rotation_complete)
    return new_node


def interval_pop(int_tree: RBTree, node: RBTreeNode):
    """Remove a node from the interval tree."""
    color_for_check, fix_from = rb_pop_raw(int_tree, node)
    interval_update_aug_upwards(int_tree, fix_from if fix_from != int_tree.nil else fix_from.parent)
    if color_for_check == RB_BLACK:
        rb_pop_fixup(int_tree, fix_from, interval_on_left_rotation_complete, interval_on_right_rotation_complete)


def interval_search(int_tree: RBTree, interval: Interval):
    """Search an interval in the given interval tree so that it overlaps the given interval."""
    node = int_tree.root
    while node != int_tree.nil and not Interval.are_overlapped(node.data, interval):
        if node.left.aug.max_hi >= interval.lo:
            node = node.left
        else:
            node = node.right
    return node


def _interval_search_min(int_tree: RBTree, root: RBTreeNode, interval: Interval):
    if root == int_tree.nil:
        return int_tree.nil

    overlap_root = Interval.are_overlapped(root.data, interval)
    if root.left.aug.max_hi >= interval.lo:
        ret = _interval_search_min(int_tree, root.left, interval)
        if ret == int_tree.nil and overlap_root:
            ret = root
    else:
        if overlap_root:
            ret = root
        else:
            ret = _interval_search_min(int_tree, root.right, interval)
    return ret


def interval_search_min(int_tree: RBTree, interval: Interval):
    """
    Ex 14.3-3. Search an interval in the given interval tree so that it overlaps the given interval, and among all
    intervals in the tree that overlaps the given interval, the return value has the minimum low endpoint.
    """
    return _interval_search_min(int_tree, int_tree.root, interval)


def interval_search_exactly(int_tree: RBTree, interval: Interval):
    """
    Ex 14.3-5. Search for an interval in the given interval tree that's equal to the given interval.
    """
    return rb_search(int_tree, interval_default_key(interval))


class TestIntervalTree(TestCase):
    def test_basic(self):
        int_tree = interval_tree_create()
        interval_insert(int_tree, Interval(0, 3))
        interval_insert(int_tree, Interval(5, 8))
        interval_insert(int_tree, Interval(6, 10))
        interval_insert(int_tree, Interval(8, 9))
        interval_insert(int_tree, Interval(15, 23))
        interval_insert(int_tree, Interval(16, 21))
        interval_insert(int_tree, Interval(17, 19))
        interval_insert(int_tree, Interval(19, 20))
        interval_insert(int_tree, Interval(25, 30))
        interval_insert(int_tree, Interval(26, 26))

        self.assertEqual(Interval(6, 10), interval_search_exactly(int_tree, Interval(6, 10)).data)
        self.assertEqual(int_tree.nil, interval_search_exactly(int_tree, Interval(10, 12)))

        node = interval_search(int_tree, Interval(10, 12))
        self.assertEqual(Interval(6, 10), node.data)
        node = interval_search_min(int_tree, Interval(10, 12))
        self.assertEqual(Interval(6, 10), node.data)

        node = interval_search(int_tree, Interval(9, 17))
        self.assertTrue(node.data in
                        (Interval(6, 10), Interval(8, 9), Interval(15, 23), Interval(16, 21), Interval(17, 19)))
        node = interval_search_min(int_tree, Interval(9, 17))
        self.assertEqual(Interval(6, 10), node.data)

        node = interval_search_min(int_tree, Interval(17, 19))
        self.assertEqual(Interval(15, 23), node.data)

        node = interval_search(int_tree, Interval(12, 14))
        self.assertEqual(int_tree.nil, node)
        node = interval_search_min(int_tree, Interval(12, 14))
        self.assertEqual(int_tree.nil, node)

        node = interval_search(int_tree, Interval(31, 100))
        self.assertEqual(int_tree.nil, node)
        node = interval_search_min(int_tree, Interval(31, 100))
        self.assertEqual(int_tree.nil, node)

        interval_pop(int_tree, rb_search(int_tree, interval_default_key(Interval(15, 23))))
        node = interval_search_min(int_tree, Interval(17, 19))
        self.assertEqual(Interval(16, 21), node.data)

        interval_pop(int_tree, rb_search(int_tree, interval_default_key(Interval(0, 3))))
        node = interval_search(int_tree, Interval(0, 3))
        self.assertEqual(int_tree.nil, node)
        node = interval_search_min(int_tree, Interval(0, 3))
        self.assertEqual(int_tree.nil, node)