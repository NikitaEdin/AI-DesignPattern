class DataCollection:
    def __init__(self):
        self._items = []
    def add(self, item):
        self._items.append(item)
    def create_looker(self):
        return Looker(self._items)

class Looker:
    def __init__(self, items):
        self._items = items
        self._pos = 0
    def ahead(self):
        return self._pos < len(self._items)
    def next(self):
        item = self._items[self._pos]
        self._pos += 1
        return item

if __name__ == "__main__":
    col = DataCollection()
    col.add("A")
    col.add("B")
    col.add("C")
    look = col.create_looker()
    while look.ahead():
        print(look.next())