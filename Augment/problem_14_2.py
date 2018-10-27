from unittest import TestCase


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


def josephus_simple(n: int, m: int):
    """
    Problem 14-2(a)
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


class TestJosephus(TestCase):
    def test_josephus_simple(self):
        self.assertSequenceEqual([1], josephus_simple(1, 1))
        self.assertSequenceEqual([3, 6, 2, 7, 5, 1, 4], josephus_simple(7, 3))
