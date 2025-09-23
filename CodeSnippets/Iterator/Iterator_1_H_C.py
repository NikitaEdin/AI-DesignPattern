from typing import TypeVar, Generic, Optional, Callable, Any
from collections.abc import Sequence

T = TypeVar('T')

class Traverser(Generic[T]):
    def __init__(self, collection: Sequence[T], reverse: bool = False, 
                 filter_func: Optional[Callable[[T], bool]] = None,
                 transform_func: Optional[Callable[[T], Any]] = None):
        self._collection = collection
        self._reverse = reverse
        self._filter_func = filter_func
        self._transform_func = transform_func
        self._current = len(collection) - 1 if reverse else 0
        self._visited_count = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        while self._has_more():
            item = self._get_current_item()
            self._advance()
            
            if self._filter_func and not self._filter_func(item):
                continue
                
            self._visited_count += 1
            return self._transform_func(item) if self._transform_func else item
            
        raise StopIteration
        
    def _has_more(self) -> bool:
        if self._reverse:
            return self._current >= 0
        return self._current < len(self._collection)
        
    def _get_current_item(self) -> T:
        return self._collection[self._current]
        
    def _advance(self) -> None:
        if self._reverse:
            self._current -= 1
        else:
            self._current += 1
            
    def reset(self) -> None:
        self._current = len(self._collection) - 1 if self._reverse else 0
        self._visited_count = 0
        
    def get_visited_count(self) -> int:
        return self._visited_count

class DataContainer(Generic[T]):
    def __init__(self):
        self._items: list[T] = []
        
    def add(self, item: T) -> None:
        self._items.append(item)
        
    def remove(self, item: T) -> bool:
        try:
            self._items.remove(item)
            return True
        except ValueError:
            return False
            
    def size(self) -> int:
        return len(self._items)
        
    def create_traverser(self, reverse: bool = False, 
                        filter_func: Optional[Callable[[T], bool]] = None,
                        transform_func: Optional[Callable[[T], Any]] = None) -> Traverser[T]:
        return Traverser(self._items, reverse, filter_func, transform_func)

if __name__ == "__main__":
    container = DataContainer[str]()
    
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words:
        container.add(word)
    
    print("Forward traversal:")
    forward_traverser = container.create_traverser()
    for item in forward_traverser:
        print(f"  {item}")
    print(f"Visited: {forward_traverser.get_visited_count()}")
    
    print("\nReverse traversal with filter (length > 5):")
    reverse_traverser = container.create_traverser(
        reverse=True, 
        filter_func=lambda x: len(x) > 5
    )
    for item in reverse_traverser:
        print(f"  {item}")
    
    print("\nTransformed traversal (uppercase):")
    transform_traverser = container.create_traverser(
        transform_func=lambda x: x.upper()
    )
    for item in transform_traverser:
        print(f"  {item}")
    
    print("\nReusing traverser after reset:")
    transform_traverser.reset()
    first_three = []
    for i, item in enumerate(transform_traverser):
        if i >= 3:
            break
        first_three.append(item)
    print(f"  {first_three}")