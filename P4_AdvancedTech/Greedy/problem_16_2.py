from unittest import TestCase
from collections import namedtuple
from P2_Sorting.HeapSort.priority_queue import MaxPriorityQueue
from P2_Sorting.HeapSort.heap_sort import heap_sort
from typing import Sequence


class Task(object):
    def __init__(self, task_id, release_time, processing_time):
        assert isinstance(task_id, int) and task_id >= 0
        assert isinstance(release_time, int) and release_time >= 0
        assert isinstance(processing_time, int) and processing_time > 0
        self._id = task_id
        self._release_time = release_time
        self._processing_time = processing_time

    @property
    def task_id(self):
        return self._id

    @property
    def release_time(self):
        return self._release_time

    @property
    def processing_time(self):
        return self._processing_time


def _populate_queue(tasks: Sequence[Task], index: int, q: MaxPriorityQueue, current_time: int) -> int:
    while index < len(tasks) and tasks[index].release_time == current_time:
        q.insert(tasks[index])
        index += 1
    return index


def schedule_tasks(tasks: Sequence[Task]) -> tuple:
    """
    Problem 16-2(b). Simulates the procedure of processing all the tasks. Running time is O(N log n) where n is the
    number of input tasks and N is the completion time of the whole procedure. Moreover, N <= R + nP, where R is the
    maximum release time of all the tasks and P is the maximum processing time.
    :param tasks: the input tasks.
    :return: Average completion time and the execution order (-1 means idle).
    """
    if not tasks:
        return 0, ()

    tasks = list(tasks)
    heap_sort(tasks, key=lambda t: t.release_time)
    q = MaxPriorityQueue(key=lambda t: -t.processing_time)
    current_time = 0

    index = _populate_queue(tasks, 0, q, current_time)
    seq = []
    complete_time = 0
    while index < len(tasks) or len(q) > 0:
        if len(q) <= 0:
            seq.append(-1)
        else:
            current_task = q.extract_max()
            seq.append(current_task.task_id)
            if current_task.processing_time > 1:
                remaining_task = Task(task_id=current_task.task_id,
                                      release_time=current_task.release_time,
                                      processing_time=current_task.processing_time - 1)
                q.insert(remaining_task)
            else:
                complete_time += current_time + 1

        current_time += 1
        index = _populate_queue(tasks, index, q, current_time)

    return complete_time / len(tasks), tuple(seq)


class TestTaskScheduling(TestCase):
    def test_task_scheduling(self):
        case_class = namedtuple('Case', 'desc tasks average_complete_time execution_seq')
        cases = (
            case_class(desc='Empty', tasks=(), average_complete_time=0, execution_seq=()),
            case_class(desc='Single', tasks=(
                Task(0, 3, 5),
            ), average_complete_time=8, execution_seq=(-1, -1, -1, 0, 0, 0, 0, 0)),
            case_class(desc='Double #0', tasks=(
                Task(0, 0, 5),
                Task(1, 2, 2),
            ), average_complete_time=5.5, execution_seq=(0, 0, 1, 1, 0, 0, 0)),
            case_class(desc='Double #1', tasks=(
                Task(0, 0, 5),
                Task(1, 2, 4),
            ), average_complete_time=7, execution_seq=(0, 0, 0, 0, 0, 1, 1, 1, 1)),
            case_class(desc='Triple #0', tasks=(
                Task(0, 1, 3),
                Task(1, 1, 2),
                Task(2, 1, 1),
            ), average_complete_time=13 / 3, execution_seq=(-1, 2, 1, 1, 0, 0, 0)),
            case_class(desc='Triple #1', tasks=(
                Task(0, 0, 3),
                Task(1, 1, 1),
                Task(2, 6, 1),
            ), average_complete_time=13 / 3, execution_seq=(0, 1, 0, 0, -1, -1, 2)),
            case_class(desc='Triple #2', tasks=(
                Task(0, 0, 5),
                Task(1, 1, 3),
                Task(2, 2, 1),
            ), average_complete_time=17 / 3, execution_seq=(0, 1, 2, 1, 1, 0, 0, 0, 0)),
        )

        for case in cases:
            average_complete_time, execution_seq = schedule_tasks(case.tasks)
            self.assertEqual(execution_seq, case.execution_seq,
                             msg='%s, Execution sequence, %s != %s' % (case.desc, execution_seq, case.execution_seq))
            self.assertAlmostEqual(average_complete_time, case.average_complete_time,
                                   msg='%s, Average complete time, %s != %s' %
                                       (case.desc, average_complete_time, case.average_complete_time))
