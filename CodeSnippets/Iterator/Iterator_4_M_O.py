class NumberCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []
        self._version = 0

    def add(self, item):
        self._items.append(item)
        self._version += 1

    def remove(self, item):
        try:
            self._items.remove(item)
            self._version += 1
        except ValueError:
            raise ValueError("Item not found in collection")

    def size(self):
        return len(self._items)

    def create_cursor(self, filter_fn=None, reverse=False):
        if filter_fn is not None and not callable(filter_fn):
            raise TypeError("filter_fn must be callable or None")
        return Cursor(self, filter_fn, reverse)


class Cursor:
    def __init__(self, collection, filter_fn=None, reverse=False):
        self._collection = collection
        self._filter = filter_fn
        self._reverse = bool(reverse)
        self._expected_version = collection._version
        self._index = len(collection._items) - 1 if self._reverse else 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._expected_version != self._collection._version:
            raise RuntimeError("Collection modified during traversal")
        items = self._collection._items
        size = len(items)
        while 0 <= self._index < size:
            current = items[self._index]
            self._index += -1 if self._reverse else 1
            if self._filter is None or self._filter(current):
                return current
        raise StopIteration


if __name__ == "__main__":
    col = NumberCollection(range(1, 11))
    even_filter = lambda x: x % 2 == 0

    print("Even numbers:")
    for value in col.create_cursor(filter_fn=even_filter):
        print(value, end=" ")
    print("\n")

    print("Values > 5 in reverse:")
    for value in col.create_cursor(filter_fn=lambda x: x > 5, reverse=True):
        print(value, end=" ")
    print("\n")

    print("Modification detection demo:")
    cur = col.create_cursor()
    print(next(cur))
    col.add(99)
    try:
        print(next(cur))
    except RuntimeError as e:
        print("Detected modification:", e)