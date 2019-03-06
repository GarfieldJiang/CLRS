from .hash_table_common import DEFAULT_CAPACITY_ANTILOG
from Common.map import Map


class _HashMapBucketNode(object):
    def __init__(self):
        self.key = None
        self.val = None
        self.deleted = False
        self.in_use = False

    def __repr__(self):
        return '{k=%r, v=%r, deleted=%r, in_use=%r}' % (self.key, self.val, self.deleted, self.in_use)

    def __str__(self):
        return repr(self)


class HashMap(Map):
    """Ex. 11.4-2. Simple hash dictionary implementation using open addressing to resolve collisions."""

    def __init__(self, secondary_hash_func):
        self._capacity_antilog = DEFAULT_CAPACITY_ANTILOG
        self._buckets = [_HashMapBucketNode() for _ in range(1 << self._capacity_antilog)]
        self._len = 0
        assert secondary_hash_func
        self._secondary_hash_func = secondary_hash_func

    def __len__(self):
        return self._len

    def __getitem__(self, k):
        i = 0
        while True:
            bucket_index = self._get_bucket_index(k, i)
            bucket = self._buckets[bucket_index]
            if not bucket.in_use:
                break
            if not bucket.deleted and bucket.key == k:
                return bucket.val
            i += 1
            if i == self.capacity:
                break

        raise KeyError(str(k))

    def __setitem__(self, k, v):
        i = 0
        override = False
        not_in_use_index = -1
        deleted_index = -1
        while True:
            bucket_index = self._get_bucket_index(k, i)
            bucket = self._buckets[bucket_index]
            if not bucket.in_use:
                not_in_use_index = bucket_index
                break
            if not bucket.deleted and bucket.key == k:
                override = True
                bucket.val = v
                break
            if deleted_index < 0 and bucket.deleted:
                deleted_index = bucket_index
            i += 1
            if i == self.capacity:
                break

        if override:
            return

        doubling = False
        if self._len == len(self._buckets):
            self._table_doubling()
            doubling = True

        if not doubling:
            index = -1
            if not_in_use_index >= 0:
                index = not_in_use_index
            if index < 0 <= deleted_index:
                index = deleted_index
            if index >= 0:
                self._set_bucket(index, k, v)
                self._len += 1
                return

        if doubling:
            i = 0

        self._do_insert(i, k, v)
        self._len += 1

    def _do_insert(self, i, k, v):
        while True:
            bucket_index = self._get_bucket_index(k, i)
            bucket = self._buckets[bucket_index]
            if not bucket.in_use or bucket.deleted:
                self._set_bucket(bucket_index, k, v)
                break
            i += 1

    def _set_bucket(self, bucket_index, k, v):
        bucket = self._buckets[bucket_index]
        bucket.key = k
        bucket.val = v
        bucket.in_use = True
        bucket.deleted = False

    def __contains__(self, k):
        i = 0
        while True:
            bucket_index = self._get_bucket_index(k, i)
            bucket = self._buckets[bucket_index]
            if not bucket.in_use:
                break
            if not bucket.deleted and bucket.key == k:
                return True
            i += 1
            if i == self.capacity:
                break
        return False

    def __iter__(self):
        for bucket in self._buckets:
            if bucket.in_use and not bucket.deleted:
                yield (bucket.key, bucket.val)

    @property
    def capacity(self):
        return 1 << self._capacity_antilog

    @property
    def capacity_antilog(self):
        return self._capacity_antilog

    def pop(self, k):
        i = 0
        while True:
            bucket_index = self._get_bucket_index(k, i)
            bucket = self._buckets[bucket_index]
            if not bucket.in_use:
                break
            if not bucket.deleted and bucket.key == k:
                bucket.deleted = True
                self._len -= 1
                return
            i += 1
            if i == self.capacity:
                break
        raise KeyError(str(k))

    def keys(self):
        for bucket in self._buckets:
            if bucket.in_use and not bucket.deleted:
                yield bucket.key

    def values(self):
        for bucket in self._buckets:
            if bucket.in_use and not bucket.deleted:
                yield bucket.val

    def _get_bucket_index(self, k, i):
        return (hash(k) + i * (2 * self._secondary_hash_func(k, self._capacity_antilog) + 1)) % len(self._buckets)

    def _table_doubling(self):
        old_buckets = self._buckets
        self._buckets = [_HashMapBucketNode() for _ in range(len(old_buckets) * 2)]
        self._capacity_antilog += 1
        for bucket in old_buckets:
            if bucket.in_use and not bucket.deleted:
                self._do_insert(0, bucket.key, bucket.val)
