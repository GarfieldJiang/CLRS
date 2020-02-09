from unittest import TestCase


def modular_exp_l2r(a: int, b: int, n: int):
    assert a > 0
    bit_limit = 32
    assert 0 <= b < (1 << bit_limit)
    assert n > 1
    res = 1
    for i in range(bit_limit - 1, -1, -1):
        res = (res * res) % n
        if ((1 << i) & b) == (1 << i):
            res = (res * a) % n
    return res


def modular_exp_r2l(a: int, b: int, n: int):
    assert a > 0
    bit_limit = 32
    assert 0 <= b < (1 << bit_limit)
    assert n > 1
    d = a
    res = 1
    for i in range(0, bit_limit):
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
