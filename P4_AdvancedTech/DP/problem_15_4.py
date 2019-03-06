import unittest
import sys
import random
import time


class PrintingNeatlyBase(object):
    """
    Base class for Problem 15-4.
    """

    def __init__(self, word_lens, line_width, score_power):
        """
        :param word_lens: the lengths of the input words.
        :param line_width: the width of a line.
        :param score_power: if it equals p, then the final score to optimize is \sum_i s_i^p, where s_i is the number
        of the trailing spaces at line i, and i will not go to the last line.
        """
        assert word_lens is not None, "word_lens shouldn't be none"
        assert type(line_width) is int and line_width > 0, 'line_width must be positive integral number.'
        assert score_power >= 1, 'score_power must be real number no less than 1.'
        self._word_lens = word_lens
        self._line_width = line_width
        self._score_power = score_power

    def run(self):
        """
        :return: the optimize score, and line numbers after which there should be a line break.
        """
        raise NotImplementedError()


class PrintingNeatlyDPV1(PrintingNeatlyBase):
    """
    O(n^4) time DP method.
    """

    class DPState(object):
        def __init__(self):
            self.score = -1
            self.last_line_used = -1
            self.split_point = -1
            self.new_k = -1

    def run(self):
        n = len(self._word_lens)

        # Say f(i, j, k) is the optimal printing paradigm of words i thru j with k starting spaces a the first line,
        # where k = 0, 1, ..., line_width - 1. Then in states[i][j][k]:
        # - score will be the valid score of f(i, j, k) plus the score of the last line of f(i, j, k).
        # - last_line_used will be the used (occupied) character count of the last line of f(i, j, k).
        # - split_points is the split point h of f(i, j, k) so that f(i, j, k) is the combination of f(i, h - 1, k)
        #   and f(h, j, new_k), where new_k depends on last_line_used[i][h][k].
        # - new_k cache the new_k calculated since 0 is always an option.
        states = [[[PrintingNeatlyDPV1.DPState() for _ in range(0, self._line_width)]
                   for _ in range(0, n)] for _ in range(0, n)]

        for i in range(0, n):
            for k in range(0, self._line_width):
                state = states[i][i][k]
                if k + self._word_lens[i] <= self._line_width:
                    state.score = sys.maxsize if k == 1 else\
                        pow(self._line_width - k - self._word_lens[i], self._score_power)
                    state.last_line_used = k + self._word_lens[i]
                else:
                    state.score = pow(self._line_width - k + 1, self._score_power) +\
                                  pow(self._line_width - self._word_lens[i], self._score_power)
                    state.last_line_used = self._word_lens[i]
                state.new_k = k

        for ji_diff in range(1, n):
            for i in range(0, n - ji_diff):  # starting word index (inclusive)
                j = i + ji_diff  # ending word index (inclusive)
                for k in range(0, self._line_width):  # starting space count of the first line.
                    self.__calc_dp(i, j, k, n, states)
                    # print 'word_count=%d, n=%d, states[%d][%d][%d].score=%d' % (
                    #     ji_diff + 1, n, i, j, k, states[i][j][k].score
                    # )

        line_break_flags = [False] * (n - 1)
        self.__retrieve_line_break_flags(0, n - 1, 0, states, line_break_flags)
        line_breaks = []
        for i in range(0, n - 1):
            if line_break_flags[i]:
                line_breaks.append(i)

        final_state = states[0][n - 1][0]
        final_score = final_state.score - pow(self._line_width - final_state.last_line_used, self._score_power)

        return final_score, tuple(line_breaks)

    def __calc_dp(self, i, j, k, n, states):
        current_state = states[i][j][k]
        old_score_should_reduce = -1
        for h in range(i + 1, j + 1):
            left_state = states[i][h - 1][k]
            assert left_state.score >= 0
            new_k = left_state.last_line_used + 1
            assert 0 <= new_k <= self._line_width + 1
            if new_k >= self._line_width:
                new_k = 0
            for new_k in set((0, new_k)):
                right_state = states[h][j][new_k]
                assert right_state.score >= 0, 'i=%d, j=%d, k=%d, h=%d, new_k=%d, right_state.score=%d' % (
                    i, j, k, h, new_k, right_state.score
                )
                new_score = left_state.score + right_state.score
                if new_k > 0:
                    new_score -= pow(self._line_width - left_state.last_line_used, self._score_power)
                new_score_should_reduce = pow(self._line_width - right_state.last_line_used, self._score_power)
                valid_new_score = new_score - new_score_should_reduce

                old_score = current_state.score
                valid_old_score = old_score - old_score_should_reduce
                if old_score < 0 or (j == n - 1 and valid_new_score < valid_old_score or
                                     j < n - 1 and new_score < old_score):
                    current_state.score = new_score
                    current_state.last_line_used = right_state.last_line_used
                    current_state.split_point = h
                    current_state.new_k = new_k
                    old_score_should_reduce = new_score_should_reduce

    def __retrieve_line_break_flags(self, i, j, k, states, line_break_flags):
        if i == j:
            if i > 0 and (k == 0 or k + self._word_lens[i] > self._line_width):
                line_break_flags[i - 1] = True
            return

        h = states[i][j][k].split_point
        self.__retrieve_line_break_flags(i, h - 1, k, states, line_break_flags)
        new_k = states[i][j][k].new_k
        self.__retrieve_line_break_flags(h, j, new_k, states, line_break_flags)


