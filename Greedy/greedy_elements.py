import logging
import unittest
from collections import namedtuple


logging.basicConfig(level=logging.WARN)


KnapsackItem = namedtuple('KnapsackItem', 'weight value')


def do_01_knapsack(items, weight_limit):
    """
    Ex 16.2-2. DP solution to the 0-1 knapsack solution working in O(nW) time, where n is len(items) and W is
    weight_limit.
    :param items: list of items to select from.
    :param weight_limit: the weight limit of the knapsack.
    :return: The optimal total value the thief can carry.
    """

    if not items:
        return 0

    n = len(items)
    dp = [[-1 for _ in xrange(0, weight_limit + 1)] for _ in xrange(0, n + 1)]

    for i in xrange(0, n + 1):
        dp[i][0] = 0

    for w in xrange(0, weight_limit + 1):
        dp[0][w] = 0

    for w in xrange(1, weight_limit + 1):
        for i in xrange(1, n + 1):
            no_choose_current = dp[i - 1][w]
            choose_current = 0
            if w >= items[i - 1].weight:
                choose_current = dp[i - 1][w - items[i - 1].weight] + items[i - 1].value
            dp[i][w] = max(no_choose_current, choose_current)

    logging.debug('0-1 knapsack, dp: %s' % dp)
    return dp[n][weight_limit]


class TestGreedyElements(unittest.TestCase):
    def test_01_knapsack(self):
        Case = namedtuple('Case', 'desc items weight_limit expected_opt_value')
        cases = (
            Case(desc='Empty', items=(), weight_limit=100, expected_opt_value=0),
            Case(desc='Single item within limit', items=(KnapsackItem(weight=10, value=5),), weight_limit=10,
                 expected_opt_value=5),
            Case(desc='Single item beyond limit', items=(KnapsackItem(weight=10, value=5),), weight_limit=9,
                 expected_opt_value=0),
            Case(desc='Triple items #0', items=(
                KnapsackItem(weight=10, value=60),
                KnapsackItem(weight=20, value=100),
                KnapsackItem(weight=30, value=120),
            ), weight_limit=50, expected_opt_value=220),
            Case(desc='Triple items #1', items=(
                KnapsackItem(weight=20, value=100),
                KnapsackItem(weight=10, value=60),
                KnapsackItem(weight=30, value=120),
            ), weight_limit=50, expected_opt_value=220),
            Case(desc='Triple items #2', items=(
                KnapsackItem(weight=30, value=120),
                KnapsackItem(weight=20, value=100),
                KnapsackItem(weight=10, value=60),
            ), weight_limit=50, expected_opt_value=220),
        )

        for case in cases:
            opt_value = do_01_knapsack(case.items, case.weight_limit)
            self.assertEqual(opt_value, case.expected_opt_value,
                             msg='%s, %d != %d' % (case.desc, opt_value, case.expected_opt_value))
