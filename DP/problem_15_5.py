import unittest


class Operations(object):
    COPY = "COPY"
    REPLACE = "REPLACE"
    DELETE = "DELETE"
    INSERT = "INSERT"
    TWIDDLE = "TWIDDLE"
    KILL = "KILL"


class Operation(object):
    def type_name(self):
        raise NotImplementedError()

    def i_increment(self, i, m):
        raise NotImplementedError()

    def j_increment(self, j, n):
        raise NotImplementedError()

    def do(self, i, j, x, z):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return isinstance(other, Operation) and other.type_name() == self.type_name()


class Copy(Operation):
    def type_name(self):
        return Operations.COPY

    def i_increment(self, i, m):
        return i + 1

    def j_increment(self, j, n):
        return j + 1

    def do(self, i, j, x, z):
        z[j] = x[i]

    def __str__(self):
        return 'Copy'


class Replace(Operation):
    def __init__(self, c):
        self.c = c

    def type_name(self):
        return Operations.REPLACE

    def i_increment(self, i, m):
        return i + 1

    def j_increment(self, j, n):
        return j + 1

    def do(self, i, j, x, z):
        z[j] = self.c

    def __str__(self):
        return 'Replace by \'%s\'' % self.c

    def __eq__(self, other):
        return super(Replace, self).__eq__(other) and self.c == other.c


class Delete(Operation):
    def type_name(self):
        return Operations.DELETE

    def i_increment(self, i, m):
        return i + 1

    def j_increment(self, j, n):
        return j

    def do(self, i, j, x, z):
        pass

    def __str__(self):
        return 'Delete'


class Insert(Operation):
    def __init__(self, c):
        self.c = c

    def type_name(self):
        return Operations.INSERT

    def i_increment(self, i, m):
        return i

    def j_increment(self, j, n):
        return j + 1

    def do(self, i, j, x, z):
        z[j] = self.c

    def __str__(self):
        return 'Insert \'%s\'' % self.c

    def __eq__(self, other):
        return super(Insert, self).__eq__(other) and self.c == other.c


class Twiddle(Operation):
    def type_name(self):
        return Operations.TWIDDLE

    def i_increment(self, i, m):
        return i + 2

    def j_increment(self, j, n):
        return j + 2

    def do(self, i, j, x, z):
        z[j] = x[i + 1]
        z[j + 1] = x[i]

    def __str__(self):
        return 'Twiddle'


class Kill(Operation):
    def type_name(self):
        return Operations.KILL

    def i_increment(self, i, m):
        return m

    def j_increment(self, j, n):
        return j

    def do(self, i, j, x, z):
        pass

    def __str__(self):
        return 'Kill'


def _op_factory(op_type, c):
    if op_type == Operations.COPY:
        return Copy()
    if op_type == Operations.REPLACE:
        return Replace(c)
    if op_type == Operations.DELETE:
        return Delete()
    if op_type == Operations.INSERT:
        return Insert(c)
    if op_type == Operations.TWIDDLE:
        return Twiddle()
    if op_type == Operations.KILL:
        return Kill()

    raise ValueError('Unsupported op type \'%s\'' % op_type)


class CachedOperation(object):
    def __init__(self):
        self.i = None
        self.j = None
        self.op = None


def _update_cost(cost, new_cost, cached_op, new_op_type, c, i, j):
    if cost < 0 or new_cost < cost:
        cached_op.op = _op_factory(new_op_type, c)
        cached_op.i = i
        cached_op.j = j
        return new_cost

    return cost