class PrintingNeatlyDPV2(PrintingNeatlyBase):
    """
    O(n^2) time DP method.
    """

    class DPState(object):
        def __init__(self):
            self.score = -1
            self.new_line = False

    def run(self):
        if len(self._word_lens) == 0:
            return 0, ()

        n = len(self._word_lens)
        states = [[PrintingNeatlyDPV2.DPState() for _ in range(0, self._line_width)] for _ in range(0, n)]
        self.__calc_dp_states(n, states)
        final_score, line_breaks = self.__retrieve_result(n, states)
        return final_score, tuple(line_breaks)

    def __calc_new_score(self, i, k, new_k, new_line, states):
        if new_k >= self._line_width:
            new_k = 0
        ref_state = states[i + 1][new_k]
        score = ref_state.score
        if new_line and k > 0:
            score += pow(self._line_width - k + 1, self._score_power)
        if new_k == 0:
            score += pow(self._line_width - self._word_lens[i] - (0 if new_line else k), self._score_power)
        return score

    def __retrieve_result(self, n, states):
        line_breaks = []
        k = 0
        for i in range(0, n):
            state = states[i][k]
            if state.new_line and i > 0:
                k = self._word_lens[i] + 1
                line_breaks.append(i - 1)
            else:
                k += self._word_lens[i] + 1
            if k >= self._line_width:
                k = 0
        final_state = states[0][0]
        final_score = final_state.score
        return final_score, line_breaks

    def __calc_dp_states(self, n, states):
        for k in range(0, self._line_width):
            state = states[n - 1][k]
            if k == 1:
                state.score = sys.maxsize
            elif k != 0 and k + self._word_lens[n - 1] <= self._line_width:
                state.score = 0
                state.new_line = False
            else:
                state.score = 0 if k == 0 else pow(self._line_width - k + 1, self._score_power)
                state.new_line = True

        for i in range(n - 2, -1, -1):
            for k in range(0, self._line_width):
                state = states[i][k]
                if k == 1:
                    state.score = sys.maxsize
                    continue

                if k == 0 or k + self._word_lens[i] > self._line_width:
                    state.new_line = True
                    state.score = self.__calc_new_score(i, k, self._word_lens[i] + 1, True, states)
                    continue

                no_nl_score = self.__calc_new_score(i, k, self._word_lens[i] + 1 + k, False, states)
                nl_score = self.__calc_new_score(i, k, self._word_lens[i] + 1, True, states)

                if no_nl_score <= nl_score:
                    state.new_line = False
                    state.score = no_nl_score
                else:
                    state.new_line = True
                    state.score = nl_score


