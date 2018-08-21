from Common import common
import unittest

'''
LCS = Longest Common Subsequence
LMIS = Longest Monotonically Increasing Subsequence
'''


# ex 15.4-2
def get_lcs_len_bottomup(x, y):
    assert x is not None
    assert y is not None

    m = len(x)
    n = len(y)
    c = [[-1 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(m + 1):
        c[i][0] = 0

    for j in range(1, n + 1):
        c[0][j] = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])

    return c


# ex 15.4-3
def get_lcs_len_memoized(x, y):
    assert x is not None
    assert y is not None

    m = len(x)
    n = len(y)
    c = [[-1 for _ in range(n + 1)] for _ in range(m + 1)]

    __get_lcs_len_memoized_internal(x, y, c, m, n)

    return c


def __get_lcs_len_memoized_internal(x, y, c, m, n):
    if c[m][n] >= 0:
        return c[m][n]

    if m == 0 or n == 0:
        c[m][n] = 0
        return 0

    elif x[m - 1] == y[n - 1]:
        c[m][n] = __get_lcs_len_memoized_internal(x, y, c, m - 1, n - 1) + 1
    else:
        c[m][n] = max(__get_lcs_len_memoized_internal(x, y, c, m - 1, n),
                      __get_lcs_len_memoized_internal(x, y, c, m, n - 1))

    return c[m][n]


# ex 15.4-5 method 1
def get_lmis_uselcs(x):
    # Gives the non-strict and strict version of the longest monotically increasing subsequences, noting that the LMIS
    # is the LCS of the original string and its sorted version. Time complexity: O(n^2).

    assert x is not None
    n = len(x)

    y = sorted(x)  # O(n * log(n))
    z = []

    for i in range(0, n):
        if i == 0 or y[i - 1] != y[i]:
            z.append(y[i])

    c = get_lcs_len_bottomup(x, y)
    non_strict_lmis = get_lcs_iter(x, y, c)
    c1 = get_lcs_len_bottomup(x, z)
    strict_lmis = get_lcs_iter(x, z, c1)
    return non_strict_lmis, strict_lmis


# ex 15.4-5 method 2
def get_lmis_direct(x):
    # Directly use dynamic programming. Only returns the strict LMIS. Time complexity: O(n^2).

    assert x is not None
    n = len(x)

    if n == 0:
        return ''

    last_indices = [-1] * n
    lmis_lengths = [1] * n

    for i in range(1, n):
        last_index = -1
        lmis_len = 1
        for j in range(0, i):
            if x[j] < x[i] and lmis_len < lmis_lengths[j] + 1:
                last_index = j
                lmis_len = lmis_lengths[j] + 1

        last_indices[i] = last_index
        lmis_lengths[i] = lmis_len

    last_index = 0
    lmis_len = 1
    for i in range(1, n):
        if lmis_lengths[i] > lmis_len:
            last_index = i
            lmis_len = lmis_lengths[i]

    return ''.join(__build_lmis(x, last_indices, last_index))


def __build_lmis(x, last_indices, last_index):
    if last_index < 0:
        return []

    return __build_lmis(x, last_indices, last_indices[last_index]) + [x[last_index]]


def __custom_binary_search(indices, x, beg, end, val):
    if beg >= end:
        return -1

    original_end = end
    while end - beg > 1:
        mid = beg + (end - beg) // 2
        if x[indices[mid]] == val:
            return mid

        if x[indices[mid]] > val:
            end = mid
        else:
            beg = mid

    return beg if x[indices[beg]] >= val else beg + 1 if beg + 1 < original_end else -1


def get_lmis_quick(x):
    """
    ex 15.4-6. https://en.wikipedia.org/wiki/Longest_increasing_subsequence. Time complexity: O(n * \log n).
    :param x:
    :return:
    """

    assert x is not None
    n = len(x)

    if n == 0:
        return ''

    # min_last_elem_indices[i] denotes the minimum last element index of the MISes of length i + 1.
    # It's obvious that min_last_elem_indices is increasing,
    # but it's not necessarily the final result.
    min_last_elem_indices = [-1] * n
    min_last_elem_indices[0] = 0

    # last_indices[i] is the predecessor index of the LMIS ending at x[i].
    last_indices = [-1] * n

    lmis_len = 1

    for i in range(1, n):
        if x[i] > x[min_last_elem_indices[lmis_len - 1]]:
            # x[i] is greater than the minimum last element of the LMISes of length lmis_len.

            min_last_elem_indices[lmis_len] = i
            last_indices[i] = min_last_elem_indices[lmis_len - 1]
            lmis_len += 1
        else:  # x[i] <= min_last_elem_indices[lmis_len - 1]
            j = __custom_binary_search(min_last_elem_indices, x, 0, lmis_len, x[i])
            min_last_elem_indices[j] = i
            last_indices[i] = min_last_elem_indices[j - 1]

    ret = [None] * lmis_len
    index = min_last_elem_indices[lmis_len - 1]
    ret[lmis_len - 1] = x[index]
    for i in range(lmis_len - 2, -1, -1):
        index = last_indices[index]
        ret[i] = x[index]

    return ''.join(ret)