def get_edit_distance(x, y, op_costs):
    """
    Core algorithm of part a. If KILL is available, then the run time is O(m^2 n). Otherwise, the run time is O(mn).
    :param x: The source sequence.
    :param y: The destination sequence.
    :param op_costs: The dictionary that stores the cost of available operations.
    :return: The lowest cost of transforming x to y and the operation sequence.
    """
    m = len(x)
    n = len(y)
    c = [[-1 for _ in xrange(0, n + 1)] for _ in xrange(0, m + 1)]
    c[0][0] = 0
    cached_ops = [[None for _ in xrange(0, n + 1)] for _ in xrange(0, m + 1)]
    for i_j_sum in xrange(1, m + n + 1):
        for i in xrange(max(0, i_j_sum - n), i_j_sum + 1):
            j = i_j_sum - i
            if i > m or j > n:
                continue

            cost = -1
            cached_op = CachedOperation()
            char = y[j - 1] if j >= 1 else ''
            if Operations.COPY in op_costs and i >= 1 and j >= 1 and x[i - 1] == y[j - 1]:
                assert c[i - 1][j - 1] >= 0
                new_cost = c[i - 1][j - 1] + op_costs[Operations.COPY]
                cost = _update_cost(cost, new_cost, cached_op, Operations.COPY, char, i - 1, j - 1)

            if Operations.REPLACE in op_costs and i >= 1 and j >= 1:
                assert c[i - 1][j - 1] >= 0
                new_cost = c[i - 1][j - 1] + op_costs[Operations.REPLACE]
                cost = _update_cost(cost, new_cost, cached_op, Operations.REPLACE, char, i - 1, j - 1)

            if Operations.DELETE in op_costs and i >= 1:
                assert c[i - 1][j] >= 0
                new_cost = c[i - 1][j] + op_costs[Operations.DELETE]
                cost = _update_cost(cost, new_cost, cached_op, Operations.DELETE, char, i - 1, j)

            if Operations.INSERT in op_costs and j >= 1:
                assert c[i][j - 1] >= 0
                new_cost = c[i][j - 1] + op_costs[Operations.INSERT]
                cost = _update_cost(cost, new_cost, cached_op, Operations.INSERT, char, i, j - 1)

            if Operations.TWIDDLE in op_costs and i >= 2 and j >= 2 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1]:
                assert c[i - 2][j - 2] >= 0
                new_cost = c[i - 2][j - 2] + op_costs[Operations.TWIDDLE]
                cost = _update_cost(cost, new_cost, cached_op, Operations.TWIDDLE, char, i - 2, j - 2)

            if Operations.KILL in op_costs and j == n:  # Kill must be the last operation, so j must be already n.
                for i_1 in xrange(0, i):
                    assert c[i_1][j] >= 0
                    new_cost = c[i_1][j] + op_costs[Operations.KILL]
                    cost = _update_cost(cost, new_cost, cached_op, Operations.KILL, char, i_1, j)

            assert cached_op.op is not None
            c[i][j] = cost
            cached_ops[i][j] = cached_op

    ops = []
    i = m
    j = n
    while cached_ops[i][j] is not None:
        assert isinstance(cached_ops[i][j], CachedOperation)
        ops.insert(0, cached_ops[i][j].op)
        i, j = cached_ops[i][j].i, cached_ops[i][j].j
    return c[m][n], tuple(ops)


def run_ops(list_x, list_z, ops, on_op=None):
    """
    Really runs the operations in given x and z in list form.
    :param list_x: source sequence in list form.
    :param list_z: target sequence in list form.
    :param ops: operation sequence.
    :param on_op: callback after each operation is run.
    :return: Nothing, but if the operation sequence is correct, list_z should be equal to list_x.
    """
    i = 0
    j = 0
    m = len(list_x)
    n = len(list_z)
    for op in ops:
        op.do(i, j, list_x, list_z)
        i = op.i_increment(i, m)
        j = op.j_increment(j, n)
        if on_op:
            on_op(list_x, list_z, i, j, op)


_OP_COSTS_FOR_DNA_ALIGNMENT = {
    Operations.REPLACE: 1,
    Operations.COPY: -1,
    Operations.INSERT: 2,
    Operations.DELETE: 2,
}


def get_dna_sequence_similarity(x, y):
    """
    Core algorithm of part b taking use of part a. Only four operation types are available, and their costs are defined
    as above in _OP_COSTS_FOR_DNA_ALIGNMENT.
    :param x: The source sequence.
    :param y: The destination sequence.
    :return: The similarity of the given sequences which is the opposite number of the edit distance, plus the operation
    sequence.
    """
    cost, ops = get_edit_distance(x, y, _OP_COSTS_FOR_DNA_ALIGNMENT)
    return -cost, ops


def print_dna_alignment(x, y, ops):
    """
    Print the result of DNA alignment.
    :param x: The source sequence.
    :param y: The destination sequence.
    :param ops: operation sequence.
    :return: Nothing.
    """
    x_row = []
    y_row = []
    score_row = []

    def append(x_char, y_char, score_char):
        x_row.append(x_char)
        y_row.append(y_char)
        score_row.append(score_char)

    i = 0
    j = 0
    m = len(x)
    n = len(y)
    for op in ops:
        if op.type_name() == Operations.REPLACE:
            append(x[i], op.c, '-')
        elif op.type_name() == Operations.COPY:
            append(x[i], x[i], '+')
        elif op.type_name() == Operations.INSERT:
            append(' ', op.c, '*')
        else:
            assert op.type_name() == Operations.DELETE
            append(x[i], ' ', '*')

        i = op.i_increment(i, m)
        j = op.j_increment(j, n)

    print ''.join(x_row)
    print ''.join(y_row)
    print ''.join(score_row)


