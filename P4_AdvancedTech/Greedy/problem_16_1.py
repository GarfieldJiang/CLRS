from unittest import TestCase
from collections import namedtuple


def dp_coin_change(target, denominations):
    """
    DP method which works in O(nk) time. This is very much like the rod cutting problem in section
    15.1.
    :param target: the target value in cents.
    :param denominations: coin denominations in increasing order starting with the penny.
    :return: the optimal coin count needed for the target value.
    """
    assert isinstance(target, int) and target >= 0
    assert denominations[0] == 1
    k = len(denominations)
    for i in range(1, k):
        assert isinstance(denominations[i], int) and denominations[i] > denominations[i - 1]
    n = target
    dp = [i for i in range(0, n + 1)]
    for i in range(1, n + 1):
        for j in range(k - 1, -1, -1):
            if denominations[j] > i:
                continue
            if dp[i - denominations[j]] + 1 < dp[i]:
                dp[i] = dp[i - denominations[j]] + 1
    return dp[n]


class TestCoinChange(TestCase):
    def test_dp_coin_change(self):
        case_class = namedtuple('Case', 'desc target denominations coin_count')
        cases = (
            case_class(desc='Zero', target=0, denominations=(1,), coin_count=0),
            case_class(desc='1,5,10,25 #0', target=4, denominations=(1, 5, 10, 25), coin_count=4),
            case_class(desc='1,5,10,25 #1', target=7, denominations=(1, 5, 10, 25), coin_count=3),
            case_class(desc='1,5,10,25 #2', target=10, denominations=(1, 5, 10, 25), coin_count=1),
            case_class(desc='1,5,10,25 #3', target=21, denominations=(1, 5, 10, 25), coin_count=3),
            case_class(desc='1,5,10,25 #4', target=33, denominations=(1, 5, 10, 25), coin_count=5),
            case_class(desc='1,3,4 #0', target=6, denominations=(1, 3, 4), coin_count=2),
            case_class(desc='1,3,4 #1', target=7, denominations=(1, 3, 4), coin_count=2),
        )

        for case in cases:
            coin_count = dp_coin_change(case.target, case.denominations)
            self.assertEqual(coin_count, case.coin_count,
                             msg='desc, %s != %s' % (coin_count, case.coin_count))

