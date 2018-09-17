from unittest import TestCase


class SLLNode(object):
    """Singly linked list node."""
    def __init__(self, data):
        self.data = data
        self.next = None


class QueueBySLL(object):
    """Ex 10.2-3"""
    def __init__(self):
        self._head = None
        self._tail = None

    def enqueue(self, x):
        node = SLLNode(x)
        if not self._head:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node

    def dequeue(self):
        if not self._head:
            raise ValueError()
        x = self._head
        self._head = self._head.next
        if self._tail == x:
            self._tail = None
        return x.data


class FancyLinkedListNode(object):
    def __init__(self, data):
        self.data = data
        self.np = 0


class FancyLinkedList(object):
    """Ex 10.2-8"""
    def __init__(self):
        self._head = self._tail = None
        self._id_to_node = {}

    def insert(self, x):
        node = FancyLinkedListNode(x)
        self._id_to_node[id(node)] = node
        if self._head:
            node.np = id(self._head)
            self._head.np ^= id(node)
        else:
            self._tail = node
        self._head = node

    def delete(self, x):
        if not self._head:
            return False
        prev_id = 0
        h = self._head
        while h:
            next_id = h.np ^ prev_id
            cur_id = id(h)
            prev_node = None if prev_id == 0 else self._id_to_node[prev_id]
            next_node = None if next_id == 0 else self._id_to_node[next_id]
            if h.data == x:
                if prev_node:
                    prev_node.np ^= cur_id ^ next_id
                if next_node:
                    next_node.np ^= cur_id ^ prev_id
                h.np = 0
                if h == self._head:
                    self._head = next_node
                if h == self._tail:
                    self._tail = prev_node
                self._id_to_node.pop(cur_id)
                return True
            prev_id = cur_id
            h = next_node
        return False

    def to_array(self):
        ret = []
        prev_id = 0
        h = self._head
        while h:
            ret.append(h.data)
            next_id = h.np ^ prev_id
            next_node = None if next_id == 0 else self._id_to_node[next_id]
            prev_id = id(h)
            h = next_node
        return ret

    def search(self, x):
        prev_id = 0
        h = self._head
        while h:
            if h.data == x:
                return h
            next_id = h.np ^ prev_id
            next_node = None if next_id == 0 else self._id_to_node[next_id]
            prev_id = id(h)
            h = next_node
        return None

    def reverse(self):
        self._head, self._tail = self._tail, self._head


class TestLinkedList(TestCase):
    def test_queue_by_sll(self):
        seq = (1, 2, 3, 4, 5, 6)
        q = QueueBySLL()
        for i in range(0, 3):
            q.enqueue(seq[i])
        for i in range(0, 3):
            x = q.dequeue()
            self.assertEqual(seq[i], x)
        for i in range(3, 3):
            q.enqueue(seq[i])
        for i in range(3, 3):
            x = q.dequeue()
            self.assertEqual(seq[i], x)

    def test_fancy_linked_list(self):
        seq = (1, 2, 3, 4, 5, 6)
        ll = FancyLinkedList()
        for i in range(len(seq)):
            ll.insert(seq[i])
            self.assertEqual(seq[0:i + 1][::-1], tuple(ll.to_array()))
        for i in range(len(seq)):
            self.assertEqual(seq[i], ll.search(seq[i]).data)
        self.assertEqual(None, ll.search(7))

        ll.reverse()
        self.assertEqual(seq, tuple(ll.to_array()))

        self.assertEqual(False, ll.delete(0))
        self.assertEqual(True, ll.delete(4))
        self.assertEqual([1, 2, 3, 5, 6], ll.to_array())
        ll.reverse()
        self.assertEqual([6, 5, 3, 2, 1], ll.to_array())
        self.assertEqual(True, ll.delete(6))
        self.assertEqual([5, 3, 2, 1], ll.to_array())
        self.assertEqual(True, ll.delete(1))
        self.assertEqual([5, 3, 2], ll.to_array())
        ll.delete(5)
        ll.delete(2)
        ll.delete(3)
        self.assertEqual([], ll.to_array())

        for i in range(len(seq)):
            ll.insert(seq[i])
            self.assertEqual(seq[0:i + 1][::-1], tuple(ll.to_array()))
        ll.reverse()
        self.assertEqual(seq, tuple(ll.to_array()))
