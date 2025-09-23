class NumberCursor:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
    def has_next(self):
        return self._index < len(self._collection._items)
    def next_item(self):
        if not self.has_next():
            raise StopIteration
        item = self._collection._items[self._index]
        self._index += 1
        return item

class NumberCollection:
    def __init__(self, items):
        self._items = list(items)
    def create_cursor(self):
        return NumberCursor(self)

if __name__ == "__main__":
    collection = NumberCollection([1, 2, 3, 4])
    cursor = collection.create_cursor()
    while cursor.has_next():
        print(cursor.next_item())