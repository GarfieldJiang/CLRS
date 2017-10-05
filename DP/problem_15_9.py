import unittest
import queue
import logging


logging.basicConfig(level=logging.WARNING)


def calc_string_break_order(n, break_points):
    """
    Calculate the optimal cost and the corresponding breaking order to break the string of length n with break points in
    break_points.
    :param n: Length of the string.
    :param break_points: Each element bp means a break point exists after char at bp.
    :return: The optimal cost and the corresponding breaking order.
    """
    if n <= 0:
        return 0, ()

    break_flags = [False] * (n - 1)
    for bp in break_points:
        break_flags[bp] = True

    c = [[float('inf') for _ in range(0, n)] for _ in range(0, n)]
    for i in range(0, n):
        c[i][i] = 0

    first_break_points = [[-1 for _ in range(0, n)] for _ in range(0, n)]

    for j_i_diff in range(1, n):
        for i in range(0, n - j_i_diff):
            j = i + j_i_diff
            cost = c[i][j]

            has_break_flags = False
            for k in range(i, j):
                if not break_flags[k]:
                    continue
                has_break_flags = True
                new_cost = j_i_diff + 1 + c[i][k] + c[k + 1][j]
                if new_cost < cost:
                    cost = new_cost
                    first_break_points[i][j] = k

            if not has_break_flags:
                cost = 0
            logging.debug('c[%d][%d] = %.2f', i, j, cost)
            c[i][j] = cost

    break_order = []
    q = queue.Queue()
    logging.debug('queue: push (%d, %d)' % (0, n - 1))
    q.put((0, n - 1))
    while not q.empty():
        cur = q.get()
        bp = first_break_points[cur[0]][cur[1]]
        if bp < 0:
            continue
        break_order.append(bp)
        logging.debug('queue: push (%d, %d)' % (cur[0], bp))
        q.put((cur[0], bp))
        q.put((bp + 1, cur[1]))
        logging.debug('queue: push (%d, %d)' % (bp + 1, cur[1]))
    return c[0][n - 1], tuple(break_order)


class TestBreakString(unittest.TestCase):
    def test_break_string(self):
        cases = (
            ("Length 0", 0, (), 0, ()),
            ("Length 1", 1, (), 0, ()),
            ("Length 20, the example in the problem", 20, (1, 7, 9), 38, (9, 1, 7)),
            ("Length 100, one break point", 100, (35,), 100, (35,)),
            ("Length 100, 2 break points", 100, (24, 49), 100 + 50, (49, 24)),
            ("Length 128, 7 even break points", 128, (15, 31, 47, 63, 79, 95, 111), 384, (63, 31, 95, 15, 47, 79, 111)),
        )

        for desc, n, break_flags, expected_cost, expected_break_order in cases:
            cost, break_order = calc_string_break_order(n, break_flags)
            self.assertAlmostEqual(cost, expected_cost, msg='%s, cost %.2f != %.2f' % (desc, cost, expected_cost))
            self.assertEqual(break_order, expected_break_order,
                             msg='%s, break order %s != %s' % (desc, break_order, expected_break_order))
