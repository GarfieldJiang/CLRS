from .selection_in_linear_time import select, select_internal
from typing import TypeVar, List, Callable
from collections import namedtuple
from Common.common import default_key


T = TypeVar('T')
K = TypeVar('K')


_Pair = namedtuple('_Pair', 'min max')


def select_variant(array: List[T], rank: int, key: Callable[[T], K]=None) -> T:
    """
    Problem 9-3(a).
    :param array:
    :param rank:
    :param key:
    :return:
    """
    assert array
    n = len(array)
    assert 0 <= rank < n
    key = key or default_key
    if rank + 1 >= (n - 1) // 2:
        return select(array, rank, key)

    pairs_count = n // 2 if n % 2 == 0 else (n + 1) // 2
    pairs: List[_Pair] = [None] * pairs_count
    i = 0
    if n % 2 == 1:
        pairs[0] = _Pair(min=array[0], max=None)
        i = 1

    while i < n:
        _min = array[i]
        _max = array[i + 1]
        if _min > _max:
            _min, _max = _max, _min
        pairs[(i + 1) // 2] = _Pair(min=_min, max=_max)
        i += 2

    select_variant(pairs, rank, key=lambda x: key(x.min))

    i = 0
    hi = None
    for j in range(0, pairs_count):
        array[i] = pairs[j].min
        i += 1
        if pairs[j].max is not None:
            array[i] = pairs[j].max
            i += 1
        if j == rank:
            hi = i - 1

    return select_internal(array, 0, hi, rank, key)
