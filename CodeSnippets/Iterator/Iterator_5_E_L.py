class Aggregate:
    def __init__(self, items):
        self._items = items
        self._index = 0
        
    def create_iterator(self):
        return Iterator(self)
        
    def get_size(self):
        return len(self._items)
    
class Iterator:
    def __init__(self, aggregate):
        self._aggregate = aggregate
        self._index = 0
    
    def has_next(self):
        return self._index < self._aggregate.get_size()
    
    def next(self):
        item = self._aggregate._items[self._index]
        self._index += 1
        return item
    
if __name__ == "__main__":
    items = [1, 2, 3, 4, 5]
    aggregate = Aggregate(items)
    iterator = aggregate.create_iterator()
    
    while iterator.has_next():
        print(iterator.next())