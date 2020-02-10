from unittest import TestCase
from P7_SelectedTopics.NumberTheory.gcd import euclid
from P7_SelectedTopics.NumberTheory.modular_linear_equations import multiplicative_inverse
from P7_SelectedTopics.NumberTheory.power import modular_exp_l2r
from random import randint


def is_prime(n: int):
    assert n > 0
    if n == 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def select_prime(start: int):
    assert start > 0
    if start <= 2:
        return 2
    if start % 2 == 0:
        start += 1
    while True:
        if is_prime(start):
            return start
        start += 2


def select_e(phi_of_n):
    start = 3
    while euclid(start, phi_of_n) != 1:
        start += 2
    return start


def generate_rsa_keys(p: int, q: int):
    n = p * q
    phi_of_n = (p - 1) * (q - 1)
    public_exp = select_e(phi_of_n)
    private_exp = multiplicative_inverse(public_exp, phi_of_n)
    return (public_exp, n), (private_exp, n)


def encrypt_or_decrypt(message, key):
    return modular_exp_l2r(message, key[0], key[1])


class TestRsa (TestCase):
    def test_naive_rsa(self):
        for i in range(10000):
            p = select_prime(randint(100, 1000))
            q = select_prime(randint(100, 1000))
            while q == p:
                q = select_prime(randint(100, 1000))
            public, private = generate_rsa_keys(p, q)
            n = public[1]
            message = randint(0, n)
            # print(message, public, private)
            encrypted = encrypt_or_decrypt(message, private)
            decrypted = encrypt_or_decrypt(encrypted, public)
            # print(message, decrypted)
            self.assertEqual(message, decrypted)



