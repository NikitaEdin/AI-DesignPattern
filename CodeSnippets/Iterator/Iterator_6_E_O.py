class Collection:
    def __init__(self, items):
        self._items = list(items)
    def create_cursor(self):
        return Cursor(self)

class Cursor:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
    def has_more(self):
        return self._index < len(self._collection._items)
    def next_item(self):
        if not self.has_more():
            raise StopIteration
        item = self._collection._items[self._index]
        self._index += 1
        return item

if __name__ == "__main__":
    coll = Collection(["apple", "banana", "cherry"])
    cur = coll.create_cursor()
    while cur.has_more():
        print(cur.next_item())