from collections import deque
from unittest import TestCase


class StackByQueue(object):
    """
    Ex 10.1-7.
    """
    def __init__(self):
        self._q1 = deque()
        self._q2 = deque()

    def __len__(self):
        return len(self._q1)

    def push(self, x):
        self._q1.append(x)

    def pop(self):
        q1 = self._q1
        if not q1:
            raise IndexError()

        q2 = self._q2
        while len(q1) > 1:
            q2.append(q1.popleft())
        ret = q1.popleft()
        self._q1, self._q2 = q2, q1
        return ret

    def top(self):
        q1 = self._q1
        if not q1:
            raise IndexError()

        q2 = self._q2
        while len(q1) > 1:
            q2.append(q1.popleft())
        ret = q1.popleft()
        q2.append(ret)
        self._q1, self._q2 = q2, q1
        return ret


class TestStackAndQueue(TestCase):
    def test_stack_by_queue(self):
        array = (1, 2, 3, 4, 5, 6)
        stack = StackByQueue()
        for i in range(len(array)):
            stack.push(array[i])
            self.assertEqual(i + 1, len(stack))
        for i in range(len(array)):
            popped = stack.pop()
            self.assertEqual(len(array) - i - 1, len(stack))
            self.assertEqual(len(array) - i, popped)
        self.assertEqual(0, len(stack))
        for i in range(len(array)):
            stack.push(array[i])
            self.assertEqual(i + 1, len(stack))
        for i in range(len(array)):
            top = stack.top()
            self.assertEqual(len(array) - i, top)
            stack.pop()
        self.assertEqual(0, len(stack))
