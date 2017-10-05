from unittest import TestCase
from collections import namedtuple
from HeapSort.heap_sort import heap_sort


class Task(object):
    def __init__(self, deadline, penalty):
        assert isinstance(deadline, int) and deadline > 0
        assert penalty > 0

        self._penalty = penalty
        self._deadline = deadline

    @property
    def deadline(self):
        return self._deadline

    @property
    def penalty(self):
        return self._penalty


def _check_input_or_error(tasks):
    if not tasks:
        return
    n = len(tasks)
    for task in tasks:
        assert task.deadline <= n


def _check_independent(tasks, indices, length):
    """
    Ex 16.5-2. O(|A|) running time algorithm to check wether a set A of tasks are independent.
    :param tasks: all the tasks.
    :param indices: indices of tasks to consider. 
    :param length: indices[0:length] will be considered, which means that length = |A|.
    :return: whether the tasks considered are independent.
    """
    deadline_counts = [0] * length
    for i in range(0, length):
        task = tasks[indices[i]]
        if task.deadline - 1 >= length:
            continue
        deadline_counts[task.deadline - 1] += 1

    cumulative_deadline_counts = 0
    for i in range(0, length):
        cumulative_deadline_counts += deadline_counts[i]
        if cumulative_deadline_counts > i + 1:
            return False

    return True


def schedule_task(tasks):
    """
    O(n^2) running time algorithm to schedule unit-time tasks with deadlines and penalties to get the minimum total
    penalty.
    :param tasks: tasks to consider. 
    :return: the optimal schedule of 'early' tasks.
    """
    _check_input_or_error(tasks)
    n = len(tasks)
    tasks = list(tasks)
    for i in range(0, n):
        tasks[i].index = i
    heap_sort(tasks, lambda t: -t.penalty)
    schedule_on_sorted = [-1] * n
    early_count = 0

    for i in range(0, n):
        schedule_on_sorted[early_count] = i
        if _check_independent(tasks, schedule_on_sorted, early_count + 1):
            early_count += 1

    schedule = [-1] * early_count
    for i in range(0, early_count):
        schedule[i] = schedule_on_sorted[i]
    heap_sort(schedule, lambda index: tasks[index].deadline)
    for i in range(0, early_count):
        schedule[i] = tasks[schedule[i]].index

    return tuple(schedule)


class TestTaskScheduling(TestCase):
    def test_task_scheduling(self):
        case_class = namedtuple('Case', 'desc tasks schedules')
        cases = (
            case_class(desc='Empty', tasks=(), schedules=(
                (),
            )),
            case_class(desc='Single', tasks=(
                Task(1, 10),
            ), schedules=(
                (0,),
            )),
            case_class(desc='Two early', tasks=(
                Task(1, 10),
                Task(2, 20)
            ), schedules=(
                (0, 1),
            )),
            case_class(desc='Two late', tasks=(
                Task(1, 10),
                Task(1, 20)
            ), schedules=(
                (1,),
            )),
            case_class(desc='Example in textbook', tasks=(
                Task(4, 70),
                Task(2, 60),
                Task(4, 50),
                Task(3, 40),
                Task(1, 30),
                Task(4, 20),
                Task(6, 10),
            ), schedules=(
                (1, 3, 0, 2, 6),
            )),
            case_class(desc='Ex 16.5-1', tasks=(
                Task(4, 10),
                Task(2, 20),
                Task(4, 30),
                Task(3, 40),
                Task(1, 50),
                Task(4, 60),
                Task(6, 70),
            ), schedules=(
                (4, 3, 2, 5, 6),
                (4, 3, 5, 2, 6),
            )),
        )

        for case in cases:
            schedule = schedule_task(case.tasks)
            self.assertTrue(schedule in case.schedules, msg='%s, wrong schedule %s' % (case.desc, schedule))
