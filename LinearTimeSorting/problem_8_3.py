from unittest import TestCase
from typing import List, Callable
from Common.sort_utilities import check_sorting_result
from LinearTimeSorting.couting_sort import counting_sort


def sort_strings(strs: List[str]):
    """
    Problem 8-3(b). Sorts strings that have totally n characters in O(n) time, assuming that the character set have a
    const size.
    :param strs: List of strings
    :return:
    """
    if not strs:
        return
    m = len(strs)

    max_len = 0
    for i in range(m):
        assert strs[i] is not None
        if len(strs[i]) > max_len:
            max_len = len(strs[i])

    len_counts = [0] * (max_len + 1)
    for s in strs:
        len_counts[len(s)] += 1

    get_len_as_key: Callable[[str], int] = lambda _s: len(_s)
    sorted_strs = counting_sort(array=strs, key=get_len_as_key)

    str_count = 0
    for l in range(max_len, 0, -1):
        str_count += len_counts[l]
        sub_array = sorted_strs[m - str_count:m]
        sub_array = counting_sort(array=sub_array,  key=lambda _s: ord(_s[l - 1]))
        for i in range(0, str_count):
            sorted_strs[i + m - str_count] = sub_array[i]

    for i in range(m):
        strs[i] = sorted_strs[i]


class TestSortStrings(TestCase):
    def test_sort_strings(self):
        cases = (
            [],
            [''],
            ['a'],
            ['', 'ab', 'bz', '', 'abc', 'axc', 'az', 'a', 'b'],
            ['', 'ab', 'bz', 'bcdfec', 'bcdef', 'az', '', 'abc', 'axc', 'az', 'a', 'bcdefg'],
        )
        for case in cases:
            before_sorting = list(case)
            # print('Before sorting: %r' % case)
            sort_strings(case)
            # print('After sorting: %r' % case)
            self.assertTrue(check_sorting_result(before_sorting, case))