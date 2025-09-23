class MessageCollection:
    def __init__(self, items=None):
        self._items = list(items) if items is not None else []

    def add(self, item):
        if item is None:
            raise ValueError("Cannot add None as an item")
        self._items.append(item)

    def create_cursor(self, start=0, step=1, filter_func=None):
        return Cursor(self, start=start, step=step, filter_func=filter_func)

    def __len__(self):
        return len(self._items)

    def _get(self, index):
        return self._items[index]


class Cursor:
    def __init__(self, collection, start=0, step=1, filter_func=None):
        if collection is None:
            raise TypeError("collection must be provided")
        if step <= 0:
            raise ValueError("step must be a positive integer")
        self._collection = collection
        self._start = int(start)
        self._step = int(step)
        self._filter = filter_func
        self.reset()

    def reset(self):
        self._index = self._start
        self._exhausted = False
        self._advance_to_next_valid()

    def _advance_to_next_valid(self):
        n = len(self._collection)
        while 0 <= self._index < n:
            candidate = self._collection._get(self._index)
            if self._filter is None or self._filter(candidate):
                return
            self._index += self._step
        self._exhausted = True

    def has_more(self):
        return not self._exhausted

    def get_next(self):
        if self._exhausted:
            raise StopIteration("No more elements")
        value = self._collection._get(self._index)
        self._index += self._step
        self._advance_to_next_valid()
        return value

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_next()


if __name__ == "__main__":
    messages = MessageCollection(["hi", "hello", "world", "!", "python", "ok", "design"])
    messages.add("pattern")
    # cursor that skips every other item and only yields messages longer than 2 characters
    cursor = messages.create_cursor(start=0, step=2, filter_func=lambda s: len(s) > 2)
    try:
        while cursor.has_more():
            print(cursor.get_next())
    except StopIteration:
        pass

    print("--- using for-loop ---")
    cursor.reset()
    for msg in cursor:
        print(msg)