class PrintingNeatlyNaive(PrintingNeatlyBase):
    """
    Naive method that enumerates all possibilities.
    """
    def run(self):
        n = len(self._word_lens)
        if n <= 1:
            return 0, ()

        line_break_flags = [False] * (n - 1)
        opt_line_break_flags = [False] * (n - 1)
        score = sys.maxsize
        true_count = 0

        while True:
            current_line_used_count = 0
            feasible, new_score = self.__add_words(current_line_used_count, line_break_flags, n)
            if feasible and new_score < score:
                score = new_score
                for i in range(n - 1):
                    opt_line_break_flags[i] = line_break_flags[i]

            if true_count == n - 1:
                break

            true_count = PrintingNeatlyNaive.__next_line_break_flags(line_break_flags, n)

        line_breaks = []
        for i in range(n - 1):
            if opt_line_break_flags[i]:
                line_breaks.append(i)

        return score, tuple(line_breaks)

    def __add_words(self, current_line_used_count, line_break_flags, n):
        new_score = 0
        feasible = True
        for i in range(n):
            if current_line_used_count == 0:
                current_line_used_count = self._word_lens[i]
            else:
                current_line_used_count += 1 + self._word_lens[i]
                if current_line_used_count > self._line_width:
                    feasible = False
                    break

            if i < n - 1 and line_break_flags[i]:
                new_score += pow(self._line_width - current_line_used_count, 3)
                current_line_used_count = 0
        return feasible, new_score

    @staticmethod
    def __next_line_break_flags(line_break_flags, n):
        true_count = 0
        carry = True
        for i in range(n - 1):
            if carry:
                line_break_flags[i] = not line_break_flags[i]

            if line_break_flags[i]:
                true_count += 1
                carry = False

        return true_count


def demo_print_neatly(paragraph, line_width, score_power, print_neatly_class):
    assert type(paragraph) is str
    assert issubclass(print_neatly_class, PrintingNeatlyBase)
    words = paragraph.split(' ')
    word_lens = [len(word) for word in words]
    start_time = time.time()
    score, line_breaks = print_neatly_class(word_lens, line_width, score_power).run()
    delta_time = time.time() - start_time
    print('DEMO PRINT NEATLY')
    print('class: %s, line width: %d, score: %d, time: %.3fs.' % (print_neatly_class.__name__, line_width, score, delta_time))
    print('=' * (line_width + 2))
    line_break_index = 0
    next_line_break = line_breaks[0] if line_breaks else -1
    line_break_len = len(line_breaks)
    line = '|'
    for word_index in range(0, len(words)):
        if line == '|':
            line += words[word_index]
        else:
            line += ' ' + words[word_index]
        if word_index == next_line_break or word_index == len(words) - 1:
            line += ' ' * (line_width - len(line) + 1) + '|'
            print(line)
            line_break_index += 1
            line = '|'
            next_line_break = -1 if line_break_index >= line_break_len else line_breaks[line_break_index]

    print('=' * (line_width + 2))


