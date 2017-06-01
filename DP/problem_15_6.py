import unittest


class EmployeeNode(object):
    def __init__(self, id):
        self.id = id
        self.first_child = None
        self.next_sibling = None
        self.score = 0


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
        score_without_self += first_child.get_score()
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
    return tuple(guest_list)


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
