"""
Problem: any non-negative integer n could be decomposed as sums of full square numbers. From all the decomposition
possibilities, we need to find the shortest. For example, 18 = 3^2 + 3^2 only has 2 terms, which is the shortest
decomposition of 18.
"""


import unittest
import math
import time


def get_shortest_full_square_decomp(n):
    assert type(n) is int, "The input number must be an integer."
    assert n >= 0, "The input number must be non-negative."
    if n == 0:
        return 1, {0: 1}

    dp = [-1] * (n + 1)
    satellites = [-1] * (n + 1)

    rounded_root = __get_rounded_sqrt(n)
    if n == rounded_root * rounded_root:
        return 1, {rounded_root: 1}

    for i in xrange(1, n + 1):
        assert dp[i] < 0
        rounded_root_i = __get_rounded_sqrt(i)
        if i == rounded_root_i * rounded_root_i:
            dp[i] = 1
            satellites[i] = 0
            continue

        j = 1
        while j * j < i:
            if dp[i] < 0 or dp[i] > 1 + dp[i - j * j]:
                dp[i] = 1 + dp[i - j * j]
                satellites[i] = j
            j += 1

    decomp = {}
    i = n
    while satellites[i] > 0:
        j = satellites[i]
        decomp[j] = decomp[j] + 1 if j in decomp else 1
        i -= j * j

    rounded_root_i = __get_rounded_sqrt(i)
    decomp[rounded_root_i] = decomp[rounded_root_i] + 1 if rounded_root_i in decomp else 1
    return dp[n], decomp


def __get_rounded_sqrt(n):
    return int(round(math.sqrt(n)))


class TestShortestFullSquareDecomp(unittest.TestCase):
    def testNormal(self):
        self.assertEqual(get_shortest_full_square_decomp(0), (1, {0: 1}))
        self.assertEqual(get_shortest_full_square_decomp(1), (1, {1: 1}))
        self.assertEqual(get_shortest_full_square_decomp(7), (4, {1: 3, 2: 1}))
        self.assertEqual(get_shortest_full_square_decomp(13), (2, {2: 1, 3: 1}))
        self.assertEqual(get_shortest_full_square_decomp(18), (2, {3: 2}))

    def test365(self):
        cnt, decomp = get_shortest_full_square_decomp(365)
        self.assertEqual(cnt, 2)

        possible_res = (
            {13: 1, 14: 1},
            {19: 1, 2: 1},
        )
        self.assertTrue(decomp in possible_res)


def print_decomp(n, decomp):
    decomp_list = []
    for k in decomp:
        decomp_list.append((k, decomp[k]))
    decomp_list.sort(key=lambda i: -i[0])

    text = "%d = " % n
    is_first = True
    for item in decomp_list:
        if is_first:
            is_first = False
        else:
            text += " + "

        if item[1] == 1:
            text += '(%d)^2' % item[0]
        else:
            text += '%d * (%d)^2' % (item[1], item[0])

    print text


def __main():
    for n in xrange(38000, 38031):
        start_time = time.time()
        _, decomp = get_shortest_full_square_decomp(n)
        end_time = time.time()
        print "Decompsing %d takes %.2fs." % (n, end_time - start_time)
        print_decomp(n, decomp)


if __name__ == '__main__':
    __main()
