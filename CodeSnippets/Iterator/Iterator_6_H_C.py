from typing import TypeVar, Generic, Optional, Callable, Any
from abc import ABC, abstractmethod

T = TypeVar('T')

class Traversable(ABC, Generic[T]):
    @abstractmethod
    def create_navigator(self):
        pass

class Navigator(ABC, Generic[T]):
    @abstractmethod
    def has_next(self) -> bool:
        pass
    
    @abstractmethod
    def next(self) -> T:
        pass
    
    @abstractmethod
    def reset(self):
        pass

class StopTraversal(Exception):
    pass

class SmartCollection(Traversable[T]):
    def __init__(self):
        self._items = []
        self._filters = []
        self._transformers = []
    
    def add(self, item: T):
        self._items.append(item)
    
    def add_filter(self, predicate: Callable[[T], bool]):
        self._filters.append(predicate)
        return self
    
    def add_transformer(self, transform: Callable[[T], Any]):
        self._transformers.append(transform)
        return self
    
    def create_navigator(self):
        return SmartNavigator(self._items, self._filters, self._transformers)
    
    def __iter__(self):
        return self.create_navigator()

class SmartNavigator(Navigator[T]):
    def __init__(self, items, filters, transformers):
        self._items = items
        self._filters = filters
        self._transformers = transformers
        self._position = 0
        self._processed_items = None
        self._prepare_items()
    
    def _prepare_items(self):
        self._processed_items = self._items.copy()
        
        for filter_func in self._filters:
            self._processed_items = [item for item in self._processed_items if filter_func(item)]
        
        for transform_func in self._transformers:
            self._processed_items = [transform_func(item) for item in self._processed_items]
    
    def has_next(self) -> bool:
        return self._position < len(self._processed_items)
    
    def next(self) -> T:
        if not self.has_next():
            raise StopTraversal("No more elements")
        
        item = self._processed_items[self._position]
        self._position += 1
        return item
    
    def reset(self):
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            return self.next()
        except StopTraversal:
            raise StopIteration

class ReverseNavigator(Navigator[T]):
    def __init__(self, items):
        self._items = items
        self._position = len(items) - 1
    
    def has_next(self) -> bool:
        return self._position >= 0
    
    def next(self) -> T:
        if not self.has_next():
            raise StopTraversal("No more elements")
        
        item = self._items[self._position]
        self._position -= 1
        return item
    
    def reset(self):
        self._position = len(self._items) - 1

class ReverseCollection(Traversable[T]):
    def __init__(self, items):
        self._items = items
    
    def create_navigator(self):
        return ReverseNavigator(self._items)

if __name__ == "__main__":
    collection = SmartCollection()
    for i in range(1, 11):
        collection.add(i)
    
    collection.add_filter(lambda x: x % 2 == 0).add_transformer(lambda x: x * x)
    
    print("Filtered and transformed (even numbers squared):")
    for item in collection:
        print(item, end=" ")
    print()
    
    navigator = collection.create_navigator()
    navigator.reset()
    print("Manual navigation:")
    while navigator.has_next():
        print(navigator.next(), end=" ")
    print()
    
    reverse_collection = ReverseCollection([1, 2, 3, 4, 5])
    reverse_nav = reverse_collection.create_navigator()
    print("Reverse traversal:")
    while reverse_nav.has_next():
        print(reverse_nav.next(), end=" ")
    print()