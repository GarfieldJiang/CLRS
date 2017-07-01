import unittest
from collections import namedtuple


def plan_inventory(demands, fixed_productivity, extra_cost_per_machine, holding_cost_func):
    if not demands:
        return 0, ()

    n = len(demands)
    cumulative_demands = [demands[i] for i in xrange(0, n)]
    for i in xrange(1, n):
        cumulative_demands[i] += cumulative_demands[i - 1]
    sum_d = cumulative_demands[n - 1]

    dp = [[-1 for _ in xrange(0, sum_d + 1)] for _ in xrange(0, n)]
    last_month_plan = [[-1 for _ in xrange(0, sum_d + 1)] for _ in xrange(0, n)]
    for j in xrange(cumulative_demands[0], sum_d + 1):
        dp[0][j] = max(0, extra_cost_per_machine * (j - fixed_productivity))\
                   + holding_cost_func(j - cumulative_demands[0])
        last_month_plan[0][j] = 0

    for i in xrange(1, n):
        for j in xrange(cumulative_demands[i], sum_d + 1):
            for k in xrange(cumulative_demands[i - 1], j + 1):
                if dp[i - 1][k] < 0:
                    continue

                new_cost = (
                    dp[i - 1][k] + max(0, extra_cost_per_machine * (j - k - fixed_productivity))
                    + holding_cost_func(j - cumulative_demands[i])
                )

                if dp[i][j] < 0 or dp[i][j] > new_cost:
                    dp[i][j] = new_cost
                    last_month_plan[i][j] = k

    plan = [0 for _ in xrange(0, n)]
    k = sum_d
    for i in xrange(n - 1, -1, -1):
        plan[i] = k - last_month_plan[i][k]
        k = last_month_plan[i][k]

    return dp[n - 1][sum_d], tuple(plan)


Case = namedtuple('Case', 'desc demands fixed_productivity extra_cost_per_machine holding_cost_func ' +
                          'expected_cost expected_plan')


class TestInventoryPlanning(unittest.TestCase):
    def test_inventory_planning(self):
        cases = (
            Case(desc='Empty', demands=(), fixed_productivity=0, extra_cost_per_machine=0,
                 holding_cost_func=None, expected_cost=0, expected_plan=()),
            Case(desc='Only one month', demands=(100,), fixed_productivity=90, extra_cost_per_machine=10,
                 holding_cost_func=lambda i: i * 1000, expected_cost=100, expected_plan=(100,)),
            Case(desc='3 in 3 months, 1 each, expensive holding', demands=(1, 1, 1),
                 fixed_productivity=2, extra_cost_per_machine=0,
                 holding_cost_func=lambda i: i * 1000, expected_cost=0, expected_plan=(1, 1, 1)),
            Case(desc='3 months, increasing demands, cheap holding, #0', demands=(1, 3, 5),
                 fixed_productivity=4, extra_cost_per_machine=1000,
                 holding_cost_func=lambda i: i, expected_cost=1, expected_plan=(1, 4, 4)),
            Case(desc='3 months, increasing demands, cheap holding, #1', demands=(1, 3, 5),
                 fixed_productivity=3, extra_cost_per_machine=1000,
                 holding_cost_func=lambda i: i, expected_cost=4, expected_plan=(3, 3, 3)),
            Case(desc='3 months, increasing demands, expensive holding', demands=(1, 3, 5),
                 fixed_productivity=3, extra_cost_per_machine=1,
                 holding_cost_func=lambda i: i * 1000, expected_cost=2, expected_plan=(1, 3, 5)),
        )

        for case in cases:
            cost, plan = plan_inventory(case.demands, case.fixed_productivity, case.extra_cost_per_machine,
                                        case.holding_cost_func)
            self.assertEqual(cost, case.expected_cost,
                             '%s, cost: %d != %d' % (case.desc, cost, case.expected_cost))
            self.assertEqual(plan, case.expected_plan,
                             '%s, plan: %s != %s' % (case.desc, plan, case.expected_plan))
