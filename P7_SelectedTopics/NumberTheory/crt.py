from unittest import TestCase
from P7_SelectedTopics.NumberTheory.gcd import euclid
from P7_SelectedTopics.NumberTheory.modular_linear_equations import multiplicative_inverse
from typing import Sequence


def crt(equations: Sequence[Sequence]):
    """
    x ≡ a_i (mod n_i), i = 1, 2, ..., k, n_i pairwise relatively prime =>
    equations = ((a_1, n_1), ..., (a_k, n_k).
    :returns (x, n) where n = n_1 * n_2 * ... * n_k.
    """
    k = len(equations)
    assert(k > 1)
    for i in range(0, k):
        for j in range(i + 1, k):
            assert(euclid(equations[i][1], equations[j][1]) == 1)

    n = 1
    for i in range(0, k):
        n *= equations[i][1]

    x = 0
    for i in range(0, k):
        m_i = n // equations[i][1]
        x += equations[i][0] * m_i * multiplicative_inverse(m_i, equations[i][1])
    x = x % n
    return x, n


class TestCRT(TestCase):
    def test_crt(self):
        cases = (
            (((2, 5), (3, 13)), (42, 65)),
            (((4, 5), (5, 11)), (49, 55)),
            (((1, 9), (2, 8), (3, 7)), (10, 504)),
        )

        for case in cases:
            equations = case[0]
            expected_solution = case[1]
            self.assertSequenceEqual(expected_solution, crt(equations))

