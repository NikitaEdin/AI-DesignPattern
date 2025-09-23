class ItemCollection:
    def __init__(self, items=None):
        self._items = list(items) if items is not None else []

    def add(self, item):
        self._items.append(item)

    def create_cursor(self, reverse=False, predicate=None):
        if predicate is not None and not callable(predicate):
            raise TypeError("predicate must be callable or None")
        return Cursor(self._items, reverse=reverse, predicate=predicate)

    def __len__(self):
        return len(self._items)


class Cursor:
    def __init__(self, items, reverse=False, predicate=None):
        if not isinstance(items, list):
            raise TypeError("items must be a list")
        self._items = items
        self._predicate = predicate
        self._reverse = bool(reverse)
        self.reset()

    def reset(self):
        self._index = len(self._items) - 1 if self._reverse else 0

    def __iter__(self):
        return self

    def __next__(self):
        next_idx = self._find_next_index(self._index)
        if next_idx is None:
            raise StopIteration
        result = self._items[next_idx]
        self._advance_from(next_idx)
        return result

    def peek(self):
        next_idx = self._find_next_index(self._index)
        if next_idx is None:
            raise StopIteration("No next element to peek")
        return self._items[next_idx]

    def _find_next_index(self, start):
        step = -1 if self._reverse else 1
        idx = start
        while 0 <= idx < len(self._items):
            candidate = self._items[idx]
            if self._predicate is None or self._predicate(candidate):
                return idx
            idx += step
        return None

    def _advance_from(self, current):
        self._index = current + (-1 if self._reverse else 1)


if __name__ == "__main__":
    collection = ItemCollection([1, 2, 3, 4, 5, 6])
    collection.add(7)

    even_cursor = collection.create_cursor(predicate=lambda x: x % 2 == 0)
    try:
        print("Next even (peek):", even_cursor.peek())
    except StopIteration:
        print("No items available to peek")

    print("Evens using cursor:")
    for value in even_cursor:
        print(value)

    print("Reverse odds:")
    reverse_odd_cursor = collection.create_cursor(reverse=True, predicate=lambda x: x % 2 == 1)
    for value in reverse_odd_cursor:
        print(value)