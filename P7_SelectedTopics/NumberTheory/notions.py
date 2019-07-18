from unittest import TestCase


def power(a: int, n: int):
    """
    Simple divide-and-conquer method to calculate a to the n'th.
    :param a: base.
    :param n: non-negative power.
    :return:
    """
    if n < 0:
        raise ValueError()
    if n == 0:
        if a == 0:
            raise ValueError()
        return 1
    if n == 1:
        return a
    half = power(a, n // 2)
    return half * half * power(a, n % 2)


def check_power(n: int):
    """
    ex 31.1-8
    :param n: b-bit non-negative integer.
    :return: (x, y) where n = power(x, y) with minimum y and 1 < x < n, or (None, None) if no such expression exists.
    """
    if n <= 0:
        raise ValueError()

    bit_count = 0  # b
    while (n >> bit_count) != 0:  # O(b)
        bit_count += 1

    for k in range(2, bit_count):  # O(b) * inside
        # k and bit_count (b) should be considered as fixed length integers
        lo = 1 << ((bit_count - 1) // k)  # O(b^2)
        q, r = bit_count // k, bit_count % k  # O(b^2)
        if r > 0:
            q = q + 1
        hi = (1 << q) - 1
        while lo <= hi:  # O(b / k) * inside
            mid = lo + ((hi - lo) >> 1)
            num = power(mid, k)  # O(b^2 k log k)
            if num == n:
                return mid, k
            if num > n:
                hi = mid - 1  # O(b)
            else:
                lo = mid + 1  # O(b)

    return None, None


class TestNotions(TestCase):
    def test_check_power(self):
        cases = (
            (4, 2, 2),
            (1, None, None),
            (8, 2, 3),
            (125, 5, 3),
            (16807, 7, 5),
            (2048, 2, 11),
            (99980001, 9999, 2),
            (99980000, None, None),
            (99980002, None, None),
            (9998001, None, None),
            (1171223165167387672982838813062831053, 37, 23),
        )
        for case in cases:
            self.assertEqual((case[1], case[2]), check_power(case[0]))


