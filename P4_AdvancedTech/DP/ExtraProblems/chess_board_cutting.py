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
import logging

logging.basicConfig(level=logging.WARNING)


def cut_chess_board(board, n):
    return ChessBoardCutter(board, n).run()


class ChessBoardCutter(object):
    def __init__(self, board, n):
        logging.debug('n = %d, board = %s' % (n, board))
        assert n > 0 and type(n) is int, 'n must be an integer greater than zero.'
        assert board is not None, 'board must not be None.'
        self._m = len(board)
        for i in range(0, self._m):
            assert len(board[i]) == self._m, 'board must be square.'

        self._board = board
        self._n = n
        self._get_score = ChessBoardCutter._memoize(self._get_score, {})
        self._get_sum = ChessBoardCutter._memoize(self._get_sum, {})

    @staticmethod
    def _memoize(f, cache):
        def wrapped(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]
        return wrapped

    def run(self):
        if not self._board:
            return -1.0
        final_score = self._get_score(0, 0, self._m, self._m, self._n)
        if final_score < 0.0:
            return -1.0
        return final_score * 1.0 / self._n

    def _get_score(self, i, j, h, w, n):
        if n == 1:
            return 0.0

        score = -1
        for new_h in range(1, h):
            new_score = self._get_score_for_one_and_n_minus_one(
                (i, j, new_h, w, 1), (i + new_h, j, h - new_h, w, n - 1), n
            )
            score = ChessBoardCutter._update_score(score, new_score)

        for new_h in range(1, h):
            new_score = self._get_score_for_one_and_n_minus_one(
                (i + new_h, j, h - new_h, w, 1), (i, j, new_h, w, n - 1), n
            )
            score = ChessBoardCutter._update_score(score, new_score)

        for new_w in range(1, w):
            new_score = self._get_score_for_one_and_n_minus_one(
                (i, j, h, new_w, 1), (i, j + new_w, h, w - new_w, n - 1), n
            )
            score = ChessBoardCutter._update_score(score, new_score)

        for new_w in range(1, w):
            new_score = self._get_score_for_one_and_n_minus_one(
                (i, j + new_w, h, w - new_w, 1), (i, j, h, new_w, n - 1), n
            )
            score = ChessBoardCutter._update_score(score, new_score)

        logging.debug('calculated score: (%d, %d, %d, %d, %d), result is %.2f' % (i, j, h, w, n, score))
        return score

    @staticmethod
    def _update_score(score, new_score):
        if (score < 0 or new_score < score) and new_score >= 0:
            score = new_score
        return score

    def _get_score_for_one_and_n_minus_one(self, one_key, n_minus_one_key, n):
        score_n_minus_1 = self._get_score(*n_minus_one_key)
        if score_n_minus_1 < 0.0:
            return -1.0

        return score_n_minus_1 + (n - 1.0) / n * (
            pow(self._get_sum(*one_key[0:-1]) - 1.0 / (n - 1) * self._get_sum(*n_minus_one_key[0:-1]), 2)
        )

    def _get_sum(self, i, j, h, w):
        assert h >= 1 and w >= 1, 'h and w should be both no less than 1.'

        if h == 1 and w == 1:
            return self._board[i][j]

        if h == 1:
            return self._get_sum(i, j, 1, 1) + self._get_sum(i, j + 1, 1, w - 1)

        return self._get_sum(i, j, 1, w) + self._get_sum(i + 1, j, h - 1, w)


class TestChessBoardCutting(unittest.TestCase):
    def test_chess_board_cutting(self):
        cases = (
            ((), 1, -1, "Empty"),
            (((100,),), 1, 0, "Single, 1 piece"),
            (((100,),), 2, -1, "Single, 2 pieces"),
            ((
                (5, 5),
                (3, 6),
            ), 1, 0, "2x2, 1 piece"),
            ((
                (5, 5),
                (3, 6),
            ), 2, 0.25, "2x2, 2 pieces"),
            ((
                (4, 4, 4),
                (6, 1, 3),
                (6, 3, 5),
            ), 3, 0, "3x3, 3 pieces, 0 variance, #0"),
            ((
                (6, 6, 4),
                (1, 3, 4),
                (3, 5, 4),
            ), 3, 0, "3x3, 3 pieces, 0 variance, #1"),
            ((
                (1, 2, 3),
                (4, 5, 6),
                (5, 7, 10),
            ), 2, 0.25, "3x3, 2 pieces, 0.25 variance"),
            ((
                (1, 2, 3),
                (4, 5, 6),
                (5, 7, 11),
            ), 2, 1, "3x3, 2 pieces, 1 variance"),
            (((100,),), 1, 0, "Single, 1 piece"),
            (((100,),), 2, -1, "Single, 2 pieces"),
            ((
                (5, 5),
                (3, 6),
            ), 1, 0, "2x2, 1 piece"),
            ((
                (5, 5),
                (3, 6),
            ), 2, 0.25, "2x2, 2 pieces"),
            ((
                (4, 4, 4),
                (6, 1, 3),
                (6, 3, 5),
            ), 3, 0, "3x3, 3 pieces, 0 variance, #0"),
            ((
                (6, 6, 4),
                (1, 3, 4),
                (3, 5, 4),
            ), 3, 0, "3x3, 3 pieces, 0 variance, #1"),
            ((
                (1, 2, 3),
                (4, 5, 6),
                (5, 7, 10),
            ), 2, 0.25, "3x3, 2 pieces, 0.25 variance"),
            ((
                (1, 2, 3),
                (4, 5, 6),
                (5, 7, 11),
            ), 2, 1, "3x3, 2 pieces, 1 variance"),
            ((
                (12, 12, 12, 12, 12, 5, 5, 5),
                (12, 12, 12, 12, 12, 5, 5, 5),
                (15, 15, 30, 60, 60, 5, 5, 5),
                (15, 15, 30, 20, 20, 5, 5, 5),
                (15, 15, 30, 20, 20, 5, 5, 5),
                (15, 15, 30, 20, 20, 5, 5, 5),
                (12, 12, 12, 12, 12, 5, 5, 5),
                (12, 12, 12, 12, 12, 5, 5, 5),
            ), 7, 0, "8x8, 7 pieces, 0 variance"),
            ((
                (12, 12, 12, 12, 12, 5, 5, 5),
                (12, 12, 12, 13, 12, 5, 5, 5),
                (15, 14, 30, 61, 60, 5, 5, 5),
                (15, 15, 30, 20, 20, 6, 5, 5),
                (15, 15, 29, 20, 20, 5, 5, 5),
                (15, 15, 30, 20, 20, 5, 5, 5),
                (12, 12, 11, 12, 12, 5, 5, 5),
                (12, 12, 12, 12, 12, 5, 5, 5),
            ), 7, 6.0 / 7, "8x8, 7 pieces, 6/7 variance"),
            ((
                (60, 60, 60, 60, 60, 60, 60, 105),
                (60, 60, 60, 60, 60, 60, 60, 105),
                (115, 140, 210, 210, 210, 210, 168, 105),
                (125, 140, 210, 420, 420, 280, 168, 105),
                (135, 140, 210, 420, 840, 280, 168, 105),
                (145, 140, 210, 420, 839, 280, 168, 105),
                (155, 140, 210, 280, 280, 280, 168, 105),
                (165, 140, 168, 168, 168, 168, 168, 106),
            ), 14, 1.0 / 7, "8x8, 14 pieces, 1/7 variance"),
        )

        for board, n, expected, desc in cases:
            res = cut_chess_board(board, n)
            self.assertAlmostEqual(res, expected, msg="Case: %s. Error: %s != %s" % (desc, res, expected))
