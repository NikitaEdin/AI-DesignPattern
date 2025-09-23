class SimpleCollection:
    def __init__(self, items):
        self._items = list(items)
    def create_traverser(self):
        return SimpleTraverser(self)

class SimpleTraverser:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
    def current(self):
        if 0 <= self._index < len(self._collection._items):
            return self._collection._items[self._index]
        raise StopIteration
    def advance(self):
        self._index += 1
    def at_end(self):
        return self._index >= len(self._collection._items)

if __name__ == "__main__":
    col = SimpleCollection(["a", "b", "c"])
    traversal = col.create_traverser()
    while not traversal.at_end():
        print(traversal.current())
        traversal.advance()