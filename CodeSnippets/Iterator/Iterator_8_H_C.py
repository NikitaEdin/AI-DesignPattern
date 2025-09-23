class DataCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []
        self._capacity = None
    
    def add(self, item):
        if self._capacity and len(self._items) >= self._capacity:
            raise OverflowError("Collection at maximum capacity")
        self._items.append(item)
    
    def set_capacity(self, capacity):
        self._capacity = capacity
    
    def __iter__(self):
        return CollectionTraverser(self._items)
    
    def reverse_traverser(self):
        return ReverseTraverser(self._items)
    
    def filtered_traverser(self, predicate):
        return FilteredTraverser(self._items, predicate)

class CollectionTraverser:
    def __init__(self, items):
        self._items = items
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item
    
    def reset(self):
        self._index = 0
    
    def has_next(self):
        return self._index < len(self._items)
    
    def peek(self):
        if not self.has_next():
            raise StopIteration("No more items")
        return self._items[self._index]

class ReverseTraverser:
    def __init__(self, items):
        self._items = items
        self._index = len(items) - 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < 0:
            raise StopIteration
        item = self._items[self._index]
        self._index -= 1
        return item

class FilteredTraverser:
    def __init__(self, items, predicate):
        self._items = items
        self._predicate = predicate
        self._index = 0
        self._find_next_valid()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        self._find_next_valid()
        return item
    
    def _find_next_valid(self):
        while self._index < len(self._items) and not self._predicate(self._items[self._index]):
            self._index += 1

if __name__ == "__main__":
    collection = DataCollection([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print("Forward traversal:")
    traverser = iter(collection)
    print(f"Peek: {traverser.peek()}")
    for item in traverser:
        print(item, end=" ")
    print()
    
    print("\nReverse traversal:")
    for item in collection.reverse_traverser():
        print(item, end=" ")
    print()
    
    print("\nFiltered traversal (even numbers):")
    for item in collection.filtered_traverser(lambda x: x % 2 == 0):
        print(item, end=" ")
    print()
    
    print("\nManual traversal with has_next:")
    manual = iter(collection)
    count = 0
    while manual.has_next() and count < 3:
        print(f"Item: {next(manual)}")
        count += 1