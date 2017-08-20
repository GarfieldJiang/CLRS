from heap import max_heapify, build_max_heap, heap_insert
from Common.common import default_key
from Common.sort_utilities import check_is_sorted
from unittest import TestCase


class MaxPriorityQueue(object):
    """
    Max priority queue implementation using max heap.
    """
    def __init__(self, init_array=None, key=None):
        """
        Initializer.
        :param init_array: array whose elements you want to insert at first.
        :param key: key getter function.
        :return: A well-initialized max priority queue.
        """
        self._array = init_array
        self._key = default_key if key is None else key
        if not init_array:
            return

        build_max_heap(init_array, key=self._key)

    def extract_max(self):
        """
        Extracts the max priority element in O(lg n) time, since we call max_heapify. Raises a ValueError if there is
        no element in the priority queue.
        :return: The max priority element.
        """

        if len(self) <= 0:
            ValueError('This priority queue is empty')

        max_elem = self._array[0]
        heap_size = len(self._array) - 1
        self._array[0] = self._array[heap_size]
        del self._array[-1]
        max_heapify(self._array, 0, heap_size, self._key)
        return max_elem

    def get_max(self):
        """
        Gets the max priority element. Raises a ValueError if there is no element in the priority queue.
        :return: The max prioirty element.
        """
        if len(self) <= 0:
            ValueError('This priority queue is empty')

        return self._array[0]

    def insert(self, new_elem):
        """
        Inserts a new element into the prioirty queue in O(log n) time, Optimized by Ex 6.5-6
        :param new_elem: The new element to insert.
        """
        heap_insert(self._array, new_elem, self._key)

    def __len__(self):
        """
        Gets the length of the prioirty queue.
        :return: The length of the prioirty queue.
        """
        return len(self._array)


def _default_reverse_key(x):
    return -x


def merge_sorted_lists(sorted_lists, reverse_key=None):
    """
    Ex 6.5-9, merging sorted lists.
    :param sorted_lists: sorted lists to merge
    :param reverse_key: function to get the decreasing sorting key.
    :return: the newly allocated, merged list.
    """
    reverse_key = reverse_key or _default_reverse_key
    k = len(sorted_lists)
    current_indices = [0] * k

    class Node(object):
        def __init__(self, _list_index):
            self.list_index = _list_index

        def key(self):
            cur_list = sorted_lists[self.list_index]
            elem_index = current_indices[self.list_index]
            return reverse_key(cur_list[elem_index])

    nodes = []
    for i in xrange(0, k):
        nodes.append(Node(i))

    merged_list = []
    pq = MaxPriorityQueue(init_array=nodes, key=lambda node: node.key())
    while len(pq) > 0:
        max_elem = pq.extract_max()
        list_index = max_elem.list_index
        index = current_indices[list_index]
        merged_list.append(sorted_lists[list_index][index])
        current_indices[list_index] += 1
        if current_indices[list_index] < len(sorted_lists[list_index]):
            pq.insert(max_elem)

    return merged_list


class TestMaxPriorityQueue(TestCase):
    def test_max_priority_queue(self):
        init_array = [1, 5, 3, 7, 10, 8]
        pq = MaxPriorityQueue(init_array)
        self.assertEqual(len(pq), len(init_array))
        self.assertEqual(pq.get_max(), max(init_array))
        sorted_array = []
        while len(pq) > 0:
            sorted_array.append(pq.extract_max())
        self.assertTrue(check_is_sorted(sorted_array, lambda x: -x))

        pq.insert(2)
        pq.insert(3)
        pq.insert(4)
        pq.insert(5)
        pq.insert(4)
        pq.insert(3)
        pq.insert(2)
        out_array = []
        while len(pq) > 0:
            out_array.append(pq.extract_max())
        self.assertEqual(out_array, [5, 4, 4, 3, 3, 2, 2])

    def test_merge_sorted_lists(self):
        sorted_lists = (
            (1, 2, 5, 6),
            (3, 4, 9, 10),
            (0, 7, 8, 9),
            (-3, -2, -1, 0, 1, 2, 3, 4),
        )

        merged_list = merge_sorted_lists(sorted_lists)
        self.assertEqual(len(merged_list), sum([len(l) for l in sorted_lists]))
        self.assertTrue(check_is_sorted(merged_list))
