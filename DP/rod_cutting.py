import unittest


def rod_cutting_memoized(prices, length):
    cached_revenues = [-1] * (length + 1)
    first_pieces = [0] * (length + 1)
    return __rod_cutting_top_down_internal(prices, length, cached_revenues, first_pieces), first_pieces[length]


def __rod_cutting_top_down_internal(prices, length, cached_revenues, first_pieces):
    if cached_revenues[length] >= 0:
        return cached_revenues[length]

    if length <= 0:
        return 0

    revenue = -1

    for i in range(1, length + 1):
        new_val = prices[i] + __rod_cutting_top_down_internal(prices, length - i, cached_revenues, first_pieces)

        if revenue < new_val:
            revenue = new_val
            first_pieces[length] = i

    cached_revenues[length] = revenue
    return revenue


def rod_cutting_bottom_up(prices, length):
    if length <= 0:
        return 0

    first_pieces = [0] * (length + 1)
    cached_revenues = [-1] * (length + 1)
    cached_revenues[0] = 0

    for k in range(1, length + 1):
        revenue = -1

        for i in range(1, k + 1):
            if revenue < prices[i] + cached_revenues[k - i]:
                revenue = prices[i] + cached_revenues[k - i]
                first_pieces[k] = i  # ex 15.1-4

        cached_revenues[k] = revenue

    return cached_revenues[length], first_pieces[length]


# ex 15.1-5
def fibonacci(n):
    assert isinstance(n, int)

    if n < 0:
        return 0

    vals = [0] * (n + 1)
    vals[0] = 1
    if n > 0:
        vals[1] = 1

    for i in range(2, n + 1):
        vals[i] = vals[i - 1] + vals[i - 2]

    return vals[n]


class TestRodCutting(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRodCutting, self).__init__(*args, **kwargs)
        self.prices = (0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30)
        self.revenues = (0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30)
        self.first_pieces = (0, 1, 2, 3, 2, 2, 6, 1, 2, 3, 10)

    def test_top_down(self):
        for length in range(1, len(self.prices)):
            self.assertEqual((self.revenues[length], self.first_pieces[length]),
                             rod_cutting_memoized(self.prices, length))

    def test_bottom_up(self):
        for length in range(1, len(self.prices)):
            self.assertEqual((self.revenues[length], self.first_pieces[length]),
                             rod_cutting_bottom_up(self.prices, length))

    def test_fibonacci(self):
        answers = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)
        for n in range(0, len(answers)):
            self.assertEqual(answers[n], fibonacci(n))
