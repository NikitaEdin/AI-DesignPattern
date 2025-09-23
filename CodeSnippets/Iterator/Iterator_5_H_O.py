from typing import Callable, Generic, List, Optional, TypeVar

T = TypeVar("T")

class ItemCollection(Generic[T]):
    def __init__(self, items: Optional[List[T]] = None):
        self._items: List[T] = list(items) if items else []
        self._mod_count = 0

    def add(self, item: T) -> None:
        self._items.append(item)
        self._mod_count += 1

    def remove_at(self, index: int) -> T:
        val = self._items.pop(index)
        self._mod_count += 1
        return val

    def get_at(self, index: int) -> T:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def get_cursor(self, *, start: Optional[int] = None, reverse: bool = False,
                   step: int = 1, predicate: Optional[Callable[[T], bool]] = None):
        return Cursor(self, start=start, reverse=reverse, step=step, predicate=predicate)

    def __iter__(self):
        return self.get_cursor()


class Cursor(Generic[T]):
    def __init__(self, collection: ItemCollection[T], *, start: Optional[int] = None,
                 reverse: bool = False, step: int = 1, predicate: Optional[Callable[[T], bool]] = None):
        self._collection = collection
        self._reverse = bool(reverse)
        self._step = max(1, int(step))
        self._pred = predicate
        n = len(collection)
        if start is None:
            self._index = n - 1 if self._reverse else 0
        else:
            s = int(start)
            if s < 0:
                s = n + s
            if self._reverse:
                if s >= n:
                    s = n - 1
                if s < 0:
                    s = -1
            else:
                if s < 0:
                    s = 0
                if s >= n:
                    s = n
            self._index = s
        self._saved_mod = collection._mod_count
        self._last_returned: Optional[int] = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._saved_mod != self._collection._mod_count:
            raise RuntimeError("collection modified during traversal")
        n = len(self._collection)
        idx = self._index
        while 0 <= idx < n:
            item = self._collection.get_at(idx)
            if not self._pred or self._pred(item):
                self._last_returned = idx
                self._index = idx - self._step if self._reverse else idx + self._step
                return item
            idx = idx - self._step if self._reverse else idx + self._step
        # exhausted; move index out of bounds consistently
        self._index = -1 if self._reverse else n
        raise StopIteration

    def peek(self):
        if self._saved_mod != self._collection._mod_count:
            raise RuntimeError("collection modified during traversal")
        n = len(self._collection)
        idx = self._index
        while 0 <= idx < n:
            item = self._collection.get_at(idx)
            if not self._pred or self._pred(item):
                return item
            idx = idx - self._step if self._reverse else idx + self._step
        raise StopIteration

    def has_next(self) -> bool:
        try:
            return True if self.peek() is not None else True
        except StopIteration:
            return False
        except RuntimeError:
            return False

    def reset(self, start: Optional[int] = None):
        n = len(self._collection)
        if start is None:
            self._index = n - 1 if self._reverse else 0
        else:
            s = int(start)
            if s < 0:
                s = n + s
            if self._reverse:
                if s >= n:
                    s = n - 1
                if s < 0:
                    s = -1
            else:
                if s < 0:
                    s = 0
                if s >= n:
                    s = n
            self._index = s
        self._saved_mod = self._collection._mod_count
        self._last_returned = None
        return self

    def clone(self):
        new = object.__new__(Cursor)
        new._collection = self._collection
        new._reverse = self._reverse
        new._step = self._step
        new._pred = self._pred
        new._index = self._index
        new._saved_mod = self._collection._mod_count
        new._last_returned = self._last_returned
        return new

    def remove(self):
        if self._last_returned is None:
            raise RuntimeError("no element to remove")
        if self._saved_mod != self._collection._mod_count:
            raise RuntimeError("collection modified")
        removed_index = self._last_returned
        self._collection.remove_at(removed_index)
        # adjust next index when elements shifted
        if self._index > removed_index:
            self._index -= 1
        # sync modification baseline
        self._saved_mod = self._collection._mod_count
        self._last_returned = None


if __name__ == "__main__":
    coll = ItemCollection([1, 2, 3, 4, 5, 6])
    cur = coll.get_cursor(start=1, reverse=False, step=2, predicate=lambda x: x % 2 == 0)
    print("Traversal:")
    for x in cur:
        print(x)
    # Demonstrate clone and reset
    c1 = coll.get_cursor(start=None, reverse=True)
    c2 = c1.clone()
    print("Peek c1:", c1.peek())
    print("Has next c2:", c2.has_next())
    print("c1 next:", next(c1))
    c2.reset(start=2)
    print("c2 after reset:")
    while c2.has_next():
        print(next(c2))
    # Demonstrate removal and concurrent modification safety
    c3 = coll.get_cursor()
    print("Before removal:", [coll.get_at(i) for i in range(len(coll))])
    print("c3 next:", next(c3))
    c3.remove()
    print("After removal:", [coll.get_at(i) for i in range(len(coll))])
    try:
        c3.has_next()
    except Exception as e:
        print("Error detected:", e)