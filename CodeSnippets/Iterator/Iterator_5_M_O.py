class ItemCollection:
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

    def create_cursor(self, reverse=False):
        return SequentialCursor(self, reverse)

    def __len__(self):
        return len(self._items)

    def _get_at(self, index):
        return self._items[index]


class SequentialCursor:
    def __init__(self, collection, reverse=False):
        if not isinstance(collection, ItemCollection):
            raise TypeError("Expected an ItemCollection")
        self._collection = collection
        self._reverse = bool(reverse)
        self._start = len(collection) - 1 if self._reverse else 0
        self._position = self._start
        self._captured_version = collection._version
        self._finished = len(collection) == 0

    def _check_modification(self):
        if self._captured_version != self._collection._version:
            raise RuntimeError("Collection modified during traversal")

    def has_more(self):
        self._check_modification()
        return not self._finished and 0 <= self._position < len(self._collection)

    def current(self):
        self._check_modification()
        if not self.has_more():
            raise IndexError("No current element")
        return self._collection._get_at(self._position)

    def advance(self):
        self._check_modification()
        if not self.has_more():
            raise StopIteration("No more elements to advance to")
        value = self._collection._get_at(self._position)
        self._position += -1 if self._reverse else 1
        if not (0 <= self._position < len(self._collection)):
            self._finished = True
        return value

    def reset(self):
        self._check_modification()
        self._position = self._start
        self._finished = len(self._collection) == 0


if __name__ == "__main__":
    coll = ItemCollection(["apple", "banana", "cherry"])
    cursor = coll.create_cursor()
    while cursor.has_more():
        print(cursor.advance())

    rev_cursor = coll.create_cursor(reverse=True)
    while rev_cursor.has_more():
        print(rev_cursor.advance())

    cursor2 = coll.create_cursor()
    print(cursor2.current())
    coll.add("date")
    try:
        cursor2.advance()
    except RuntimeError as e:
        print("Traversal error caught:", str(e))