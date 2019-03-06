from unittest import TestCase
from P3_DataStructures.Augment import dynamic_order_statistics as os


class LinkedListNode(object):
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


def make_loop(n):
    h = LinkedListNode(1)
    x = h
    for i in range(2, n + 1):
        x.next = LinkedListNode(i)
        x.next.prev = x
        x = x.next
    x.next = h
    h.prev = x
    return h


def josephus_a(n: int, m: int):
    """
    Problem 14-2(a). O(mn) time.
    """
    assert n > 0
    assert 0 < m <= n

    h = make_loop(n)

    ret = []
    last = h.prev
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            last = last.next
        ret.append(last.data)
        last = last.prev
        last.next = last.next.next
        last.next.prev = last

    return ret


def josephus_b(n: int, m: int):
    """
    Problem 14-2(b). O(n\lg n) time.
    """
    assert n > 0
    assert 0 < m <= n

    ost = os.os_tree_create()
    for i in range(1, n + 1):
        os.os_insert(ost, i)

    ret = []
    rank = m
    for i in range(1, n + 1):
        node = os.os_select(ost, rank)
        ret.append(node.data)
        os.os_pop(ost, node)
        if i < n:
            rank = (rank + m - 2) % (n - i) + 1

    return ret


class TestJosephus(TestCase):
    def test_josephus(self):
        for josephus in (josephus_a, josephus_b):
            self.assertSequenceEqual([1], josephus(1, 1))
            self.assertSequenceEqual([3, 6, 2, 7, 5, 1, 4], josephus(7, 3))