class TestPrintNeatly(unittest.TestCase):
    print_neatly_classes = (PrintingNeatlyNaive, PrintingNeatlyDPV1, PrintingNeatlyDPV2)
    print_neatly_dp_classes = (PrintingNeatlyDPV1, PrintingNeatlyDPV2)

    def test_single_word(self):
        for word_len in range(1, 11):
            for line_width in range(word_len, 20):
                for score_power in range(1, 5):
                    for cls in self.print_neatly_classes:
                        score, line_breaks = cls((word_len,), line_width, score_power).run()
                        self.assertEqual(score, 0)
                        self.assertEqual(line_breaks, ())

    def test_double_words(self):
        score_power = 3
        for word_len_0 in range(1, 3):
            for word_len_1 in range(1, 3):
                max_word_len = max(word_len_0, word_len_1)
                for line_width in range(max_word_len, 10):
                    for cls in self.print_neatly_classes:
                        score, line_breaks = cls((word_len_0, word_len_1), line_width, score_power).run()
                        if line_width >= word_len_0 + word_len_1 + 1:
                            self.assertEqual(score, 0)
                            self.assertEqual(line_breaks, ())
                        else:
                            self.assertEqual(score, pow(line_width - word_len_0, score_power))
                            self.assertEqual(line_breaks, (0, ))

    def test_triple_words(self):
        score_power = 3
        for cls in self.print_neatly_classes:
            self.assertEqual(cls((1, 2, 3), 3, score_power).run(), (9, (0, 1)))
            self.assertEqual(cls((1, 3, 2), 3, score_power).run(), (8, (0, 1)))
            self.assertEqual(cls((2, 1, 3), 3, score_power).run(), (9, (0, 1)))
            self.assertEqual(cls((2, 3, 1), 3, score_power).run(), (1, (0, 1)))
            self.assertEqual(cls((1, 2, 3), 4, score_power).run(), (0, (1,)))
            self.assertEqual(cls((1, 3, 2), 4, score_power).run(), (28, (0, 1)))
            self.assertEqual(cls((2, 1, 3), 4, score_power).run(), (0, (1,)))
            self.assertEqual(cls((2, 3, 1), 4, score_power).run(), (9, (0, 1)))
            self.assertEqual(cls((3, 1, 2), 4, score_power).run(), (1, (0,)))
            self.assertEqual(cls((3, 2, 1), 4, score_power).run(), (1, (0,)))
            self.assertEqual(cls((3, 2, 1), 8, score_power).run(), (0, ()))

    def test_weird_triple_words(self):
        score_power = 3
        for cls in self.print_neatly_classes:
            self.assertEqual(cls((3, 1, 3), 3, score_power).run(), (8, (0, 1)))
            self.assertEqual(cls((4, 1, 4), 4, score_power).run(), (27, (0, 1)))

    def test_four_words(self):
        score_power = 3
        for cls in self.print_neatly_classes:
            self.assertEqual(cls((3, 3, 2, 2), 6, score_power).run(), (27, (0, 2)))
            self.assertEqual(cls((3, 2, 3, 2), 6, score_power).run(), (0, (1,)))

    def test_weird_four_words(self):
        score_power = 3
        for cls in self.print_neatly_classes:
            self.assertEqual(cls((2, 1, 1, 4), 4, score_power).run(), (9, (0, 2)))

    def test_six_words(self):
        score_power = 3
        for cls in self.print_neatly_classes:
            res = cls((2, 2, 1, 4, 7, 7), 7, score_power).run()
            self.assertEqual(res, (9, (1, 3, 4)))

            res = cls((2, 2, 1, 4, 7, 7), 12, score_power).run()
            self.assertTrue(res == (125, (2, 4)) or res == (125, (3, 4)))

    def test_randomly(self):
        score_power = 3
        for i in range(0, 100):
            for cls in self.print_neatly_dp_classes:
                word_count = random.randint(3, 13)
                word_lens = []
                for _ in range(word_count):
                    word_lens.append(random.randint(1, 10))
                max_word_len = max(word_lens)
                line_width = random.randint(max_word_len, 10 * max_word_len)
                res_dp = cls(word_lens, line_width, score_power).run()
                res_naive = PrintingNeatlyNaive(word_lens, line_width, score_power).run()
                self.assertEqual(res_dp[0], res_naive[0], 'line_width=%d, word_lens=%r, cls=%r\n%r != %r' %
                                 (line_width, word_lens, cls, res_dp, res_naive))

    def test_selection_from_random(self):
        score_power = 3
        for cls in self.print_neatly_classes:
            line_width = 15
            word_lens = (5, 2, 1, 5, 7, 3, 1)
            res_dp = cls(word_lens, line_width, score_power).run()
            self.assertEqual(res_dp, (133, (2, 4)))


def __main():
    paragraph = (
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, '
        'sed do eiusmod tempor incididunt ut labore et dolore magna '
        'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
        'ullamco laboris nisi ut aliquip ex ea commodo consequat. '
        'Duis aute irure dolor in reprehenderit in voluptate velit '
        'esse cillum dolore eu fugiat nulla pariatur. Excepteur sint '
        'occaecat cupidatat non proident, sunt in culpa qui officia '
        'deserunt mollit anim id est laborum.'
    )

    for cls in (PrintingNeatlyDPV2, PrintingNeatlyDPV1):
        demo_print_neatly(paragraph, 50, 3, cls)
        demo_print_neatly(paragraph, 60, 3, cls)
        demo_print_neatly(paragraph, 70, 3, cls)
        demo_print_neatly(paragraph, 80, 3, cls)


if __name__ == '__main__':
    __main()

