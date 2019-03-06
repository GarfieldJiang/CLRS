# This Python file uses the following encoding: utf-8

"""
Problem: given a string of parentheses ('(', ')', '[', ']'), find the minimum number of parentheses to insert to make
the string a valid parenthesis sequence (VPS). The definition of a VPS goes recursively:
- The empty string is a VPS.
- If S is a VPS, then (S) and [S] are VPSes.
- If A and B are VPSes, then AB is a VPS.
For example, '(()' is invalid, and a ')' can be appended to make it valid.

Note: This problem is Example 1 of Section 1.5 in the book 算法艺术与信息学竞赛, written by 刘汝佳 and 黄亮, published
by 清华大学出版社, 2004.
"""

import unittest


LEFT = (
    '(',
    '[',
)

RIGHT = (
    ')',
    ']',
)


def __match(a, b):
    for i in range(0, len(LEFT)):
        if a == LEFT[i]:
            return b == RIGHT[i]

    return False


def __same_side(a, b):
    return (a in LEFT and b in LEFT) or (a in RIGHT and b in RIGHT)


def add_to_make_valid_parantheses(s):
    assert type(s) is str
    n = len(s)
    if n == 0:
        return 0

    for c in s:
        assert c in LEFT or c in RIGHT, "Input string contains illegal symbols"

    b = [[-1 for _ in range(0, n + 1)] for _ in range(0, n + 1)]
    for i in range(1, n + 1):
        b[i][i - 1] = 0
        b[i][i] = 1

    for ji_diff in range(1, n):
        for i in range(1, n + 1 - ji_diff):
            j = i + ji_diff
            if __same_side(s[i - 1], s[j - 1]):
                if s[i] in LEFT:
                    b[i][j] = b[i][j - 1] + 1
                else:
                    b[i][j] = b[i + 1][j] + 1
                continue

            for k in range(i + 1, j + 1):
                new_val = b[i][k - 1] + b[k][j]
                if b[i][j] < 0 or b[i][j] > new_val:
                    b[i][j] = new_val

            new_val = b[i + 1][j - 1]
            if not __match(s[i - 1], s[j - 1]):
                new_val += 2

            if b[i][j] < 0 or b[i][j] > new_val:
                b[i][j] = new_val

    return b[1][n]


class TestAddToMakeValidParentheses(unittest.TestCase):
    def testEmptyString(self):
        self.assertEqual(add_to_make_valid_parantheses(''), 0)

    def testSingleChar(self):
        for s in LEFT + RIGHT:
            self.assertEqual(add_to_make_valid_parantheses(s), 1)

    def testDoubleChars(self):
        for a in LEFT + RIGHT:
            for b in LEFT + RIGHT:
                s = a + b
                res = add_to_make_valid_parantheses(s)
                if a == '(' and b == ')' or a == '[' and b == ']':
                    self.assertEqual(res, 0)
                else:
                    self.assertEqual(res, 2)

    def testTripleChars(self):
        self.assertEqual(add_to_make_valid_parantheses('(()'), 1)
        self.assertEqual(add_to_make_valid_parantheses('([('), 3)
        self.assertEqual(add_to_make_valid_parantheses('((('), 3)
        self.assertEqual(add_to_make_valid_parantheses('])('), 3)
        self.assertEqual(add_to_make_valid_parantheses('([)'), 1)

    def test4Chars(self):
        self.assertEqual(add_to_make_valid_parantheses('(((('), 4)
        self.assertEqual(add_to_make_valid_parantheses('[]()'), 0)
        self.assertEqual(add_to_make_valid_parantheses('[(])'), 2)
        self.assertEqual(add_to_make_valid_parantheses('[()]'), 0)

    def testLongValidStrings(self):
        s = '([' * 100 + '])' * 100
        self.assertEqual(add_to_make_valid_parantheses(s), 0)

    def testLongInvalidStrings(self):
        s = '([' * 100 + ')]' * 100
        self.assertEqual(add_to_make_valid_parantheses(s), 2)

        s = '([' * 100 + ')]' * 99 + ')'
        self.assertEqual(add_to_make_valid_parantheses(s), 1)
