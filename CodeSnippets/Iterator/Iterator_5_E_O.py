class Collection:
    def __init__(self, items):
        self._items = list(items)
    def __iter__(self):
        return Cursor(self._items)

class Cursor:
    def __init__(self, items):
        self._items = items
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        value = self._items[self._index]
        self._index += 1
        return value

if __name__ == "__main__":
    coll = Collection(range(5))
    for item in coll:
        print(item)