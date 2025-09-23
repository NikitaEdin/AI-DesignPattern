class ItemCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []

    def create_cursor(self, start=0, step=1, reverse=False, filter_func=None):
        return Cursor(self, start=start, step=step, reverse=reverse, filter_func=filter_func)

    def add(self, item):
        self._items.append(item)

    def remove_at(self, index):
        if not 0 <= index < len(self._items):
            raise IndexError("Index out of range")
        return self._items.pop(index)

    def get_at(self, index):
        if not 0 <= index < len(self._items):
            raise IndexError("Index out of range")
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"ItemCollection({self._items})"


class Cursor:
    def __init__(self, collection, start=0, step=1, reverse=False, filter_func=None):
        if step < 1:
            raise ValueError("step must be >= 1")
        if len(collection) == 0 and start != 0:
            raise ValueError("start must be 0 for empty collection")
        self._collection = collection
        self._step = step
        self._reverse = bool(reverse)
        self._filter = filter_func
        self._start = start
        self._indices = self._build_index_list()
        self._position = 0

    def _build_index_list(self):
        n = len(self._collection)
        if n == 0:
            return []
        seq = list(range(n))
        if self._reverse:
            seq = list(reversed(seq))
        if not 0 <= self._start < n:
            raise IndexError("start index out of range")
        seq = seq[self._start::self._step]
        if self._filter:
            seq = [i for i in seq if self._filter(self._collection.get_at(i))]
        return seq

    def has_more(self):
        return self._position < len(self._indices)

    def next_item(self):
        if not self.has_more():
            raise StopIteration("No more elements")
        idx = self._indices[self._position]
        self._position += 1
        return self._collection.get_at(idx)

    def reset(self):
        self._indices = self._build_index_list()
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_item()


if __name__ == "__main__":
    data = ItemCollection(["apple", "banana", "cherry", "date", "elderberry", "fig"])
    cursor = data.create_cursor(start=1, step=2, reverse=False, filter_func=lambda x: len(x) > 4)
    while cursor.has_more():
        print(cursor.next_item())
    cursor.reset()
    for item in cursor:
        print("again:", item)