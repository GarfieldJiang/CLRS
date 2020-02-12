from random import randint
from P7_SelectedTopics.NumberTheory.gcd import euclid
from P7_SelectedTopics.NumberTheory.rsa import is_prime


def pollard_rho(n: int):
    assert n >= 2
    count = n ** (1/2)
    x = randint(0, n - 1)
    y = x
    i = 0
    k = 2
    while i < count:
        i = i + 1
        x = (x * x - 1) % n
        d = euclid((y - x) % n, n)
        if 1 < d < n:
            return d
        if i == k:
            y = x
            k = k << 1

    return None


def _main():
    composite_count = 0
    failure_count = 0
    for n in range(1000, 5000):
        factor = pollard_rho(n)
        if is_prime(n):
            continue
        else:
            composite_count = composite_count + 1
            if not factor:
                failure_count += 1
    print("Pollard's Rho Heuristic failure rate: %f" % (failure_count / composite_count,))


if __name__ == "__main__":
    _main()
