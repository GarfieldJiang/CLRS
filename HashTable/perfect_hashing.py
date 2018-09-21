from random import randint
from typing import List, Callable


def _is_prime(n):
    assert isinstance(n, int) and n > 0
    if n == 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _find_prime_no_less_than(n):
    n = max(2, n)
    if n % 2 == 0:
        n += 1
    while not _is_prime(n):
        n += 2
    return n


def _get_hash_func(a, b, m, p):
    return (lambda _: 0) if m == 0 else (lambda k: ((a * k + b) % p) % m)


def _rand_hash_func_params(m, p):
    return (0, 0) if m <= 1 else (randint(1, p), randint(0, p))


class PerfectHashingParams(object):
    def __init__(self):
        self.try_count = None
        self.prime = None
        self.a = None
        self.b = None
        self.ai = None
        self.bi = None
        self.mi = None

    def __str__(self):
        return 'try_count=%d, prime=%d, a=%d, b=%d, ai=%r, bi=%r, mi=%r' %\
               (self.try_count, self.prime, self.a, self.b, self.ai, self.bi, self.mi)


def find_perfect_hashing(key_set):
    """
    :param key_set: non-negative integer SET.
    :return:
    """
    assert key_set
    key_count = len(key_set)
    prime = _find_prime_no_less_than(max(key_set))
    try_count = 1
    while True:
        a, b = _rand_hash_func_params(key_count, prime)
        primary_collisions = [0] * key_count
        primary_hash_func = _get_hash_func(a, b, key_count, prime)
        for k in key_set:
            primary_collisions[primary_hash_func(k)] += 1

        mi = [primary_collisions[i] * primary_collisions[i] for i in range(key_count)]
        too_much_space = (sum(mi) > 4 * key_count)
        if too_much_space:
            try_count += 1
            continue

        ai = [0] * key_count
        bi = [0] * key_count
        secondary_hash_funcs: List[Callable] = [None] * key_count
        secondary_collisions = [([0] * mi[i]) for i in range(key_count)]
        for i in range(key_count):
            ai[i], bi[i] = _rand_hash_func_params(mi[i], prime)
            secondary_hash_funcs[i] = _get_hash_func(ai[i], bi[i], mi[i], prime)

        has_secondary_collision = False
        for k in key_set:
            i = primary_hash_func(k)
            j = secondary_hash_funcs[i](k)
            if secondary_collisions[i][j] > 0:
                has_secondary_collision = True
                break
            secondary_collisions[i][j] += 1

        if has_secondary_collision:
            try_count += 1
            continue

        ret = PerfectHashingParams()
        ret.a = a
        ret.b = b
        ret.ai = tuple(ai)
        ret.bi = tuple(bi)
        ret.prime = prime
        ret.mi = tuple(mi)
        ret.try_count = try_count
        return ret


def _main():
    run_count = 1000
    sum_try_count = 0
    i = None
    for i in range(run_count):
        ret = find_perfect_hashing({10, 22, 37, 40, 52, 60, 70, 72, 75})
        print(ret)
        sum_try_count += ret.try_count
    print("Ave try count: %f" % (sum_try_count / (i + 1)))

if __name__ == '__main__':
    _main()
