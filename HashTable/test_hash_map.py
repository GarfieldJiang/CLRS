from unittest import TestCase
from .hash_table_common import DEFAULT_CAPACITY_ANTILOG
from .hash_table import HashMap as HashMapChaining
from .open_addressing import HashMap as HashMapOpenAddressing
from random import randint


class TestOpenAddressing(TestCase):
    def test_basic_use(self):
        for hash_map in (HashMapChaining(), HashMapOpenAddressing(),):
            print(type(hash_map))
            hash_map[1] = 3
            hash_map[2] = 4
            hash_map[10] = 5
            hash_map[18] = 6
            self.assertDictEqual({1: 3, 2: 4, 10: 5, 18: 6}, dict(hash_map))
            self.assertEqual(4, len(hash_map))
            self.assertEqual(1 << DEFAULT_CAPACITY_ANTILOG, hash_map.capacity)

            self.assertRaises(KeyError, lambda: hash_map.pop(100))
            hash_map.pop(1)
            self.assertDictEqual({2: 4, 10: 5, 18: 6}, dict(hash_map))
            self.assertTrue(2 in hash_map)
            self.assertTrue(10 in hash_map)
            self.assertTrue(18 in hash_map)
            self.assertFalse(1 in hash_map)
            self.assertEqual(3, len(hash_map))
            hash_map.pop(10)
            hash_map.pop(18)
            self.assertDictEqual({2: 4}, dict(hash_map))
            self.assertEqual(1, len(hash_map))

            end = 34
            for k in range(end):
                hash_map[k] = k * k
            self.assertDictEqual({k: k * k for k in range(end)}, dict(hash_map))
            self.assertEqual(end, len(hash_map))
            self.assertEqual(1 << (DEFAULT_CAPACITY_ANTILOG + 3), hash_map.capacity)
            self.assertSetEqual(set([k for k in range(end)]), set(hash_map.keys()))
            self.assertSetEqual(set([k * k for k in range(end)]), set(hash_map.values()))

            for k in range(end):
                hash_map.pop(k)
            self.assertDictEqual({}, dict(hash_map))
            self.assertEqual(0, len(hash_map))
            self.assertEqual(1 << (DEFAULT_CAPACITY_ANTILOG + 3), hash_map.capacity)

    def test_random_ops(self):
        for hash_map in (HashMapChaining(), HashMapOpenAddressing(),):
            print(type(hash_map))
            my_dict = {}
            for i in range(0, 100):
                op = randint(0, 2)  # 0: del, not 0: set item
                if len(my_dict) == 0:
                    op = 1

                if op == 0:
                    keys = list(my_dict.keys())
                    k = keys[randint(0, len(keys) - 1)]
                    print('delete k=%d' % k)
                    my_dict.pop(k)
                    hash_map.pop(k)
                else:
                    k = randint(1, 10000)
                    v = randint(1, 100)
                    print('insert k=%d, v=%d' % (k, v))
                    my_dict[k] = v
                    hash_map[k] = v

                self.assertDictEqual(my_dict, dict(hash_map))
                self.assertSetEqual(set(my_dict.keys()), set(hash_map.keys()))
                self.assertSetEqual(set(my_dict.values()), set(hash_map.values()))
                self.assertEqual(len(my_dict), len(hash_map))
                print(my_dict)
