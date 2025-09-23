class SimpleCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []
    def add(self, item): self._items.append(item)
    def create_cursor(self): return SimpleCursor(self)
class SimpleCursor:
    def __init__(self, collection):
        self._collection = collection; self._index = 0
    def has_more(self): return self._index < len(self._collection._items)
    def get_next(self):
        if not self.has_more(): raise StopIteration
        item = self._collection._items[self._index]; self._index += 1
        return item
if __name__ == "__main__":
    coll = SimpleCollection([1, 2, 3])
    coll.add(4)
    cur = coll.create_cursor()
    while cur.has_more():
        print(cur.get_next())