def get_lcs_iter(x, y, c):
    assert x is not None
    assert y is not None

    m = len(x)
    n = len(y)
    k = c[m][n]
    seq = ['' for _ in range(k)]

    i = m
    j = n
    l = k
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            seq[l - 1] = x[i - 1]
            i -= 1
            j -= 1
            l -= 1
        elif c[i - 1][j] >= c[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(seq)


def get_lcs_recur(x, y, c):
    assert x is not None
    assert y is not None

    m = len(x)
    n = len(y)
    seq = []
    __calc_lcs_recur_internal(x, y, c, m, n, seq)
    return ''.join(seq)


def __calc_lcs_recur_internal(x, y, c, m, n, seq):
    if m == 0 or n == 0:
        return

    if x[m - 1] == y[n - 1]:
        __calc_lcs_recur_internal(x, y, c, m - 1, n - 1, seq)
        seq.append(x[m - 1])
        return

    if c[m - 1][n] >= c[m][n - 1]:
        __calc_lcs_recur_internal(x, y, c, m - 1, n, seq)
    else:
        __calc_lcs_recur_internal(x, y, c, m, n - 1, seq)


class TestLCS(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLCS, self).__init__(*args, **kwargs)

    def test_get_lcs(self):
        get_lcs_len_methods = (get_lcs_len_bottomup, get_lcs_len_memoized)
        get_lcs_methods = (get_lcs_iter, get_lcs_recur)

        for get_lcs_len_method in get_lcs_len_methods:
            for get_lcs_method in get_lcs_methods:
                for case in TestLCS.__get_lcs_cases():
                    self.assertEqual(len(case), 3)
                    x = case[0]
                    y = case[1]
                    z = case[2]

                    m = len(x)
                    n = len(y)
                    k = len(z)
                    c = get_lcs_len_method(x, y)
                    self.assertEqual(len(c), m + 1)
                    for i in range(m + 1):
                        self.assertEqual(len(c[i]), n + 1)
                    self.assertEqual(c[m][n], k)  # Length of LCS
                    self.assertEqual(get_lcs_method(x, y, c), z)  # LCS

    def test_get_lmis_uselcs(self):
        for case in TestLCS.__get_lmis_cases():
            self.assertEqual(len(case), 3)
            original = case[0]
            non_strict_lmises = case[1]
            strict_lmises = case[2]
            res_non_strict, res_strict = get_lmis_uselcs(original)
            self.assertTrue(res_non_strict in non_strict_lmises,
                            'Wrong result \'%s\' for input \'%s\'. Expecting one of %s'
                            % (res_non_strict, original, non_strict_lmises))
            self.assertTrue(res_strict in strict_lmises,
                            'Wrong result \'%s\' for input \'%s\'. Expecting one of %s'
                            % (res_strict, original, strict_lmises))

    def test_get_lmis_direct(self):
        for case in TestLCS.__get_lmis_cases():
            self.assertEqual(len(case), 3)
            original = case[0]
            lmises = case[2]
            res = get_lmis_direct(original)
            self.assertTrue(res in lmises,
                            'Wrong result \'%s\' for input \'%s\'. Expecting one of %s'
                            % (res, original, lmises))

    def test_get_lmis_quick(self):
        for case in TestLCS.__get_lmis_cases():
            self.assertEqual(len(case), 3)
            original = case[0]
            lmises = case[2]
            res = get_lmis_quick(original)
            self.assertTrue(res in lmises,
                            'Wrong result \'%s\' for input \'%s\'. Expecting one of %s'
                            % (res, original, lmises))

    @classmethod
    def __get_lcs_cases(cls):
        # Order: two strings followed by their LCS.
        return (
            ('', '', ''),
            ('1234567', 'ABCDEFGHIJKLMN', ''),
            ('ABCBDAB', 'BDCABA', 'BCBA'),
            ('ACCGGTCGAGTGCGCGGAAGCCGGCCGAA', 'GTCGTTCGGAATGCCGTTGCTCTGTAAA', 'GTCGTCGGAAGCCGGCCGAA'),
        )

    @classmethod
    def __get_lmis_cases(cls):
        # Order: a string followed by its non-strict and strict LMIS.
        return (
            ('', ('',), ('',)),
            ('123', ('123',), ('123',)),
            ('1223', ('1223',), ('123',)),
            ('9784560123', ('0123',), ('0123',)),
            ('0918373225246', ('0122246',), ('01246', '01256', '01346', '01356')),
            ('013425', ('01345',), ('01345',)),
            ('01982376', ('01236', '01237'), ('01236', '01237')),
            ('0011998822337766', ('0011223366', '0011223377'), ('01236', '01237')),
        )
