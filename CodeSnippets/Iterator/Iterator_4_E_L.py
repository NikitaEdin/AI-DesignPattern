class Container:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def has_next(self):
        return self._index < len(self._items)

    def next(self):
        item = self._items[self._index]
        self._index += 1
        return item

class MyIterator:
    def __init__(self, container):
        self._container = container

    def has_next(self):
        return self._container.has_next()

    def next(self):
        return self._container.next()

def main():
    items = [1, 2, 3, 4, 5]
    container = Container(items)
    iterator = MyIterator(container)

    while iterator.has_next():
        print(iterator.next())