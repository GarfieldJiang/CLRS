import unittest


def get_longest_palindrome_subsequence(s):
    """
    Problem 15-2. __calc_lps_length runs in \Theta(n^2) time. __build_lps runs in \Theta(n) time.
    :param s: input string.
    :return: a longest palindrome subsequence (LPS) of s.
    """

    if not s:
        return ()

    n = len(s)
    lengths = __calc_lps_length(s, n)

    max_len = lengths[0][n]
    p = [None for _ in xrange(0, max_len)]
    __build_lps(s, lengths, 0, n, p, 0, len(p))

    return tuple(p)


def __calc_lps_length(s, n):
    lengths = [[-1 for _ in xrange(0, n + 1)] for _ in xrange(0, n + 1)]

    for beg in xrange(0, n + 1):
        lengths[beg][beg] = 0
        if beg != n:
            lengths[beg][beg + 1] = 1

    for end_beg in xrange(2, n + 1):
        for beg in xrange(n - end_beg, -1, -1):
            end = beg + end_beg
            assert lengths[beg + 1][end - 1] >= 0
            assert lengths[beg + 1][end] >= 0
            assert lengths[beg][end - 1] >= 0
            if s[beg] == s[end - 1]:
                lengths[beg][end] = 2 + lengths[beg + 1][end - 1]
            else:
                lengths[beg][end] = max(lengths[beg + 1][end], lengths[beg][end - 1])

    # print lengths
    return lengths


def __build_lps(s, lengths, beg, end, p, sub_beg, sub_end):
    assert beg <= end
    assert sub_beg <= sub_end

    if beg == end:
        return

    if beg + 1 == end:
        assert sub_beg + 1 == sub_end
        p[sub_beg] = s[beg]
        return

    if s[beg] == s[end - 1]:
        p[sub_beg] = p[sub_end - 1] = s[beg]
        __build_lps(s, lengths, beg + 1, end - 1, p, sub_beg + 1, sub_end - 1)
        return

    if lengths[beg + 1][end] > lengths[beg][end - 1]:
        __build_lps(s, lengths, beg + 1, end, p, sub_beg, sub_end)
    else:
        __build_lps(s, lengths, beg, end - 1, p, sub_beg, sub_end)


class TestLongestPalindromeSubsequence(unittest.TestCase):
    def test_get_longest_palindrome_subsequence(self):
        self.assertEqual(get_longest_palindrome_subsequence(''), ())
        self.assertEqual(''.join(get_longest_palindrome_subsequence('x')), 'x')
        self.assertEqual(''.join(get_longest_palindrome_subsequence('xyxw')), 'xyx')
        self.assertEqual(''.join(get_longest_palindrome_subsequence('aAbBcCDbEFaGHdUeVfWggYfZed')), 'defggfed')
        self.assertEqual(''.join(get_longest_palindrome_subsequence('aAbBcCDbEFaGHdUeVfWgKgYfZed')), 'defgKgfed')
        self.assertEqual(''.join(get_longest_palindrome_subsequence('dUeVfWggYfZedaAbBcCDbEFaGH')), 'defggfed')
        self.assertEqual(''.join(get_longest_palindrome_subsequence('dUeVfWgKgYfZedaAbBcCDbEFaGH')), 'defgKgfed')
        self.assertEqual(''.join(get_longest_palindrome_subsequence('character')), 'carac')
