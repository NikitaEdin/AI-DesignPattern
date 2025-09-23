from typing import Callable, Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")

class ItemCollection(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None):
        self._items: List[T] = list(items) if items is not None else []

    def add(self, item: T) -> None:
        self._items.append(item)

    def create_cursor(self, predicate: Optional[Callable[[T], bool]] = None, reverse: bool = False):
        if predicate is not None and not callable(predicate):
            raise TypeError("predicate must be callable or None")
        return Cursor(self._items, predicate, reverse)

class Cursor(Generic[T]):
    def __init__(self, items: List[T], predicate: Optional[Callable[[T], bool]] = None, reverse: bool = False):
        self._items = items
        self._predicate = predicate
        self._reverse = reverse
        self._index = len(items) - 1 if reverse else 0
        self._step = -1 if reverse else 1

    def has_next(self) -> bool:
        idx = self._index
        while 0 <= idx < len(self._items):
            item = self._items[idx]
            if self._predicate is None or self._predicate(item):
                return True
            idx += self._step
        return False

    def next_item(self) -> T:
        while 0 <= self._index < len(self._items):
            item = self._items[self._index]
            self._index += self._step
            if self._predicate is None or self._predicate(item):
                return item
        raise StopIteration("No more elements")

    def reset(self) -> None:
        self._index = len(self._items) - 1 if self._reverse else 0

if __name__ == "__main__":
    numbers = ItemCollection(range(1, 11))
    even_filter = lambda x: x % 2 == 0
    forward_cursor = numbers.create_cursor(predicate=even_filter)
    print("Forward even numbers:")
    try:
        while forward_cursor.has_next():
            print(forward_cursor.next_item(), end=" ")
    except StopIteration:
        pass
    print()

    reverse_cursor = numbers.create_cursor(predicate=lambda x: x > 5, reverse=True)
    print("Reverse numbers greater than 5:")
    try:
        while reverse_cursor.has_next():
            print(reverse_cursor.next_item(), end=" ")
    except StopIteration:
        pass
    print()