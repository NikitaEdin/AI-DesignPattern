class ConcurrentModificationError(RuntimeError):
    pass


class EndOfCollection(StopIteration):
    pass


class AggregateCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []
        self._mod = 0

    def add(self, item):
        self._items.append(item)
        self._mod += 1

    def remove(self, item):
        self._items.remove(item)
        self._mod += 1

    def get(self, index):
        return self._items[index]

    def size(self):
        return len(self._items)

    def snapshot(self):
        return list(self._items)

    def create_cursor(self, start=None, direction=1, snapshot=False):
        if snapshot:
            data = self.snapshot()
            start_index = len(data) - 1 if start is None and direction < 0 else (0 if start is None else start)
            return CursorSnapshot(data, start_index, direction)
        start_index = start if start is not None else (0 if direction >= 0 else max(0, len(self._items) - 1))
        return Cursor(self, start_index, direction)


class Cursor:
    def __init__(self, collection, index=0, direction=1):
        self._collection = collection
        self._index = index
        self._direction = 1 if direction >= 0 else -1
        self._expected_mod = collection._mod

    def _check_mod(self):
        if self._expected_mod != self._collection._mod:
            raise ConcurrentModificationError("Collection modified during traversal")

    def has_next(self):
        self._check_mod()
        size = self._collection.size()
        if self._direction > 0:
            return 0 <= self._index < size
        return 0 <= self._index < size

    def next(self):
        self._check_mod()
        if not self.has_next():
            raise EndOfCollection("No more elements")
        value = self._collection.get(self._index)
        self._index += self._direction
        return value

    def peek(self):
        self._check_mod()
        if not self.has_next():
            raise EndOfCollection("No more elements")
        return self._collection.get(self._index)

    def reset(self, index=0, direction=None):
        if direction is not None:
            self._direction = 1 if direction >= 0 else -1
        self._index = index
        self._expected_mod = self._collection._mod

    def reverse(self):
        self._direction *= -1

    def position(self):
        return self._index


class CursorSnapshot:
    def __init__(self, data, index=0, direction=1):
        self._data = list(data)
        self._index = index
        self._direction = 1 if direction >= 0 else -1

    def has_next(self):
        size = len(self._data)
        return 0 <= self._index < size

    def next(self):
        if not self.has_next():
            raise EndOfCollection("No more elements in snapshot")
        value = self._data[self._index]
        self._index += self._direction
        return value

    def peek(self):
        if not self.has_next():
            raise EndOfCollection("No more elements in snapshot")
        return self._data[self._index]

    def reset(self, index=0, direction=None):
        if direction is not None:
            self._direction = 1 if direction >= 0 else -1
        self._index = index

    def reverse(self):
        self._direction *= -1

    def position(self):
        return self._index


if __name__ == "__main__":
    coll = AggregateCollection([10, 20, 30, 40, 50])
    cursor = coll.create_cursor()
    while cursor.has_next():
        print("next:", cursor.next())

    cursor = coll.create_cursor(start=4, direction=-1)
    while cursor.has_next():
        print("prev:", cursor.next())

    snap = coll.create_cursor(snapshot=True)
    coll.add(60)
    print("snapshot traversal after external add:")
    while snap.has_next():
        print("snap:", snap.next())

    c2 = coll.create_cursor()
    print("first from c2:", c2.next())
    coll.add(70)
    try:
        print("attempt next after modification:", c2.next())
    except ConcurrentModificationError as err:
        print("concurrent modification detected:", err)