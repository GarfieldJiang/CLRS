from P7_SelectedTopics.NumberTheory.power import modular_exp_l2r as modular_exp
from P7_SelectedTopics.NumberTheory.rsa import is_prime
from random import randint


def _witness_compositeness(n: int, a: int):
    """
    :param n: The number to check compositeness
    :param a: The candidate witness.
    :return: True if I'm sure n is composite.
    """
    assert n > 1
    if n == 2:
        return False
    pot = 0
    while True:
        if (((n - 1) >> pot) & 1) == 1:
            break
        pot += 1

    odd = (n - 1) // (1 << pot)
    square = modular_exp(a, odd, n)
    for _ in range(pot):
        last_square = square
        square = (square * square) % n
        if square == 1 and last_square != 1 and last_square != n - 1:
            return True
    return square % n != 1


def miller_rabin_is_prime(n: int, times: int):
    assert n > 1
    for _ in range(times):
        a = randint(1, n - 1)
        if _witness_compositeness(n, a):
            return False
    return True


def _main():
    count = 0
    error_count = 0
    prime_count = 0
    times = 3
    for n in range(1000, 10000):
        count += 1
        really_prime = is_prime(n)
        if really_prime:
            prime_count += 1
        if really_prime != miller_rabin_is_prime(n, times):
            error_count += 1
    print("Miller-Rabin algorithm trying %d times, error rate %f, prime rate %f" % (times, (error_count / count), (prime_count / count)))


if __name__ == "__main__":
    __main()
