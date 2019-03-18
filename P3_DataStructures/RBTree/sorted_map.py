from Common.map import Map
from P3_DataStructures.RBTree.basic_ops import RBTree, rb_insert, rb_pop, rb_search, rb_iter
from unittest import TestCase
from random import randint


class _KeyValuePair(object):
    def __init__(self, k, v):
        self.k = k
        self.v = v


class SortedMap(Map):
    """Simple implementation of a sorted map with a red-black tree."""
    def __init__(self):
        super().__init__()
        self._len = 0
        self._rbt = RBTree(key=lambda kv: kv.k)

    def pop(self, k):
        rbt = self._rbt
        node = rb_search(rbt, k)
        if node == rbt.nil:
            raise KeyError(str(k))
        rb_pop(rbt, node)
        self._len -= 1

    def items(self):
        for kv in rb_iter(self._rbt):
            yield (kv.k, kv.v)

    def __contains__(self, k):
        rbt = self._rbt
        return rb_search(rbt, k) != rbt.nil

    def __setitem__(self, k, v):
        already = rb_search(self._rbt, k)
        if already != self._rbt.nil:
            already.data.v = v
        else:
            rb_insert(self._rbt, _KeyValuePair(k, v))
            self._len += 1

    def __len__(self):
        return self._len

    def __iter__(self):
        yield self.keys()

    def __getitem__(self, k):
        rbt = self._rbt
        node = rb_search(self._rbt, k)
        if node == rbt.nil:
            raise KeyError(str(k))
        return node.data.v

    def values(self):
        for kv in rb_iter(self._rbt):
            yield kv.v

    def keys(self):
        for kv in rb_iter(self._rbt):
            yield kv.k

class TestSortedMap(TestCase):
    def test_basic(self):
        sorted_map = SortedMap()
        insert_count = 10
        for i in range(insert_count):
            sorted_map[i] = i * i
            sorted_map[i] = i * i * i
        self.assertDictEqual({i: i * i * i for i in range(insert_count)}, dict(sorted_map))
        self.assertSequenceEqual([i * i * i for i in range(insert_count)], list(sorted_map.values()))
        for i in range(insert_count):
            self.assertTrue(i in sorted_map)
            self.assertEqual(i * i * i, sorted_map[i])

        self.assertEqual(insert_count, len(sorted_map))
        self.assertFalse(10 in sorted_map)
        self.assertRaises(KeyError, lambda: sorted_map[10])

        for i in range(insert_count):
            sorted_map.pop(i)
            self.assertFalse(i in sorted_map)
            self.assertEqual(insert_count - i - 1, len(sorted_map))

    def test_random_ops(self):
        self.maxDiff = 4096
        sorted_map = SortedMap()
        my_dict = dict()
        for i in range(0, 400):
            op = randint(0, 2)  # 0: del, not 0: set item
            if len(my_dict) == 0:
                op = 1

            if op == 0:
                keys = list(my_dict.keys())
                k = keys[randint(0, len(keys) - 1)]
                my_dict.pop(k)
                sorted_map.pop(k)
            else:
                k = randint(1, 400)
                v = randint(1, 100)
                my_dict[k] = v
                sorted_map[k] = v

            self.assertDictEqual(my_dict, dict(sorted_map))
            self.assertSetEqual(set(my_dict.values()), set(sorted_map.values()))
            self.assertSequenceEqual(sorted(my_dict.keys()), list(sorted_map.keys()))
            self.assertEqual(len(my_dict), len(sorted_map))
            # print(my_dict)
