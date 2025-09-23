from typing import Callable, Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class Collection(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None):
        self._data: List[T] = list(items or [])
        self._mod_count = 0

    def add(self, item: T):
        self._data.append(item)
        self._mod_count += 1

    def remove_at(self, index: int) -> T:
        val = self._data.pop(index)
        self._mod_count += 1
        return val

    def get(self, index: int) -> T:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    @property
    def mod_count(self) -> int:
        return self._mod_count

    def snapshot(self) -> List[T]:
        return list(self._data)


class Cursor(Generic[T]):
    def __init__(
        self,
        collection: Collection[T],
        start: Optional[int] = None,
        reverse: bool = False,
        step: int = 1,
        predicate: Optional[Callable[[T], bool]] = None,
        use_snapshot: bool = False,
    ):
        self._collection = collection
        self._step = max(1, step)
        self._reverse = bool(reverse)
        self._pred = predicate or (lambda x: True)
        self._snapshot_mode = bool(use_snapshot)
        self._source_list = collection.snapshot() if self._snapshot_mode else None
        self._expected_mod = None if self._snapshot_mode else collection.mod_count

        size = len(self._source_list) if self._snapshot_mode else len(collection)
        if size == 0:
            self._next_index = None
        else:
            if start is None:
                self._next_index = size - 1 if self._reverse else 0
            else:
                idx = start + size if start < 0 else start
                self._next_index = idx if 0 <= idx < size else None

        self._last_returned: Optional[int] = None

    def _check_mod(self):
        if self._snapshot_mode:
            return
        if self._collection.mod_count != self._expected_mod:
            raise RuntimeError("Collection modified during traversal")

    def _get_size(self) -> int:
        return len(self._source_list) if self._snapshot_mode else len(self._collection)

    def _get_item(self, idx: int) -> T:
        return self._source_list[idx] if self._snapshot_mode else self._collection.get(idx)

    def _passes(self, idx: int) -> bool:
        try:
            return self._pred(self._get_item(idx))
        except Exception:
            return False

    def _find_next_from(self, start: Optional[int]) -> Optional[int]:
        if start is None:
            return None
        size = self._get_size()
        step = self._step if not self._reverse else -self._step
        idx = start
        while 0 <= idx < size:
            if self._passes(idx):
                return idx
            idx += step
        return None

    def __iter__(self):
        return self

    def __next__(self) -> T:
        self._check_mod()
        self._next_index = self._find_next_from(self._next_index)
        if self._next_index is None:
            raise StopIteration
        value = self._get_item(self._next_index)
        self._last_returned = self._next_index
        size = self._get_size()
        if self._reverse:
            candidate = self._next_index - self._step
        else:
            candidate = self._next_index + self._step
        self._next_index = candidate if 0 <= candidate < size else None
        return value

    def remove_current(self):
        if self._last_returned is None:
            raise RuntimeError("No current element to remove")
        if self._snapshot_mode:
            raise RuntimeError("Cannot remove from a snapshot view")
        self._check_mod()
        removed_idx = self._last_returned
        self._collection.remove_at(removed_idx)
        self._expected_mod = self._collection.mod_count
        size = len(self._collection)
        if self._reverse:
            candidate = removed_idx - self._step
            self._next_index = candidate if 0 <= candidate < size else None
        else:
            # After removal indices shift left; next element occupies removed_idx
            candidate = removed_idx
            self._next_index = candidate if 0 <= candidate < size else None
        self._last_returned = None

    def clone(self) -> "Cursor[T]":
        clone = Cursor(
            collection=self._collection,
            start=0,
            reverse=self._reverse,
            step=self._step,
            predicate=self._pred,
            use_snapshot=self._snapshot_mode,
        )
        clone._source_list = None if not self._snapshot_mode else list(self._source_list)
        clone._expected_mod = None if self._snapshot_mode else self._collection.mod_count
        clone._next_index = self._next_index
        clone._last_returned = self._last_returned
        return clone

    def to_list(self) -> List[T]:
        copy = self.clone()
        results: List[T] = []
        for x in copy:
            results.append(x)
        return results


if __name__ == "__main__":
    coll = Collection(["a", "b", "c", "d", "e"])
    cur = Cursor(coll, step=1)
    print("Forward traversal:")
    for x in cur:
        print(x)
    cur = Cursor(coll, reverse=True, step=1)
    print("Reverse with removal demonstration:")
    # remove middle element during traversal
    it = iter(cur)
    print(next(it))  # e
    print(next(it))  # d
    cur2 = cur  # reference to same cursor
    cur2.remove_current()  # remove d
    print("After removal, continue reverse:")
    for x in cur2:
        print(x)
    print("Snapshot isolation:")
    snap = Cursor(coll, use_snapshot=True)
    coll.add("f")
    print("Collection length:", len(coll))
    print("Snapshot traversal (should not see 'f'):", snap.to_list())