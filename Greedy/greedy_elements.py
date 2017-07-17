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


def plan_water_stops(positions, duration):
    """
    Ex 16.2-4. Greedy algorithm with O(n) run time, where n is len(positions)
    :param positions: positions of the water stops plus the beginning and ending points of the trip.
    :param duration: how much distance the professor can cover without refilling his water supply.
    :return: The optimal choice of water stop indices, including the beginning point.
    """

    if not positions:
        return 0, ()

    n = len(positions)
    for i in xrange(1, n):
        assert positions[i - 1] < positions[i]
    assert duration > 0

    stops = [0]
    for i in xrange(1, n):
        last_stop_pos = positions[stops[-1]]
        if positions[i] - last_stop_pos > duration:  # No way to finish the trip.
            return -1, ()

        if i == n - 1:
            break

        if positions[i + 1] - last_stop_pos > duration:
            stops.append(i)

    return len(stops), tuple(stops)


class TestGreedyElements(unittest.TestCase):
    def test_01_knapsack(self):
        case_class = namedtuple('Case', 'desc items weight_limit expected_opt_value')
        cases = (
            case_class(desc='Empty', items=(), weight_limit=100, expected_opt_value=0),
            case_class(desc='Single item within limit', items=(KnapsackItem(weight=10, value=5),), weight_limit=10,
                       expected_opt_value=5),
            case_class(desc='Single item beyond limit', items=(KnapsackItem(weight=10, value=5),), weight_limit=9,
                       expected_opt_value=0),
            case_class(desc='Triple items #0', items=(
                KnapsackItem(weight=10, value=60),
                KnapsackItem(weight=20, value=100),
                KnapsackItem(weight=30, value=120),
            ), weight_limit=50, expected_opt_value=220),
            case_class(desc='Triple items #1', items=(
                KnapsackItem(weight=20, value=100),
                KnapsackItem(weight=10, value=60),
                KnapsackItem(weight=30, value=120),
            ), weight_limit=50, expected_opt_value=220),
            case_class(desc='Triple items #2', items=(
                KnapsackItem(weight=30, value=120),
                KnapsackItem(weight=20, value=100),
                KnapsackItem(weight=10, value=60),
            ), weight_limit=50, expected_opt_value=220),
        )

        for case in cases:
            opt_value = do_01_knapsack(case.items, case.weight_limit)
            self.assertEqual(opt_value, case.expected_opt_value,
                             msg='%s, %d != %d' % (case.desc, opt_value, case.expected_opt_value))

    def test_plan_water_stops(self):
        case_class = namedtuple('Case', 'desc positions duration expected_stop_count expected_stops')
        cases = (
            case_class(desc="Empty", positions=(), duration=2000, expected_stop_count=0, expected_stops=()),
            case_class(desc="One point", positions=(0,), duration=2000, expected_stop_count=1, expected_stops=(0,)),
            case_class(desc="Two points reachable", positions=(0, 1500),
                       duration=2000, expected_stop_count=1, expected_stops=(0,)),
            case_class(desc="Two points unreachable", positions=(0, 2500),
                       duration=2000, expected_stop_count=-1, expected_stops=()),
            case_class(desc="10 points reachable", positions=(0, 1000, 1500, 2500, 2800, 3200, 3600, 4000, 5000, 6000),
                       duration=2000, expected_stop_count=4, expected_stops=(0, 2, 5, 8)),
            case_class(desc="10 points unreachable",
                       positions=(0, 1000, 1500, 2500, 2800, 4810, 5600, 6500, 7000, 9000),
                       duration=2000, expected_stop_count=-1, expected_stops=()),
        )

        for case in cases:
            stop_count, stops = plan_water_stops(case.positions, case.duration)
            res = (stop_count, stops)
            expected = (case.expected_stop_count, case.expected_stops)
            self.assertEqual(res, expected, msg='%s, %s != %s' % (case.desc, res, expected))
