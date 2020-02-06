from unittest import TestCase
from P7_SelectedTopics.NumberTheory.gcd import extended_euclid


def solve_modular_linear_equations(a: int, b: int, n: int):
    """Solve equation ax ≡ b (mod n) for x."""
    assert n > 0 and b >= 0
    if a >= n:
        a = a % n
    assert a > 0
    d, x_prime, _ = extended_euclid(a, n)
    if b % d != 0:
        return []
    solutions = [None] * d
    solutions[0] = (x_prime * (b // d)) % n
    for i in range(1, d):
        solutions[i] = (solutions[0] + i * (n // d)) % n
    return solutions


def multiplicative_inverse(a: int, n: int):
    """Get multiplicative inverse of a modulo n, if existing."""
    assert n > 0
    if a >= n:
        a = a % n
    assert a > 0
    d, x_prime, _ = extended_euclid(a, n)
    if d > 1:
        return None
    return x_prime % n


class TestGCD(TestCase):
    def test_solve_modular_linear_equations(self):
        cases = (
            (14, 30, 100, (95, 45)),
            (35, 10, 50, (6, 16, 26, 36, 46)),
        )

        for case in cases:
            a, b, n, expected_solutions = case[0], case[1], case[2], case[3]
            solutions = solve_modular_linear_equations(a, b, n)
            self.assertSetEqual(set(expected_solutions), set(solutions))

    def test_multiplicative_inverse(self):
        cases = (
            (1, 15, 1),
            (7, 15, 13),
            (11, 15, 11),
            (8, 15, 2),
            (3, 6, None),
        )

        for case in cases:
            a, n, expected_result = case[0], case[1], case[2]
            result = multiplicative_inverse(a, n)
            self.assertEqual(expected_result, result)
