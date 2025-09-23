from typing import Generic, TypeVar, Optional, Callable
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
    
    def add_transformer(self, func: Callable[[T], T]):
        self._transformers.append(func)
        return self
    
    def create_navigator(self):
        return SmartNavigator(self._items, self._filters, self._transformers)

class SmartNavigator(Navigator[T]):
    def __init__(self, items, filters, transformers):
        self._items = items
        self._filters = filters
        self._transformers = transformers
        self._position = 0
        self._direction = 1
    
    def has_next(self) -> bool:
        temp_pos = self._position
        while 0 <= temp_pos < len(self._items):
            item = self._items[temp_pos]
            if self._passes_filters(item):
                return True
            temp_pos += self._direction
        return False
    
    def next(self) -> T:
        while 0 <= self._position < len(self._items):
            item = self._items[self._position]
            self._position += self._direction
            
            if self._passes_filters(item):
                return self._apply_transformers(item)
        
        raise StopTraversal("No more elements")
    
    def reset(self):
        self._position = 0
        self._direction = 1
    
    def reverse(self):
        if self._direction == 1:
            self._position = len(self._items) - 1
            self._direction = -1
        else:
            self._position = 0
            self._direction = 1
    
    def _passes_filters(self, item: T) -> bool:
        return all(f(item) for f in self._filters)
    
    def _apply_transformers(self, item: T) -> T:
        result = item
        for transformer in self._transformers:
            result = transformer(result)
        return result

if __name__ == "__main__":
    collection = SmartCollection[int]()
    for i in range(1, 11):
        collection.add(i)
    
    collection.add_filter(lambda x: x % 2 == 0).add_transformer(lambda x: x * 2)
    
    navigator = collection.create_navigator()
    
    print("Forward traversal (even numbers doubled):")
    while navigator.has_next():
        try:
            print(navigator.next())
        except StopTraversal:
            break
    
    navigator.reverse()
    print("\nReverse traversal:")
    while navigator.has_next():
        try:
            print(navigator.next())
        except StopTraversal:
            break