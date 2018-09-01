from collections import namedtuple
from Common.common import default_key
from random import randint


Case = namedtuple('Case', 'desc array key offset length')


def get_cases():
    return (
        Case(desc='Empty', array=[], offset=0, length=None, key=None),
        Case(desc='Single', array=[1], offset=0, length=None, key=None),
        Case(desc="7 elements reverse key", array=[1, 2, 3, 4, 7, 6, 5], offset=0, length=None, key=lambda x: -x),
        Case(desc='8 elements #0', array=[1, 8, 2, 7, 3, 6, 4, 5], offset=4, length=None, key=None),
        Case(desc='8 elements #1 (sorted)', array=[1, 2, 3, 4, 5, 6, 7, 8], offset=0, length=None, key=None),
        Case(desc='8 elements #2 (reversely sorted)', array=[8, 7, 6, 5, 4, 3, 2, 1], offset=0, length=None, key=None),
        Case(desc='10 elements #0', array=[1, 2, 2, 2, 2, 2, 1, 1, 1, 1], offset=0, length=None, key=None),
        Case(desc='10 elements #0', array=[5, 2, 3, 2, 1, 3, 5, 4, 4, 1], offset=0, length=None, key=None),
        Case(desc='101 elements #0 (sorted)', array=[i + 1 for i in range(0, 101)], offset=0, length=None, key=None),
        Case(desc='101 elements #0 (reversely sorted)', array=[i + 1 for i in range(100, -1, -1)],
             offset=0, length=None, key=None),
        Case(desc='1000 elements #0 (sorted)', array=[i + 1 for i in range(0, 1000)], offset=0, length=None, key=None),
        Case(desc='1000 elements #1 (reversely sorted)', array=[i + 1 for i in range(999, -1, -1)],
             offset=0, length=None, key=None),
        Case(desc='Sort last half', array=[randint(1, 50) for _ in range(0, 200)], offset=100, length=None, key=None),
        Case(desc='Sort middle part', array=[randint(1, 50) for _ in range(0, 200)], offset=50, length=100, key=None),
    )


def check_is_sorted(array, offset=0, length=None, key=None):
    if not array:
        return True
    if length is None:
        length = len(array) - offset
    key = key or default_key
    for i in range(offset, offset + length - 1):
        if key(array[i]) > key(array[i + 1]):
            return False

    return True


def check_sorting_result(before_sorting, after_sorting, offset=0, length=None, key=None):
    assert(len(before_sorting) == len(after_sorting))
    if length is None:
        length = len(before_sorting) - offset
    key = key or default_key

    # Remains unchanged out of the scope of sorting.
    for i in range(0, offset):
        if before_sorting[i] != after_sorting[i]:
            return False

    for i in range(offset + length, len(before_sorting)):
        if before_sorting[i] != after_sorting[i]:
            return False

    # Sorted in the sorting scope.
    if not check_is_sorted(after_sorting, offset, length, key):
        return False

    # after_sorting is a permutation of before_sorting
    dict_before = {}
    dict_after = {}
    for i in range(offset, offset + length):
        if before_sorting[i] in dict_before:
            dict_before[before_sorting[i]] += 1
        else:
            dict_before[before_sorting[i]] = 1

        if after_sorting[i] in dict_after:
            dict_after[after_sorting[i]] += 1
        else:
            dict_after[after_sorting[i]] = 1
    if dict_before != dict_after:
        return False;

    return True
