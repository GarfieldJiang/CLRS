import unittest


def default_key(x):
    """
    Default key getter.
    :param x: input.
    :return: the input itself.
    """
    return x


def binary_search_eq(x, beg, end, val):
    """
    Returns the index of the input sequence where the value is equal to the given value.
    :param x: the input sequence.
    :param beg: the first index (inclusive).
    :param end: the last index (exclusive).
    :param val: the given value.
    :return: the index of 'x' where the value is equal to 'val'.
    """

    if beg >= end:
        return -1

    while end - beg > 1:
        mid = beg + (end - beg) // 2
        if x[mid] == val:
            return mid

        if x[mid] > val:
            end = mid
        else:
            beg = mid

    return beg if x[beg] == val else -1


def binary_search_ge(x, beg, end, val):
    """
    Returns the index of the input sequence where the value is equal to or the first one to be greater than the given
    value.
    :param x: the input sequence.
    :param beg: the first index (inclusive).
    :param end: the last index (exclusive).
    :param val: the given value.
    :return: the index of 'x' where the value is equal to or the first one to be greater than 'val'.
    """

    if beg >= end:
        return -1

    original_end = end
    while end - beg > 1:
        mid = beg + (end - beg) // 2
        if x[mid] == val:
            return mid

        if x[mid] > val:
            end = mid
        else:
            beg = mid

    return beg if x[beg] >= val else beg + 1 if beg + 1 < original_end else -1


class TestCommon(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCommon, self).__init__(*args, **kwargs)

    def test_binary_search_eq(self):
        cases = (
            ([], 666, -1),
            ([3], 3, 0),
            ([3], 2, -1),
            ([3], 4, -1),
            ([1, 3, 5, 7, 8, 10, 12], 1, 0),
            ([1, 3, 5, 7, 8, 10, 12], 3, 1),
            ([1, 3, 5, 7, 8, 10, 12], 5, 2),
            ([1, 3, 5, 7, 8, 10, 12], 7, 3),
            ([1, 3, 5, 7, 8, 10, 12], 8, 4),
            ([1, 3, 5, 7, 8, 10, 12], 10, 5),
            ([1, 3, 5, 7, 8, 10, 12], 12, 6),
            ([1, 3, 5, 7, 8, 10, 12], 13, -1),
            ([1, 3, 5, 7, 8, 10, 12], 4, -1),
            (['1', '6', '7'], '2', -1),
            (['1', '6', '7'], '0', -1),
            (['1', '6', '7'], '7', 2),
            (['1', '6', '7'], '8', -1),
            ([1, 3], 0, -1),
            ([1, 3], 1, 0),
            ([1, 3], 2, -1),
            ([1, 3], 3, 1),
            ([1, 3], 4, -1),
        )
        for case in cases:
            self.assertEqual(len(case), 3)
            self.assertEqual(binary_search_eq(case[0], 0, len(case[0]), case[1]), case[2])

    def test_binary_search_ge(self):
        cases = (
            ([], 666, -1),
            ([3], 3, 0),
            ([3], 2, 0),
            ([3], 4, -1),
            ([1, 3, 5, 7, 8, 10, 12], 1, 0),
            ([1, 3, 5, 7, 8, 10, 12], 3, 1),
            ([1, 3, 5, 7, 8, 10, 12], 5, 2),
            ([1, 3, 5, 7, 8, 10, 12], 7, 3),
            ([1, 3, 5, 7, 8, 10, 12], 8, 4),
            ([1, 3, 5, 7, 8, 10, 12], 10, 5),
            ([1, 3, 5, 7, 8, 10, 12], 12, 6),
            ([1, 3, 5, 7, 8, 10, 12], 13, -1),
            ([1, 3, 5, 7, 8, 10, 12], 4, 2),
            (['1', '6', '7'], '2', 1),
            (['1', '6', '7'], '0', 0),
            (['1', '6', '7'], '7', 2),
            (['1', '6', '7'], '8', -1),
            ([1, 3], 0, 0),
            ([1, 3], 1, 0),
            ([1, 3], 2, 1),
            ([1, 3], 3, 1),
            ([1, 3], 4, -1),
        )
        for case in cases:
            self.assertEqual(len(case), 3)
            self.assertEqual(binary_search_ge(case[0], 0, len(case[0]), case[1]), case[2])
