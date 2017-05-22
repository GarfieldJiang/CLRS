# This Python file uses the following encoding: utf-8
"""
Problem: Suppose there is a 8x8 chess board, each of whose tile stores a number as the tile's value. Cut the chess board
(n - 1) times to make n pieces (0 < n <= 15), so that each cut goes along the row or column direction to split the
current remaining chess board into two parts, where one is considered as a piece and the other the new remaining chess
board. The value of one piece is defined as the sum of the values contained in its tiles. Find the minimum possible
variance (square deviation) of the values of the pieces, given the board and n.

Note: This problem is Example 2 of Section 1.5 in the book 算法艺术与信息学竞赛, written by 刘汝佳 and 黄亮, published
by 清华大学出版社, 2004.
"""

import unittest


def cut_chess_board(board, n):
    # print 'n = %d, board = %s' % (n, board)
    assert n > 0 and type(n) is int, 'n must be an integer greater than zero.'
    assert board is not None, 'board must not be None.'
    m = len(board)
    for i in xrange(0, m):
        assert len(board[i]) == m, 'board must be square.'

    if m == 0:
        return -1

    sums = {}
    scores = {}
    __calc_chess_board_cutting(board, sums, scores, 0, 0, m, m, n)
    final_score = scores[(0, 0, m, m, n)]
    if final_score < 0:
        return -1
    return final_score * 1.0 / n


def __calc_chess_board_cutting(board, sums, scores, i, j, h, w, n):
    if (i, j, h, w, n) in scores:
        return scores[(i, j, h, w, n)]

    if n == 1:
        __ensure_sum(board, sums, i, j, h, w)
        scores[(i, j, h, w, n)] = 0
        # print 'calculated score: (%d, %d, %d, %d, %d), result is %.2f' % (i, j, h, w, n, 0)
        return 0

    score = -1
    for newh in xrange(1, h):
        new_score = __calc_score_for_one_and_n_minus_one(
            board, sums, scores, (i, j, newh, w, 1), (i + newh, j, h - newh, w, n - 1), n
        )
        if (score < 0 or new_score < score) and new_score >= 0:
            score = new_score

    for newh in xrange(1, h):
        new_score = __calc_score_for_one_and_n_minus_one(
            board, sums, scores, (i + newh, j, h - newh, w, 1), (i, j, newh, w, n - 1), n
        )
        if (score < 0 or new_score < score) and new_score >= 0:
            score = new_score

    for neww in xrange(1, w):
        new_score = __calc_score_for_one_and_n_minus_one(
            board, sums, scores, (i, j, h, neww, 1), (i, j + neww, h, w - neww, n - 1), n
        )
        if (score < 0 or new_score < score) and new_score >= 0:
            score = new_score

    for neww in xrange(1, w):
        new_score = __calc_score_for_one_and_n_minus_one(
            board, sums, scores, (i, j + neww, h, w - neww, 1), (i, j, h, neww, n - 1), n
        )
        if (score < 0 or new_score < score) and new_score >= 0:
            score = new_score

    # print 'calculated score: (%d, %d, %d, %d, %d), result is %.2f' % (i, j, h, w, n, 0)
    scores[(i, j, h, w, n)] = score


def __calc_score_for_one_and_n_minus_one(board, sums, scores, one_key, n_minus_one_key, n):
    __calc_chess_board_cutting(board, sums, scores, *n_minus_one_key)
    score_n_minus_1 = scores[n_minus_one_key]
    if score_n_minus_1 < 0:
        return -1

    __ensure_sum(board, sums, *one_key[0:-1])
    __ensure_sum(board, sums, *n_minus_one_key[0:-1])
    new_score = score_n_minus_1 + (n - 1.0) / n * (
        pow(sums[one_key[0:-1]] - 1.0 / (n - 1) * sums[n_minus_one_key[0:-1]], 2)
    )
    return new_score


