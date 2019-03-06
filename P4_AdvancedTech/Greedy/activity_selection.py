import logging
import unittest
from collections import namedtuple
from P2_Sorting.HeapSort.heap_sort import heap_sort as sort


logging.basicConfig(level=logging.WARNING)


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
    for i in range(1, n):
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

    for i in range(1, n):
        for j in range(0, i):
            if activities[j].finish_time > activities[i].start_time:
                continue
            if opt_counts[j] + 1 <= opt_counts[i]:
                continue
            opt_counts[i] = opt_counts[j] + 1
            opt_predecessors[i] = j

    opt_index = 0
    opt_count = opt_counts[0]

    for i in range(1, n):
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

    c = [[0 for _ in range(0, n + 2)] for _ in range(0, n + 2)]
    first_selected = [[-1 for _ in range(n + 2)] for _ in range(0, n + 2)]

    for j_i_diff in range(2, n + 2):
        for i in range(0, n + 2 - j_i_diff):
            j = i + j_i_diff

            for k in range(i + 1, j):
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
    for i in range(1, n):
        if activities[i].start_time >= activities[res[len(res) - 1]].finish_time:
            res.append(i)
    return len(res), tuple(res)


class _HallUseTimeItem(object):
    def __init__(self, value, start_or_finish, index):
        self.value = value
        self.start_or_finish = start_or_finish
        self.index = index

    def __eq__(self, other):
        if not isinstance(other, _HallUseTimeItem):
            raise ValueError('Wrong type')

        return self.value == other.value and self.start_or_finish == other.start_or_finish

    def __lt__(self, other):
        if not isinstance(other, _HallUseTimeItem):
            raise ValueError('Wrong type')

        return self.value < other.value or (self.value == other.value and not self.start_or_finish and
                                            other.start_or_finish)

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __cmp__(self, other):
        if self == other:
            return 0
        elif self < other:
            return -1
        else:
            return 1

    def __str__(self):
        return 'value=%s, %s, index=%d' % (self.value, 'START' if self.start_or_finish else 'FINISH', self.index)


def use_least_halls(activities):
    """
    Ex 16.1-4. Found the solution from the internet. Basic idea is to sort the start and finish times of all activities,
    and really simulate the process of selecting halls to use.
    :param activities: Activities to schedule.
    :return: Hall usage as a set of each hall's occupation sequence.
    """
    _check_input(activities)
    n = len(activities)
    hall_use_time_items = [None] * n * 2
    index = 0
    for activity in activities:
        hall_use_time_items[index] = _HallUseTimeItem(value=activity.start_time,
                                                      start_or_finish=True, index=index // 2)
        index += 1
        hall_use_time_items[index] = _HallUseTimeItem(value=activity.finish_time,
                                                      start_or_finish=False, index=index // 2)
        index += 1

    sort(hall_use_time_items)

    halls_per_activity = [-1] * n
    hall_count = 0
    available_halls = []
    for hall_use_time_item in hall_use_time_items:
        if not hall_use_time_item.start_or_finish:
            assert halls_per_activity[hall_use_time_item.index] >= 0
            available_halls.append(halls_per_activity[hall_use_time_item.index])
        elif not available_halls:
            halls_per_activity[hall_use_time_item.index] = hall_count
            hall_count += 1
        else:
            halls_per_activity[hall_use_time_item.index] = available_halls.pop()

    hall_usage = [[] for _ in range(0, hall_count)]
    for i in range(0, len(halls_per_activity)):
        hall_usage[halls_per_activity[i]].append(i)

    for i in range(0, hall_count):
        hall_usage[i] = tuple(hall_usage[i])
    return set(hall_usage)


class TestActivitySelection(unittest.TestCase):
    def test_activity_selection(self):
        case_class = namedtuple('Case', 'desc activities expected_optimal_count expected_optimal_subsets')
        cases = (
            case_class(desc='Empty', activities=(), expected_optimal_count=0, expected_optimal_subsets=((),)),
            case_class(desc='Single', activities=(Activity(0, 1),), expected_optimal_count=1,
                       expected_optimal_subsets=((0,),)),
            case_class(desc='Example in the book', activities=(
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

    def test_using_least_halls(self):
        case_class = namedtuple('Case', 'desc activities hall_usage')
        cases = (
            case_class(desc='Empty', activities=(), hall_usage=set()),
            case_class(desc='Single', activities=(Activity(0, 1),), hall_usage={(0,)}),
            case_class(desc='Triple #0', activities=(
                Activity(1, 2),
                Activity(2, 4),
                Activity(4, 5),
            ), hall_usage={(0, 1, 2)}),
            case_class(desc='Triple #1', activities=(
                Activity(1, 3),
                Activity(2, 4),
                Activity(3, 5),
            ), hall_usage={(0, 2), (1,)}),
            case_class(desc='Triple #2', activities=(
                Activity(1, 4),
                Activity(2, 5),
                Activity(3, 6),
            ), hall_usage={(0,), (1,), (2,)}),
            case_class(desc='Example in the book for activity selection', activities=(
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
            ), hall_usage={(2, 6), (0, 5), (9,), (1, 7), (4,), (8, 10)}),
        )

        for case in cases:
            hall_usage = use_least_halls(case.activities)
            self.assertEqual(len(hall_usage), len(case.hall_usage),
                             msg='%s, Hall count %s != %s' % (case.desc, len(hall_usage), len(case.hall_usage)))
            activity_indices = set(range(0, len(case.activities)))
            for hall_usage_item in hall_usage:
                for i in range(0, len(hall_usage_item)):
                    if i > 0:
                        self.assertTrue(case.activities[hall_usage_item[i - 1]].finish_time <=
                                        case.activities[hall_usage_item[i]].start_time,
                                        msg="%s, Wrong hall usage: %s" % (case.desc, hall_usage_item[i - 1]))
                    self.assertTrue(hall_usage_item[i] in activity_indices,
                                    msg='%s, activity %d has been visited or does not exist.'
                                        % (case.desc, hall_usage_item[i]))
                    activity_indices.remove(hall_usage_item[i])
            self.assertTrue(len(activity_indices) == 0,
                            "%s, activity indices unempty at the end: %s" % (case.desc, activity_indices))

