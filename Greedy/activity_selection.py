import logging
import unittest
from collections import namedtuple


logging.basicConfig(level=logging.WARN)


class Activity(object):
    def __init__(self, start_time, finish_time):
        if start_time >= finish_time:
            raise ValueError('start_time must be less than finish_time')
        self.start_time = start_time
        self.finish_time = finish_time


def _check_input(activities):
    if not activities:
        return

    assert isinstance(activities, tuple)

    n = len(activities)
    assert isinstance(activities[0], Activity)
    assert activities[0].start_time >= 0 and activities[0].finish_time < float('inf')
    for i in xrange(1, n):
        assert isinstance(activities[i], Activity)
        assert activities[i].finish_time >= activities[i].start_time
        assert activities[i].start_time >= 0 and activities[i].finish_time < float('inf')


def select_activity_dp_0(activities):
    """
    A DP approach similar to the O(n^2) time solution to the longest increasing subsequence problem, which is also
    O(n^2) time where n = len(activities)
    :param activities: The activities sorted by their finishing times.
    :return: The optimal subset count and an optimal subset (indices of activities sorted in the original order).
    """
    _check_input(activities)
    if not activities:
        return 0, ()

    n = len(activities)
    opt_counts = [1] * n
    opt_predecessors = [-1] * n

    for i in xrange(1, n):
        for j in xrange(0, i):
            if activities[j].finish_time > activities[i].start_time:
                continue
            if opt_counts[j] + 1 <= opt_counts[i]:
                continue
            opt_counts[i] = opt_counts[j] + 1
            opt_predecessors[i] = j

    opt_index = 0
    opt_count = opt_counts[0]

    for i in xrange(1, n):
        if opt_counts[i] > opt_count:
            opt_count = opt_counts[i]
            opt_index = i

    opt_set = [-1] * opt_count
    i = opt_count - 1
    while opt_index >= 0:
        opt_set[i] = opt_index
        opt_index = opt_predecessors[opt_index]
        i -= 1

    return opt_count, tuple(opt_set)


def _get_result_dp_1(c, first_selected, i, j, result):
    if i + 1 >= j or first_selected[i][j] < 0:
        return

    k = first_selected[i][j]
    _get_result_dp_1(c, first_selected, i, k, result)
    result.append(k - 1)
    _get_result_dp_1(c, first_selected, k, j, result)


def select_activity_dp_1(activities):
    """
    The DP approach in the text. Let n = len(activities) and this algorithm runs in O(n^3) time. The advantage of this
    algorithm is that it could help demonstrate the correctness of the greedy algorithm.
    :param activities: The activities sorted by their finishing times.
    :return: The optimal subset count and an optimal subset (indices of activities sorted in the original order).
    """
    _check_input(activities)
    if not activities:
        return 0, ()

    n = len(activities)

    # Add 2 dummy activities at the beginning and the end to facilitate subsequent calculation.
    activities = (Activity(-1, 0),) + activities + (Activity(activities[n - 1].finish_time, float('inf')),)

    c = [[0 for _ in xrange(0, n + 2)] for _ in xrange(0, n + 2)]
    first_selected = [[-1 for _ in xrange(n + 2)] for _ in xrange(0, n + 2)]

    for j_i_diff in xrange(2, n + 2):
        for i in xrange(0, n + 2 - j_i_diff):
            j = i + j_i_diff

            for k in xrange(i + 1, j):
                if activities[k].start_time < activities[i].finish_time\
                        or activities[k].finish_time > activities[j].start_time:
                    continue

                new_count = c[i][k] + c[k][j] + 1
                if new_count > c[i][j]:
                    c[i][j] = new_count
                    first_selected[i][j] = k

            logging.debug('i=%d, j=%d, c[i][j]=%d, first_selected[i][j]=%d', i, j, c[i][j], first_selected[i][j])

    logging.debug('count matrix: %s' % c)
    logging.debug('first selected: %s' % first_selected)

    opt_subset = []
    _get_result_dp_1(c, first_selected, 0, n + 1, opt_subset)

    logging.debug('result: %s' % opt_subset)
    return c[0][n + 1], tuple(opt_subset)


def select_activity_greedy(activities):
    """
    Greedy algorithm with O(n) time, by always choosing the compatible activity with the smallest finishing time.
    :param activities: The activities sorted by their finishing times.
    :return: The optimal subset count and an optimal subset (indices of activities sorted in the original order).
    """
    _check_input(activities)
    if not activities:
        return 0, ()

    n = len(activities)
    res = [0]
    for i in xrange(1, n):
        if activities[i].start_time >= activities[res[len(res) - 1]].finish_time:
            res.append(i)
    return len(res), tuple(res)


Case = namedtuple('Case', 'desc activities expected_optimal_count expected_optimal_subsets')


class TestActivitySelection(unittest.TestCase):
    def test_activity_selection(self):
        cases = (
            Case(desc='Empty', activities=(), expected_optimal_count=0, expected_optimal_subsets=((),)),
            Case(desc='Single', activities=(Activity(0, 1),), expected_optimal_count=1,
                 expected_optimal_subsets=((0,),)),
            Case(desc='Example in the book', activities=(
                Activity(1, 4),
                Activity(3, 5),
                Activity(0, 6),
                Activity(5, 7),
                Activity(3, 9),
                Activity(5, 9),
                Activity(6, 10),
                Activity(8, 11),
                Activity(8, 12),
                Activity(2, 14),
                Activity(12, 16),
            ), expected_optimal_count=4, expected_optimal_subsets=((0, 3, 7, 10), (1, 3, 8, 10))),
        )

        for case in cases:
            for method in (select_activity_dp_0, select_activity_dp_1, select_activity_greedy):
                optimal_count, optimal_subset = method(case.activities)
                self.assertEqual(
                    optimal_count, case.expected_optimal_count,
                    msg='%s, optimal count: %d != %d' % (case.desc, optimal_count, case.expected_optimal_count)
                )
                self.assertTrue(
                    optimal_subset in case.expected_optimal_subsets,
                    msg='%s, optimal subset: %s not in %s' % (case.desc, optimal_subset, case.expected_optimal_subsets)
                )