class TestEditDistance(unittest.TestCase):
    def test_edit_distance(self):
        cases = (
            ('', '', 'Uniform cost', {
                Operations.COPY: 1,
                Operations.REPLACE: 1,
                Operations.DELETE: 1,
                Operations.INSERT: 1,
                Operations.TWIDDLE: 1,
                Operations.KILL: 1,
            }, 0, ()),

            ('ab', '', 'Cheap kill', {
                Operations.COPY: 10,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 10,
                Operations.KILL: 2.5,
            }, 2.5, (Kill(),)),

            ('ab', '', 'Cheap delete', {
                Operations.COPY: 10,
                Operations.REPLACE: 10,
                Operations.DELETE: 1,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 10,
                Operations.KILL: 10,
            }, 2, (Delete(), Delete())),

            ('ab', 'ba', 'Cheap twiddle, less cheap insert and kill', {
                Operations.COPY: 10,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 1,
                Operations.TWIDDLE: 2.5,
                Operations.KILL: 1,
            }, 2.5, (Twiddle(),)),

            ('ab', 'ba', 'Cheap insert and kill, less cheap twiddle', {
                Operations.COPY: 10,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 1,
                Operations.TWIDDLE: 3.5,
                Operations.KILL: 1,
            }, 3, (Insert('b'), Insert('a'), Kill())),

            ('ab', 'ba', 'Cheap replace and less cheap twiddle', {
                Operations.COPY: 10,
                Operations.REPLACE: 0.5,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 1.5,
                Operations.KILL: 10,
            }, 1, (Replace('b'), Replace('a'))),

            ('abc', 'abc', 'Cheap copy', {
                Operations.COPY: 1,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 10,
                Operations.KILL: 10,
            }, 3, (Copy(), Copy(), Copy())),

            ('abc', 'abc', 'Cheap replace', {
                Operations.COPY: 10,
                Operations.REPLACE: 1,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 10,
                Operations.KILL: 10,
            }, 3, (Replace('a'), Replace('b'), Replace('c'))),

            ('abc', 'abc', 'Cheap insert and kill', {
                Operations.COPY: 10,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 1,
                Operations.TWIDDLE: 10,
                Operations.KILL: 1,
            }, 4, (Insert('a'), Insert('b'), Insert('c'), Kill())),

            ('abc', 'abc', 'Cheap copy', {
                Operations.COPY: 1,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 10,
                Operations.KILL: 10,
            }, 3, (Copy(), Copy(), Copy())),

            ('abc', 'abc', 'Cheap replace and twiddle', {
                Operations.COPY: 10,
                Operations.REPLACE: 1,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 1,
                Operations.KILL: 10,
            }, 3, (Replace('a'), Replace('b'), Replace('c'))),

            ('abc', 'acb', 'Cheap replace and twiddle', {
                Operations.COPY: 10,
                Operations.REPLACE: 1,
                Operations.DELETE: 10,
                Operations.INSERT: 10,
                Operations.TWIDDLE: 1,
                Operations.KILL: 10,
            }, 2, (Replace('a'), Twiddle())),

            ('abc', 'abc', 'Cheap insert and kill', {
                Operations.COPY: 10,
                Operations.REPLACE: 10,
                Operations.DELETE: 10,
                Operations.INSERT: 1,
                Operations.TWIDDLE: 10,
                Operations.KILL: 1,
            }, 4, (Insert('a'), Insert('b'), Insert('c'), Kill())),
        )

        for x, y, desc, op_costs, expected_cost, expected_ops in cases:
            cost, ops = get_edit_distance(x, y, op_costs)
            self.assertAlmostEqual(cost, expected_cost,
                                   msg="From '%s' to '%s', %s, cost is %.2f, expected is %.2f"
                                       % (x, y, desc, cost, expected_cost))
            self.assertEqual(len(ops), len(expected_ops),
                             msg="From '%s' to '%s', %s, ops len is %d, expected ops len is %d"
                                 % (x, y, desc, len(ops), len(expected_ops)))
            op_len = len(ops)
            for i in xrange(0, op_len):
                self.assertEqual(ops[i], expected_ops[i],
                                 msg="From '%s' to '%s', %s, operation %d, op is [%s], expected op is [%s]"
                                     % (x, y, desc, i, ops[i], expected_ops[i]))

            list_x = list(x)
            list_z = [''] * len(y)
            run_ops(list_x, list_z, ops)
            self.assertEqual(y, ''.join(list_z))


def _on_op(list_x, list_z, i, j, op):
    op_str = '%-20s' % op
    x = ''.join(list_x)
    if i < len(x):
        x = '%s\033[4m%s\033[0m%s ' % (x[0:i], x[i:i + 1], x[i + 1:len(x)])
    else:
        x = '%s\033[4m \033[0m' % x
    x = '%-30s' % x
    z = list_z[0:j]
    z = ''.join(z) + '_'
    z = '%-30s' % z
    print ''.join([op_str, x, z])


def _demo_part_a():
    print '==================== PART A ===================='
    x = 'algorithm'
    y = 'altruistic'
    op_costs = {
        Operations.COPY: 1,
        Operations.REPLACE: 2.5,
        Operations.DELETE: 1,
        Operations.INSERT: 2,
        Operations.TWIDDLE: 1,
        Operations.KILL: 1,
    }
    cost, ops = get_edit_distance(x, y, op_costs)
    print 'Transforming x=\'%s\' to y=\'%s\', cost=%.2f' % (x, y, cost)
    run_ops(list(x), [None] * len(y), ops, _on_op)


def _demo_part_b():
    print '==================== PART B ===================='
    x = 'GATCGGCAT'
    y = 'CAATGTGAATC'
    similarity, ops = get_dna_sequence_similarity(x, y)
    print 'Aligning: \'%s\' and \'%s\' Similarity: %.2f' % (x, y, similarity)
    print_dna_alignment(x, y, ops)


if __name__ == '__main__':
    _demo_part_a()
    _demo_part_b()
