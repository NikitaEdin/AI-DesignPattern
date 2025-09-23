class Container:
    def __init__(self, items):
        self._items = items
        self._index = 0
    
    def has_next(self):
        return self._index < len(self._items)
    
    def next(self):
        if not self.has_next():
            raise StopIteration()
        item = self._items[self._index]
        self._index += 1
        return item
    
    def __iter__(self):
        return self

class IteratorExample:
    def __init__(self, container):
        self._container = container
    
    def iterate(self):
        for item in self._container:
            print(item)
            
if __name__ == '__main__':
    container = Container(['a', 'b', 'c'])
    iterator = IteratorExample(container)
    iterator.iterate()