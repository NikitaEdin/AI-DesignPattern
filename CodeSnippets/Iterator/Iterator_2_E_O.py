class Collection:
    def __init__(self, items):
        self._items = list(items)
    def create_cursor(self):
        return Cursor(self._items)

class Cursor:
    def __init__(self, items):
        self._items = items
        self._index = 0
    def has_more(self):
        return self._index < len(self._items)
    def get_next(self):
        if not self.has_more():
            raise IndexError("No more elements")
        item = self._items[self._index]
        self._index += 1
        return item

if __name__ == "__main__":
    col = Collection([1, 2, 3, 4])
    cur = col.create_cursor()
    while cur.has_more():
        print(cur.get_next())