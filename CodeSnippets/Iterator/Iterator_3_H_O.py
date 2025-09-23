from typing import Any, Callable, List, Optional

class NoSuchElementError(Exception):
    pass

class ConcurrentModificationError(Exception):
    pass

class IllegalStateError(Exception):
    pass

class CollectionContainer:
    def __init__(self, items: Optional[List[Any]] = None) -> None:
        self._items: List[Any] = list(items) if items else []
        self._mod_count: int = 0

    def add(self, item: Any) -> None:
        self._items.append(item)
        self._mod_count += 1

    def remove_at(self, index: int) -> Any:
        if index < 0 or index >= len(self._items):
            raise IndexError("index out of range")
        value = self._items.pop(index)
        self._mod_count += 1
        return value

    def size(self) -> int:
        return len(self._items)

    def get_at(self, index: int) -> Any:
        return self._items[index]

    def create_cursor(self, forward: bool = True, start: Optional[int] = None,
                      predicate: Optional[Callable[[Any], bool]] = None,
                      live: bool = True):
        return Cursor(self, forward, start, predicate, live)

class Cursor:
    def __init__(self, collection: CollectionContainer, forward: bool = True,
                 start: Optional[int] = None, predicate: Optional[Callable[[Any], bool]] = None,
                 live: bool = True) -> None:
        self._collection = collection
        self._forward = forward
        self._predicate = predicate
        self._live = live
        self._expected_mod = collection._mod_count
        if live:
            if start is None:
                self._index = 0 if forward else collection.size() - 1
            else:
                self._index = start
            self._snapshot = None
        else:
            self._snapshot = list(collection._items)
            if start is None:
                self._index = 0 if forward else len(self._snapshot) - 1
            else:
                self._index = start
        self._last_returned: Optional[int] = None

    def _check_modification(self) -> None:
        if self._live and self._expected_mod != self._collection._mod_count:
            raise ConcurrentModificationError("Collection modified during traversal")

    def _get_source_size(self) -> int:
        return len(self._snapshot) if self._snapshot is not None else self._collection.size()

    def _get_at(self, idx: int) -> Any:
        return self._snapshot[idx] if self._snapshot is not None else self._collection.get_at(idx)

    def has_next(self) -> bool:
        self._check_modification()
        idx = self._index
        size = self._get_source_size()
        step = 1 if self._forward else -1
        while 0 <= idx < size:
            try:
                candidate = self._get_at(idx)
            except IndexError:
                return False
            if self._predicate is None or self._predicate(candidate):
                return True
            idx += step
        return False

    def next_item(self) -> Any:
        self._check_modification()
        size = self._get_source_size()
        step = 1 if self._forward else -1
        while 0 <= self._index < size:
            try:
                candidate = self._get_at(self._index)
            except IndexError:
                break
            current_index = self._index
            self._index += step
            if self._predicate is None or self._predicate(candidate):
                self._last_returned = current_index
                return candidate
        raise NoSuchElementError("No more elements")

    def current(self) -> Any:
        if self._last_returned is None:
            raise IllegalStateError("No current element")
        return self._get_at(self._last_returned)

    def reset(self) -> None:
        self._check_modification()
        if self._snapshot is None:
            self._index = 0 if self._forward else self._collection.size() - 1
        else:
            self._index = 0 if self._forward else len(self._snapshot) - 1
        self._last_returned = None

    def move_prev(self) -> None:
        if self._forward:
            raise IllegalStateError("move_prev only valid for backward traversal")
        self._check_modification()
        self._index -= 1

    def remove_current(self) -> Any:
        if self._last_returned is None:
            raise IllegalStateError("Nothing to remove")
        if self._snapshot is not None:
            raise IllegalStateError("Cannot remove from a snapshot view")
        self._check_modification()
        removed = self._collection.remove_at(self._last_returned)
        self._expected_mod = self._collection._mod_count
        if self._forward:
            if self._last_returned < self._index:
                self._index -= 1
        else:
            if self._last_returned <= self._index:
                self._index += 1
        self._last_returned = None
        return removed

if __name__ == "__main__":
    c = CollectionContainer([1, 2, 3, 4, 5, 6])
    cursor = c.create_cursor(forward=True, predicate=lambda x: x % 2 == 0, live=True)
    collected = []
    while cursor.has_next():
        val = cursor.next_item()
        collected.append(val)
        if val == 4:
            cursor.remove_current()
    print("Collected (evens) before removal of 4:", collected)
    print("Collection after removal:", [c.get_at(i) for i in range(c.size())])

    back = c.create_cursor(forward=False, live=False)
    back_list = []
    while back.has_next():
        back_list.append(back.next_item())
    print("Backward snapshot traversal:", back_list)