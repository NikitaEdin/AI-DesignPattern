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

class SmartCollection(Traversable[T]):
    def __init__(self, items: list[T]):
        self._items = items[:]
        self._filters: list[Callable[[T], bool]] = []
        self._transformers: list[Callable[[T], T]] = []
    
    def add_filter(self, predicate: Callable[[T], bool]):
        self._filters.append(predicate)
        return self
    
    def add_transform(self, transformer: Callable[[T], T]):
        self._transformers.append(transformer)
        return self
    
    def create_navigator(self):
        return SmartNavigator(self._items, self._filters, self._transformers)

class SmartNavigator(Navigator[T]):
    def __init__(self, items: list[T], filters: list[Callable], transformers: list[Callable]):
        self._original_items = items
        self._filters = filters
        self._transformers = transformers
        self._current_index = 0
        self._processed_items = self._process_items()
    
    def _process_items(self) -> list[T]:
        result = self._original_items[:]
        
        for filter_func in self._filters:
            result = [item for item in result if filter_func(item)]
        
        for transform_func in self._transformers:
            result = [transform_func(item) for item in result]
        
        return result
    
    def has_next(self) -> bool:
        return self._current_index < len(self._processed_items)
    
    def next(self) -> T:
        if not self.has_next():
            raise StopIteration("No more elements")
        
        item = self._processed_items[self._current_index]
        self._current_index += 1
        return item
    
    def reset(self):
        self._current_index = 0
        self._processed_items = self._process_items()
    
    def peek(self) -> Optional[T]:
        if self.has_next():
            return self._processed_items[self._current_index]
        return None
    
    def skip(self, count: int):
        self._current_index = min(self._current_index + count, len(self._processed_items))

class BatchNavigator(Navigator[list[T]]):
    def __init__(self, source_navigator: Navigator[T], batch_size: int):
        self._source = source_navigator
        self._batch_size = max(1, batch_size)
    
    def has_next(self) -> bool:
        return self._source.has_next()
    
    def next(self) -> list[T]:
        if not self.has_next():
            raise StopIteration("No more batches")
        
        batch = []
        for _ in range(self._batch_size):
            if self._source.has_next():
                batch.append(self._source.next())
            else:
                break
        
        return batch
    
    def reset(self):
        self._source.reset()

if __name__ == "__main__":
    numbers = SmartCollection([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    filtered_collection = (numbers
                          .add_filter(lambda x: x % 2 == 0)
                          .add_transform(lambda x: x * x))
    
    nav = filtered_collection.create_navigator()
    
    print("Filtered and squared even numbers:")
    while nav.has_next():
        print(nav.next())
    
    nav.reset()
    nav.skip(2)
    print(f"After reset and skip(2), next item: {nav.next()}")
    
    words = SmartCollection(["apple", "banana", "cherry", "date", "elderberry"])
    word_nav = words.add_filter(lambda x: len(x) > 5).create_navigator()
    
    batch_nav = BatchNavigator(word_nav, 2)
    print("Words longer than 5 chars in batches of 2:")
    while batch_nav.has_next():
        print(batch_nav.next())