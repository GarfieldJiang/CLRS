import unittest


class EmployeeNode(object):
    def __init__(self, the_id, score, first_child=None, next_sibling=None):
        self.id = the_id
        self.first_child = first_child
        self.next_sibling = next_sibling
        self.score = score


def get_guest_list(root):
    """
    Core algorithm of the problem.
    :param root: The root node of the employee tree.
    :return: The maximum conviviality plus the guest list.
    """
    if not root:
        return 0, ()

    score_cache = {}
    _calc_scores(root, score_cache)
    score = score_cache[root.id].get_score()
    guests = _get_guest_list(root, score_cache)
    return score, guests


class _CacheScore(object):
    def __init__(self, score_with_self, score_without_self):
        self.score_with_self = score_with_self
        self.score_without_self = score_without_self

    def get_score(self):
        return max(self.score_with_self, self.score_without_self)


def _calc_scores(employee_node, cache):
    if employee_node.id in cache:
        return

    first_child = employee_node.first_child
    score_with_self = employee_node.score
    score_without_self = 0

    while first_child:
        _calc_scores(first_child, cache)
        cached_score_obj = cache[first_child.id]
        score_with_self += cached_score_obj.score_without_self
        score_without_self += cached_score_obj.get_score()
        first_child = first_child.next_sibling

    assert employee_node.id not in cache, 'Duplicate employee ID %d' % employee_node.id
    cache[employee_node.id] = _CacheScore(score_with_self, score_without_self)


def _get_guest_list(root, score_cache):
    guest_list = []
    root_score_obj = score_cache[root.id]
    if root_score_obj.score_with_self > root_score_obj.score_without_self:
        guest_list.append(root.id)
        _populate_guest_list(root, True, score_cache, guest_list)
    else:
        _populate_guest_list(root, False, score_cache, guest_list)
    return tuple(sorted(guest_list))


def _populate_guest_list(employee_node, with_self, score_cache, guest_list):
    first_child = employee_node.first_child
    while first_child:
        score_obj = score_cache[first_child.id]
        if with_self or score_obj.score_without_self > score_obj.score_with_self:
            _populate_guest_list(first_child, False, score_cache, guest_list)
        else:
            guest_list.append(first_child.id)
            _populate_guest_list(first_child, True, score_cache, guest_list)
        first_child = first_child.next_sibling


class TestParty(unittest.TestCase):
    def test_guest_list(self):
        cases = (
            ('Empty', None, 0, ()),
            ('Rootonly', EmployeeNode(1, 10), 10, (1,)),
            (
                '2 employees where leader has a higher score',
                EmployeeNode(
                    1, 10,
                    first_child=EmployeeNode(2, 5),
                ),
                10, (1,)
            ),
            (
                '2 employees where leaf node has a higher score',
                EmployeeNode(
                    1, 10,
                    first_child=EmployeeNode(2, 20),
                ),
                20, (2,)
            ),
            (
                'A leader has 2 members + leader has advantage',
                EmployeeNode(
                    1, 10,
                    first_child=EmployeeNode
                    (
                        2, 4,
                        first_child=None,
                        next_sibling=EmployeeNode(3, 4)
                    )
                ),
                10, (1,)
            ),
            (
                'A leader has 2 members + members have advantage',
                EmployeeNode(
                    1, 10,
                    first_child=EmployeeNode
                    (
                        2, 4,
                        first_child=None,
                        next_sibling=EmployeeNode(3, 7)
                    )
                ),
                11, (2, 3)
            ),
            (
                '3-layer structure + leader must attend',
                EmployeeNode(
                    1, 10,
                    first_child=EmployeeNode
                    (
                        11, 1,
                        first_child=EmployeeNode
                        (
                            111, 10, next_sibling=EmployeeNode(112, 10, next_sibling=EmployeeNode(113, 10))
                        ),
                        next_sibling=EmployeeNode
                        (
                            12, 1,
                            first_child=EmployeeNode
                            (
                                121, 10, next_sibling=EmployeeNode(122, 10, None),
                            ),
                            next_sibling=EmployeeNode(13, 1)
                        )
                    )
                ),
                60, (1, 111, 112, 113, 121, 122)
            ),
            (
                '3-layer structure + leader must not attend',
                EmployeeNode(
                    1, 10,
                    first_child=EmployeeNode
                    (
                        11, 10,
                        first_child=EmployeeNode
                        (
                            111, 1, next_sibling=EmployeeNode(112, 1, next_sibling=EmployeeNode(113, 1))
                        ),
                        next_sibling=EmployeeNode
                        (
                            12, 10,
                            first_child=EmployeeNode
                            (
                                121, 1, next_sibling=EmployeeNode(122, 6, None),
                            ),
                            next_sibling=EmployeeNode(13, 1)
                        )
                    )
                ),
                21, (11, 12, 13)
            ),
        )
        for desc, tree, expected_score, expected_guest_list in cases:
            score, guest_list = get_guest_list(tree)
            self.assertAlmostEqual(score, expected_score,
                                   msg='%s, score is %.2f, expected score is %2f'
                                       % (desc, score, expected_score))
            self.assertEqual(guest_list, expected_guest_list,
                             msg='%s, guest list is %s, expected guest list is %s'
                                 % (desc, guest_list, expected_guest_list))
