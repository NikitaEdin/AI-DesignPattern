class SimpleCollection:
    def __init__(self, items):
        self._items = list(items)
    def create_cursor(self):
        return Cursor(self)

class Cursor:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
    def has_next(self):
        return self._index < len(self._collection._items)
    def next_item(self):
        if not self.has_next():
            raise IndexError("No more items")
        item = self._collection._items[self._index]
        self._index += 1
        return item

if __name__ == "__main__":
    col = SimpleCollection([1, 2, 3, 4])
    cur = col.create_cursor()
    while cur.has_next():
        print(cur.next_item())