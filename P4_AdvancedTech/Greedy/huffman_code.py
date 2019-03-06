from Common.tree import BinaryTreeNode, pre_order_traverse_tree
from collections import namedtuple
from unittest import TestCase
from P2_Sorting.HeapSort.priority_queue import MaxPriorityQueue
import logging


logging.getLogger().setLevel(logging.INFO)


class BinaryCodeTreeNode(BinaryTreeNode):
    def __init__(self, symbol, freq):
        super().__init__(None)
        self._symbol = symbol
        assert freq >= 0
        self._freq = freq

    @property
    def symbol(self):
        return self._symbol

    @property
    def freq(self):
        return self._freq


def build_binary_huffman_tree(symbol_freqs):
    if not symbol_freqs:
        return None

    n = len(symbol_freqs)
    nodes = [None for _ in range(0, n)]
    for i in range(0, n):
        nodes[i] = BinaryCodeTreeNode(i, symbol_freqs[i])
    pq = MaxPriorityQueue(nodes, key=lambda node: -node.freq)
    while len(pq) > 1:
        a = pq.extract_max()
        logging.debug('symbol=%s, freq=%.2f' % ('<None>' if a.symbol is None else a.symbol, a.freq))
        b = pq.extract_max()
        logging.debug('symbol=%s, freq=%.2f' % ('<None>' if b.symbol is None else b.symbol, b.freq))
        new_node = BinaryCodeTreeNode(None, a.freq + b.freq)
        new_node.left = a
        new_node.right = b
        a.parent = b.parent = new_node
        pq.insert(new_node)

    return pq.extract_max()


def get_binary_huffman_code_len(root):
    my_dict = {'ret': 0}

    def visit(node):
        if node.left or node.right:
            return

        current = node
        code_len = -1
        while current:
            code_len += 1
            current = current.parent

        logging.debug('symbol=%s, freq=%.2f, code_len=%d' % (node.symbol, node.freq, code_len))
        my_dict['ret'] += node.freq * code_len

    pre_order_traverse_tree(root, visit)
    return my_dict['ret']


class TestHuffmanCode(TestCase):
    def _check_binary_code_tree(self, root, symbol_freqs, desc):
        self.assertTrue(root is None or isinstance(root, BinaryCodeTreeNode),
                        msg='%s, invalid root' % desc)
        if not symbol_freqs:
            self.assertIsNone(root, msg='%s, root should be none' % desc)

        symbol_set = set(range(0, len(symbol_freqs)))

        def visit(node):
            if not node.left and not node.right:
                self.assertIsNotNone(node.symbol, msg='%s, leaf node points to no symbol.' % desc)
                symbol_set.remove(node.symbol)
                return

            if node.left and not node.right or node.right and not node.left:
                self.fail(msg='%s, node has exactly one child.' % desc)

        pre_order_traverse_tree(root, visit)
        self.assertTrue(not symbol_set, '%s, symbols %s are not found.')

    def test_binary_huffman_code(self):
        case_class = namedtuple('Case', 'desc symbol_freqs code_len')
        cases = (
            case_class(desc='Empty symbol set', symbol_freqs=(), code_len=0),
            case_class(desc='Single symbol set', symbol_freqs=(1,), code_len=0),
            case_class(desc='Double symbol set', symbol_freqs=(0.1, 0.9), code_len=1),
            case_class(desc='Example in the text book',
                       symbol_freqs=(45, 13, 12, 16, 9, 5), code_len=224),
        )

        for case in cases:
            logging.debug('case: ' + case.desc)
            root = build_binary_huffman_tree(case.symbol_freqs)
            self._check_binary_code_tree(root, case.symbol_freqs, case.desc)
            code_len = get_binary_huffman_code_len(root)
            self.assertAlmostEqual(code_len, case.code_len, 7,
                                   msg='%s, code length %s != %s' % (case.desc, code_len, case.code_len))
