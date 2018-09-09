from random import randint
from typing import TypeVar, List


T = TypeVar('T')


def default_key(x):
    """
    Default key getter.
    :param x: input.
    :return: the input itself.
    """
    return x


def rand_permutate(array: List[T], offset: int=0, length: int=None):
    if not array:
        return
    n = len(array)
    assert offset >= 0
    length = length or n - offset
    assert length >= 0 and offset + length <= n
    while length > 1:
        r = randint(0, length - 1)
        array[offset + r], array[offset + length - 1] = array[offset + length - 1], array[offset + r]
        length -= 1
