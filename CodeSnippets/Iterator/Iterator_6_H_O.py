class EndOfCollection(Exception):
    pass


class ConcurrentModificationError(RuntimeError):
    pass


class AggregateCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []
        self._mod_count = 0

    def add(self, item):
        self._items.append(item)
        self._mod_count += 1

    def remove_at(self, index):
        if index < 0 or index >= len(self._items):
            raise IndexError("Index out of range")
        value = self._items.pop(index)
        self._mod_count += 1
        return value

    def size(self):
        return len(self._items)

    def get_snapshot(self):
        return list(self._items)

    def create_cursor(self, direction="forward", snapshot=False, start_index=None):
        return Cursor(self, direction=direction, snapshot=snapshot, start_index=start_index)


class Cursor:
    def __init__(self, source_collection, direction="forward", snapshot=False, start_index=None, _seed_snapshot=None):
        self._source = source_collection
        self._snapshot_flag = bool(snapshot) or (_seed_snapshot is not None)
        self._snapshot = list(_seed_snapshot) if _seed_snapshot is not None else (self._source.get_snapshot() if self._snapshot_flag else None)
        self._expected_mod = self._source._mod_count if not self._snapshot_flag else None
        self._direction = -1 if direction == "backward" else 1
        self._reset_index(start_index)

    def _reset_index(self, start_index):
        length = len(self._snapshot) if self._snapshot_flag else self._source.size()
        if start_index is not None:
            idx = start_index
        else:
            idx = (length - 1) if self._direction < 0 else 0
        self._index = idx

    def _check_concurrent_mod(self):
        if not self._snapshot_flag and self._expected_mod != self._source._mod_count:
            raise ConcurrentModificationError("Collection modified during traversal")

    def has_next(self):
        if self._snapshot_flag:
            length = len(self._snapshot)
        else:
            self._check_concurrent_mod()
            length = self._source.size()
        if self._direction > 0:
            return 0 <= self._index < length
        return -1 < self._index < length

    def next(self):
        if not self.has_next():
            raise EndOfCollection("No more elements")
        if self._snapshot_flag:
            value = self._snapshot[self._index]
        else:
            value = self._source._items[self._index]
        self._index += self._direction
        return value

    def peek(self):
        if not self.has_next():
            raise EndOfCollection("No element to peek")
        if self._snapshot_flag:
            return self._snapshot[self._index]
        self._check_concurrent_mod()
        return self._source._items[self._index]

    def reset(self, start_index=None):
        self._reset_index(start_index)
        if not self._snapshot_flag:
            self._expected_mod = self._source._mod_count

    def clone(self):
        seed = list(self._snapshot) if self._snapshot_flag else None
        clone_cursor = Cursor(self._source, direction=("backward" if self._direction < 0 else "forward"),
                              snapshot=self._snapshot_flag, start_index=self._index, _seed_snapshot=seed)
        if not self._snapshot_flag:
            clone_cursor._expected_mod = self._expected_mod
        return clone_cursor


if __name__ == "__main__":
    col = AggregateCollection(["a", "b", "c", "d"])
    snap_cursor = col.create_cursor(direction="forward", snapshot=True)
    live_cursor = col.create_cursor(direction="forward", snapshot=False)

    print("Snapshot traversal:")
    while True:
        try:
            print(snap_cursor.next())
        except EndOfCollection:
            break

    print("Live traversal with concurrent modification detection:")
    try:
        print(live_cursor.next())
        col.add("e")
        print(live_cursor.next())
    except ConcurrentModificationError as e:
        print("Detected modification:", e)

    print("Reverse traversal and cloning:")
    rev = col.create_cursor(direction="backward", snapshot=True)
    print("First element (reverse):", rev.next())
    clone_rev = rev.clone()
    print("Clone next:", clone_rev.next())
    print("Original next:", rev.next())