from typing import TypeVar, Generic, Optional, Callable, Any
from collections.abc import Iterable

T = TypeVar('T')

class Traverser(Generic[T]):
    def __init__(self, collection: 'TraversableCollection[T]'):
        self._collection = collection
        self._position = 0
        self._reverse = False
        self._filter_func: Optional[Callable[[T], bool]] = None
        self._transform_func: Optional[Callable[[T], Any]] = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._reverse:
            return self._next_reverse()
        return self._next_forward()

    def _next_forward(self):
        while self._position < len(self._collection):
            item = self._collection._items[self._position]
            self._position += 1
            
            if self._filter_func and not self._filter_func(item):
                continue
                
            return self._transform_func(item) if self._transform_func else item
        raise StopIteration

    def _next_reverse(self):
        if self._position == 0:
            self._position = len(self._collection)
            
        while self._position > 0:
            self._position -= 1
            item = self._collection._items[self._position]
            
            if self._filter_func and not self._filter_func(item):
                continue
                
            return self._transform_func(item) if self._transform_func else item
        raise StopIteration

    def reset(self):
        self._position = 0
        return self

    def reverse(self):
        self._reverse = not self._reverse
        self._position = 0
        return self

    def filter(self, predicate: Callable[[T], bool]):
        self._filter_func = predicate
        self._position = 0
        return self

    def transform(self, func: Callable[[T], Any]):
        self._transform_func = func
        return self

class TraversableCollection(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None):
        self._items = list(items) if items else []

    def create_traverser(self) -> Traverser[T]:
        return Traverser(self)

    def add(self, item: T):
        self._items.append(item)

    def remove(self, item: T) -> bool:
        try:
            self._items.remove(item)
            return True
        except ValueError:
            return False

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

class NumberSequence(TraversableCollection[int]):
    def __init__(self, start: int = 0, end: int = 10):
        super().__init__(range(start, end))

    def evens_only(self) -> Traverser[int]:
        return self.create_traverser().filter(lambda x: x % 2 == 0)

    def squares(self) -> Traverser[int]:
        return self.create_traverser().transform(lambda x: x * x)

if __name__ == "__main__":
    collection = TraversableCollection([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print("Forward traversal:")
    for item in collection.create_traverser():
        print(item, end=" ")
    
    print("\nReverse traversal:")
    for item in collection.create_traverser().reverse():
        print(item, end=" ")
    
    print("\nFiltered (even numbers):")
    for item in collection.create_traverser().filter(lambda x: x % 2 == 0):
        print(item, end=" ")
    
    print("\nTransformed (squares) and filtered (> 25):")
    for item in collection.create_traverser().transform(lambda x: x * x).filter(lambda x: x > 25):
        print(item, end=" ")
    
    print("\nNumber sequence with method chaining:")
    seq = NumberSequence(1, 11)
    for square in seq.evens_only().transform(lambda x: x * x):
        print(square, end=" ")
    
    print("\nReusing traverser:")
    traverser = collection.create_traverser().filter(lambda x: x > 5)
    print("\nFirst pass:")
    for item in traverser:
        print(item, end=" ")
    
    print("\nSecond pass (reset):")
    for item in traverser.reset():
        print(item, end=" ")