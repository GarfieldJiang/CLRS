from unittest import TestCase
from random import randint
from Common.common import rand_permutate
from collections import namedtuple
from .selection_in_linear_time import select, rand_select
from .problem_9_3 import select_variant


class TestSelection(TestCase):
    def test_selection(self):
        case_class = namedtuple('case_class', 'array i key expected_res')
        for select_method in (rand_select, select, select_variant,):
            cases = (
                case_class(array=[1], i=0, key=None, expected_res=1),
                case_class(array=[3, 2, 1], i=0, key=None, expected_res=1),
                case_class(array=[1, 3, 5, 4, 2, 7, 6], i=4, key=None, expected_res=5),
                case_class(array=[1, 3, 5, 4, 2, 7, 6], i=2, key=None, expected_res=3),
                case_class(array=[1, 3, 5, 4, 2, 7, 6], i=6, key=lambda x: -x, expected_res=1),
                case_class(array=[8, 3, 2, 4, 6, 9, 7, 5, 1], i=0, key=None, expected_res=1),
                case_class(array=[16, 196, 64, 121, 144, 9, 36, 0, 49, 100, 4, 81, 169, 1, 25], i=4, key=None,
                           expected_res=16),
                case_class(array=[1, 16, 4, 9, 49, 100, 25, 36, 81, 64, 0], i=0, key=None, expected_res=0),
            )

            for case in cases:
                # print(case.array, case.i)
                self.assertEqual(case.expected_res, select_method(case.array, case.i, case.key))

            for length in range(1, 100):
                i = randint(0, length - 1)
                array = [x * x for x in range(0, length)]
                rand_permutate(array)
                case = case_class(array=array, i=i, key=None, expected_res=i * i)
                # print(case.array, case.i)
                self.assertEqual(case.expected_res, select_method(case.array, case.i, case.key))