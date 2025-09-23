from typing import Any, Optional, Callable
from collections.abc import Sequence

class CustomSequence:
    def __init__(self, data: Sequence[Any]):
        self._data = list(data)
        self._version = 0
    
    def add(self, item: Any) -> None:
        self._data.append(item)
        self._version += 1
    
    def remove(self, item: Any) -> None:
        if item in self._data:
            self._data.remove(item)
            self._version += 1
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __getitem__(self, index: int) -> Any:
        return self._data[index]
    
    def create_traverser(self, reverse: bool = False, 
                        filter_func: Optional[Callable[[Any], bool]] = None) -> 'DataTraverser':
        return DataTraverser(self, reverse, filter_func)

class DataTraverser:
    def __init__(self, sequence: CustomSequence, reverse: bool = False,
                 filter_func: Optional[Callable[[Any], bool]] = None):
        self._sequence = sequence
        self._reverse = reverse
        self._filter_func = filter_func
        self._initial_version = sequence._version
        self._current_index = len(sequence) - 1 if reverse else 0
        self._visited_count = 0
        self._cache = []
        self._build_cache()
    
    def _build_cache(self) -> None:
        for item in self._sequence._data:
            if self._filter_func is None or self._filter_func(item):
                self._cache.append(item)
        if self._reverse:
            self._cache.reverse()
    
    def _check_concurrent_modification(self) -> None:
        if self._sequence._version != self._initial_version:
            raise RuntimeError("Collection was modified during traversal")
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Any:
        self._check_concurrent_modification()
        
        if self._visited_count >= len(self._cache):
            raise StopIteration
        
        item = self._cache[self._visited_count]
        self._visited_count += 1
        return item
    
    def peek(self) -> Optional[Any]:
        self._check_concurrent_modification()
        if self._visited_count < len(self._cache):
            return self._cache[self._visited_count]
        return None
    
    def has_next(self) -> bool:
        self._check_concurrent_modification()
        return self._visited_count < len(self._cache)
    
    def reset(self) -> None:
        self._visited_count = 0
        self._initial_version = self._sequence._version
        self._cache.clear()
        self._build_cache()

if __name__ == "__main__":
    numbers = CustomSequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print("Forward traversal:")
    forward_traverser = numbers.create_traverser()
    for num in forward_traverser:
        print(num, end=" ")
    print()
    
    print("\nReverse traversal:")
    reverse_traverser = numbers.create_traverser(reverse=True)
    for num in reverse_traverser:
        print(num, end=" ")
    print()
    
    print("\nFiltered traversal (even numbers only):")
    filtered_traverser = numbers.create_traverser(filter_func=lambda x: x % 2 == 0)
    for num in filtered_traverser:
        print(num, end=" ")
    print()
    
    print("\nManual traversal with peek and has_next:")
    manual_traverser = numbers.create_traverser()
    while manual_traverser.has_next():
        current = next(manual_traverser)
        next_item = manual_traverser.peek()
        print(f"Current: {current}, Next: {next_item}")
    
    print("\nConcurrent modification test:")
    traverser = numbers.create_traverser()
    try:
        first = next(traverser)
        print(f"First item: {first}")
        numbers.add(11)
        second = next(traverser)
    except RuntimeError as e:
        print(f"Error caught: {e}")