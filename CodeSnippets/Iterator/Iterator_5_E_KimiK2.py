class Items:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def create_traverser(self):
        return _ItemsHelper(self._items)


class _ItemsHelper:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def has_next(self):
        return self._index < len(self._items)

    def next(self):
        item = self._items[self._index]
        self._index += 1
        return item


if __name__ == "__main__":
    c = Items()
    for i in "abc":
        c.add(i)
    t = c.create_traverser()
    while t.has_next():
        print(t.next())