def __ensure_sum(board, sums, i, j, h, w):
    if (i, j, h, w) in sums:
        return

    assert h >= 1 and w >= 1, 'h and w should be both no less than 1.'

    if h == 1 and w == 1:
        sums[(i, j, h, w)] = board[i][j]
        # print 'calculated sum: (%d, %d, %d, %d), result is %d' % (i, j, h, w, sums[(i, j, h, w)])
        return

    if h == 1:
        __ensure_sum(board, sums, i, j, 1, 1)
        __ensure_sum(board, sums, i, j + 1, 1, w - 1)
        sums[(i, j, h, w)] = sums[(i, j, 1, 1)] + sums[(i, j + 1, 1, w - 1)]
        # print 'calculated sum: (%d, %d, %d, %d), result is %d' % (i, j, h, w, sums[(i, j, h, w)])
        return

    __ensure_sum(board, sums, i, j, 1, w)
    __ensure_sum(board, sums, i + 1, j, h - 1, w)
    sums[(i, j, h, w)] = sums[(i, j, 1, w)] + sums[(i + 1, j, h - 1, w)]
    # print 'calculated sum: (%d, %d, %d, %d), result is %d' % (i, j, h, w, sums[(i, j, h, w)])


class TestChessBoardCutting(unittest.TestCase):
    def test_empty(self):
        res = cut_chess_board((), 1)
        self.assertEqual(res, -1)

    def test_single(self):
        res = cut_chess_board(((100,),), 1)
        self.assertAlmostEqual(res, 0.0)

        res = cut_chess_board(((100,),), 2)
        self.assertEqual(res, -1)

    def test_2x2(self):
        res = cut_chess_board((
            (5, 5),
            (3, 6),
        ), 1)
        self.assertAlmostEqual(res, 0.0)

        res = cut_chess_board((
            (5, 5),
            (3, 6),
        ), 2)
        self.assertAlmostEqual(res, 0.25)

    def test_3x3(self):
        res = cut_chess_board((
            (4, 4, 4),
            (6, 1, 3),
            (6, 3, 5),
        ), 3)
        self.assertAlmostEqual(res, 0.0)

        res = cut_chess_board((
            (6, 6, 4),
            (1, 3, 4),
            (3, 5, 4),
        ), 3)
        self.assertAlmostEqual(res, 0.0)

        res = cut_chess_board((
            (1, 2, 3),
            (4, 5, 6),
            (5, 7, 10),
        ), 2)
        self.assertAlmostEqual(res, 0.25)

        res = cut_chess_board((
            (1, 2, 3),
            (4, 5, 6),
            (5, 7, 11),
        ), 2)
        self.assertAlmostEqual(res, 1)

    def test_8x8(self):
        board = (
            (12, 12, 12, 12, 12, 5, 5, 5),
            (12, 12, 12, 12, 12, 5, 5, 5),
            (15, 15, 30, 60, 60, 5, 5, 5),
            (15, 15, 30, 20, 20, 5, 5, 5),
            (15, 15, 30, 20, 20, 5, 5, 5),
            (15, 15, 30, 20, 20, 5, 5, 5),
            (12, 12, 12, 12, 12, 5, 5, 5),
            (12, 12, 12, 12, 12, 5, 5, 5),
        )

        res = cut_chess_board(board, 7)
        self.assertAlmostEqual(res, 0)

        board = (
            (12, 12, 12, 12, 12, 5, 5, 5),
            (12, 12, 12, 13, 12, 5, 5, 5),
            (15, 14, 30, 61, 60, 5, 5, 5),
            (15, 15, 30, 20, 20, 6, 5, 5),
            (15, 15, 29, 20, 20, 5, 5, 5),
            (15, 15, 30, 20, 20, 5, 5, 5),
            (12, 12, 11, 12, 12, 5, 5, 5),
            (12, 12, 12, 12, 12, 5, 5, 5),
        )

        res = cut_chess_board(board, 7)
        self.assertAlmostEqual(res, 6.0 / 7)

        board = (
            (60, 60, 60, 60, 60, 60, 60, 105),
            (60, 60, 60, 60, 60, 60, 60, 105),
            (115, 140, 210, 210, 210, 210, 168, 105),
            (125, 140, 210, 420, 420, 280, 168, 105),
            (135, 140, 210, 420, 840, 280, 168, 105),
            (145, 140, 210, 420, 839, 280, 168, 105),
            (155, 140, 210, 280, 280, 280, 168, 105),
            (165, 140, 168, 168, 168, 168, 168, 106),
        )

        res = cut_chess_board(board, 14)
        self.assertAlmostEqual(res, 1.0 / 7)
