from .hash_table_common import DEFAULT_CAPACITY_ANTILOG
from Common.map import Map


class _HashMapBucketNode(object):
    def __init__(self):
        self.key = None
        self.val = None
        self.next = None


class HashMap(Map):
    """Simple hash dictionary implementation using chaining to resolve collisions."""

    def __init__(self):
        self._buckets = [None] * (1 << DEFAULT_CAPACITY_ANTILOG)
        self._len = 0

    def __len__(self):
        return self._len

    def __getitem__(self, k):
        i = self._get_bucket_index(k)
        head = self._buckets[i]
        while head is not None:
            if head.key == k:
                return head.val
            head = head.next
        raise KeyError(str(k))

    def __setitem__(self, k, v):
        bucket_index = self._get_bucket_index(k)
        head = self._buckets[bucket_index]
        override = False
        while head is not None:
            if head.key == k:
                head.val = v
                override = True
                break
            head = head.next

        if override:
            return

        if self._len == len(self._buckets):
            self._table_doubling()
            bucket_index = self._get_bucket_index(k)

        head = self._buckets[bucket_index]
        new_head = _HashMapBucketNode()
        new_head.key = k
        new_head.val = v
        new_head.next = head
        self._buckets[bucket_index] = new_head
        self._len += 1

    def __contains__(self, k):
        bucket_index = self._get_bucket_index(k)
        head = self._buckets[bucket_index]
        while head is not None:
            if head.key == k:
                return True
            head = head.next
        return False

    def __iter__(self):
        for bucket in self._buckets:
            head = bucket
            while head:
                yield (head.key, head.value)
                head = head.next

    @property
    def capacity(self):
        return len(self._buckets)

    def pop(self, k):
        bucket_index = self._get_bucket_index(k)
        head = self._buckets[bucket_index]
        prev = None
        while head is not None:
            if head.key == k:
                if prev is not None:
                    prev.next = head.next
                else:
                    self._buckets[bucket_index] = head.next
                self._len -= 1
                return
            prev = head
            head = head.next
        raise KeyError(str(k))

    def keys(self):
        for bucket in self._buckets:
            head = bucket
            while head:
                yield head.key
                head = head.next

    def values(self):
        for bucket in self._buckets:
            head = bucket
            while head:
                yield head.val
                head = head.next

    def _get_bucket_index(self, k):
        return hash(k) % len(self._buckets)

    def _table_doubling(self):
        old_buckets = self._buckets
        self._buckets = [None] * (len(old_buckets) * 2)
        for bucket in old_buckets:
            head = bucket
            while head is not None:
                _next = head.next
                new_bucket_index = self._get_bucket_index(head.key)
                head.next = self._buckets[new_bucket_index]
                self._buckets[new_bucket_index] = head
                head = _next
