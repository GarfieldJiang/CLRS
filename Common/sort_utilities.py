from collections import namedtuple
from common import default_key


Case = namedtuple('Case', 'desc array key')


def get_cases():
    return (
        Case(desc='Empty', array=[], key=None),
        Case(desc='Single', array=[1], key=None),
        Case(desc='8 elements #0', array=[1, 8, 2, 7, 3, 6, 4, 5], key=None),
        Case(desc='8 elements #1 (sorted)', array=[1, 2, 3, 4, 5, 6, 7, 8], key=None),
        Case(desc='8 elements #2 (reversely sorted)', array=[8, 7, 6, 5, 4, 3, 2, 1], key=None),
        Case(desc='1000 elements #0 (sorted)', array=[i + 1 for i in xrange(0, 1000)], key=None),
        Case(desc='1000 elements #1 (reversely sorted)', array=[i + 1 for i in xrange(999, -1, -1)], key=None),
    )


def check_is_sorted(array, key=None):
    if not array:
        return True

    key = key or default_key
    for i in xrange(0, len(array) - 1):
        if key(array[i]) > key(array[i + 1]):
            return False

    return True
