from typing import Any, Callable, List, Optional


class Sequence:
    def __init__(self, items: Optional[List[Any]] = None):
        self._data = list(items) if items is not None else []
        self._version = 0

    def add(self, item: Any):
        self._data.append(item)
        self._version += 1

    def remove(self, item: Any):
        self._data.remove(item)
        self._version += 1

    def get_count(self) -> int:
        return len(self._data)

    def get_item(self, index: int) -> Any:
        return self._data[index]

    def create_walker(self, direction: str = "forward", predicate: Optional[Callable[[Any], bool]] = None, snapshot: bool = False):
        if direction not in ("forward", "backward"):
            raise ValueError("direction must be 'forward' or 'backward'")
        source = list(self._data) if snapshot else self
        return Walker(source, direction, predicate, snapshot, self._version)


class Walker:
    def __init__(self, source, direction: str, predicate: Optional[Callable[[Any], bool]], snapshot: bool, version_at_creation: int):
        self._source = source
        self._direction = 1 if direction == "forward" else -1
        self._predicate = predicate
        self._snapshot = snapshot
        self._version_at_creation = version_at_creation
        self._reset_indices()

    def _reset_indices(self):
        if self._snapshot:
            self._items = list(self._source)
            self._start = 0
            self._end = len(self._items)
            self._index = self._start if self._direction == 1 else self._end - 1
        else:
            self._items = None
            count = self._source.get_count()
            self._start = 0
            self._end = count
            self._index = self._start if self._direction == 1 else self._end - 1

    def _check_modification(self):
        if not self._snapshot and self._source._version != self._version_at_creation:
            raise RuntimeError("Source changed during traversal")

    def _get_at(self, pos: int) -> Any:
        if self._snapshot:
            return self._items[pos]
        return self._source.get_item(pos)

    def has_more(self) -> bool:
        if not self._snapshot:
            self._check_modification()
            count = self._source.get_count()
            if count != self._end:
                self._end = count
                if self._direction == -1:
                    self._index = min(self._index, self._end - 1)
        idx = self._index
        while 0 <= idx < self._end:
            candidate = self._get_at(idx)
            if self._predicate is None or self._predicate(candidate):
                return True
            idx += self._direction
        return False

    def get_next(self) -> Any:
        if not self._snapshot:
            self._check_modification()
        while 0 <= self._index < self._end:
            candidate = self._get_at(self._index)
            self._index += self._direction
            if self._predicate is None or self._predicate(candidate):
                return candidate
        raise StopIteration

    def peek(self) -> Any:
        if not self._snapshot:
            self._check_modification()
        idx = self._index
        while 0 <= idx < self._end:
            candidate = self._get_at(idx)
            if self._predicate is None or self._predicate(candidate):
                return candidate
            idx += self._direction
        raise StopIteration

    def reset(self):
        self._reset_indices()
        if not self._snapshot:
            self._version_at_creation = self._source._version

    def remaining_count(self) -> int:
        if not self._snapshot:
            self._check_modification()
        count = 0
        idx = self._index
        while 0 <= idx < self._end:
            candidate = self._get_at(idx)
            if self._predicate is None or self._predicate(candidate):
                count += 1
            idx += self._direction
        return count


if __name__ == "__main__":
    seq = Sequence([1, 2, 3, 4, 5, 6])

    even_predicate = lambda x: x % 2 == 0

    walker_live = seq.create_walker(direction="forward", predicate=even_predicate, snapshot=False)
    print("Live traversal (evens):")
    while walker_live.has_more():
        print(walker_live.get_next())

    walker_back = seq.create_walker(direction="backward", predicate=lambda x: x > 2, snapshot=True)
    print("Snapshot backward (>2):")
    try:
        while True:
            print(walker_back.get_next())
    except StopIteration:
        pass

    walker_detect = seq.create_walker(direction="forward", predicate=None, snapshot=False)
    print("Modification detection demo:")
    print("Next:", walker_detect.get_next())
    seq.add(7)
    try:
        print("Next after modification:", walker_detect.get_next())
    except RuntimeError as e:
        print("Raised:", e)

    walker_snapshot = seq.create_walker(direction="forward", predicate=None, snapshot=True)
    print("Snapshot unaffected by later changes:")
    seq.add(8)
    while True:
        try:
            print(walker_snapshot.get_next())
        except StopIteration:
            break