from unittest import TestCase


def _count_bits(n: int):
    assert n >= 0
    b = 0
    while n != 0:
        n = n >> 1
        b = b + 1
    return b


def modular_exp_l2r(a: int, b: int, n: int):
    assert a > 0
    assert n > 1
    res = 1
    for i in range(_count_bits(n) - 1, -1, -1):
        res = (res * res) % n
        if ((1 << i) & b) == (1 << i):
            res = (res * a) % n
    return res


def modular_exp_r2l(a: int, b: int, n: int):
    assert a > 0
    assert n > 1
    d = a
    res = 1
    for i in range(0, _count_bits(n)):
        if ((1 << i) & b) == (1 << i):
            res = (res * d) % n
        d = (d * d) % n
    return res


class TestPower(TestCase):
    def test_modular_exp(self):
        cases = (
            (2, 9, 11, 6),
            (2, 15, 11, 10),
        )

        for case in cases:
            a, b, n, expected_result = case
            for method in (modular_exp_l2r, modular_exp_r2l):
                result = method(a, b, n)
                self.assertEqual(expected_result, result)
