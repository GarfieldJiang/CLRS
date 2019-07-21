from unittest import TestCase
from typing import Sequence, List


def extended_euclid(a: int, b: int):
    """Extended Euclid algorithm for 2 non-negative integers."""
    assert (a >= 0)
    assert (b >= 0)
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


def _gcd_internal(seq: Sequence[int], coefs: List[int], n: int):
    if n == 2:
        d, x, y = extended_euclid(seq[0], seq[1])
        coefs[0] = x
        coefs[1] = y
        return d

    old_d = _gcd_internal(seq, coefs, n - 1)
    new_d, x, y = extended_euclid(seq[n - 1], old_d)
    coefs[n - 1] = x
    for i in range(n - 1):
        coefs[i] *= y
    return new_d


def gcd(seq: Sequence[int]):
    """Ex 31.2-7. GCD algorithm for multiple non-negative integers"""
    n = len(seq)
    assert n >= 2
    coefs = [0] * n
    return _gcd_internal(seq, coefs, n), coefs


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

    def test_gcd(self):
        cases = (
            ((1, 2, 3, 4, 5), 1),
            ((5, 3, 2, 4, 1), 1),
            ((125, 75, 85, 35), 5),
            ((312, 542, 798, 324), 2),
            ((624, 3984, 1056, 3000, 240, 224), 8),
        )
        for case in cases:
            seq = case[0]
            expected_d = case[1]
            d, coefs = gcd(seq)
            self.assertEqual(expected_d, d)
            # print(d, seq, coefs)
            self.assertEqual(expected_d, sum(i[0] * i[1] for i in zip(seq, coefs)))
