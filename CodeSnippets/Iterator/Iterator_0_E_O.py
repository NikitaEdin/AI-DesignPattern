class SimpleCollection:
    def __init__(self, items):
        self._items = list(items)
    def create_walker(self):
        return SimpleWalker(self._items)

class SimpleWalker:
    def __init__(self, items):
        self._items = items
        self._index = 0
    def has_more(self):
        return self._index < len(self._items)
    def next_item(self):
        if not self.has_more():
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item

if __name__ == "__main__":
    collection = SimpleCollection(["a", "b", "c"])
    walker = collection.create_walker()
    while walker.has_more():
        print(walker.next_item())