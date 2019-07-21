from unittest import TestCase


def extended_euclid(a: int, b: int):
    assert(a >= 0)
    assert(b >= 0)
    stack = [a]
    while b != 0:
        a, b = b, a % b
        stack.append(a)
    d = a
    x, y = 1, 0
    a = stack.pop()
    while stack:
        b = a
        a = stack.pop()
        new_x, new_y = y, x - y * (a // b)
        x, y = new_x, new_y
    return d, x, y


class TestGCD(TestCase):
    def test_euclid(self):
        cases = (
            (0, 0, 0),
            (1, 0, 1),
            (0, 5, 5),
            (500, 300, 100),
            (99, 78, 3)
        )
        for case in cases:
            a = case[0]
            b = case[1]
            expected_d = case[2]
            d, x, y = extended_euclid(a, b)
            self.assertEqual(expected_d, d)
            self.assertEqual(expected_d, a * x + b * y)
