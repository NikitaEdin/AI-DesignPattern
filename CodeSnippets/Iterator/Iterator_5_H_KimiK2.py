from __future__ import annotations
import threading
from typing import TypeVar, Generic, Protocol, runtime_checkable, Any, Callable, Iterator, List, Optional
from collections.abc import Iterable
import weakref

T = TypeVar('T')
U = TypeVar('U')

@runtime_checkable
class Cursor(Protocol[T]):
    def __iter__(self) -> Cursor[T]: ...
    def __next__(self) -> T: ...
    def clone(self) -> Cursor[T]: ...

class FailFastMixin:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._mod_count = 0
        self._src_ref: Optional[Any] = None
    
    def _register_src(self, src: Any) -> None:
        self._src_ref = weakref.ref(src) if src else None
    
    def _check_mod(self) -> None:
        if self._src_ref and self._src_ref() is None:
            raise RuntimeError("Source collection was destroyed")
        with self._lock:
            if hasattr(self, '_expected_mod') and self._expected_mod != self._mod_count:
                raise RuntimeError("Concurrent modification detected")

class CustomSequenceCursor(FailFastMixin, Generic[T]):
    def __init__(self, data: List[T], start: int = 0) -> None:
        super().__init__()
        self._storage = data
        self._idx = start
        self._expected_mod = self._mod_count
        self._register_src(data)
    
    def __iter__(self) -> CustomSequenceCursor[T]:
        return self
    
    def __next__(self) -> T:
        self._check_mod()
        with self._lock:
            if self._idx >= len(self._storage):
                raise StopIteration
            val = self._storage[self._idx]
            self._idx += 1
            return val
    
    def clone(self) -> CustomSequenceCursor[T]:
        with self._lock:
            twin = CustomSequenceCursor(self._storage, self._idx)
            twin._expected_mod = self._mod_count
            return twin

class CustomSequenceCursorReverse(FailFastMixin, Generic[T]):
    def __init__(self, data: List[T]) -> None:
        super().__init__()
        self._storage = data
        self._idx = len(data) - 1
        self._expected_mod = self._mod_count
        self._register_src(data)
        if self._idx < 0:
            self._idx = -1
    
    def __iter__(self) -> CustomSequenceCursorReverse[T]:
        return self
    
    def __next__(self) -> T:
        self._check_mod()
        with self._lock:
            if self._idx < 0:
                raise StopIteration
            val = self._storage[self._idx]
            self._idx -= 1
            return val
    
    def clone(self) -> CustomSequenceCursorReverse[T]:
        with self._lock:
            twin = CustomSequenceCursorReverse(self._storage)
            twin._idx = self._idx
            twin._expected_mod = self._mod_count
            return twin

class CustomSequenceCursorSkip(FailFastMixin, Generic[T]):
    def __init__(self, data: List[T], step: int) -> None:
        super().__init__()
        if step <= 0:
            raise ValueError("Step must be positive")
        self._storage = data
        self._step = step
        self._idx = 0
        self._expected_mod = self._mod_count
        self._register_src(data)
    
    def __iter__(self) -> CustomSequenceCursorSkip[T]:
        return self
    
    def __next__(self) -> T:
        self._check_mod()
        with self._lock:
            if self._idx >= len(self._storage):
                raise StopIteration
            val = self._storage[self._idx]
            self._idx += self._step
            return val
    
    def clone(self) -> CustomSequenceCursorSkip[T]:
        with self._lock:
            twin = CustomSequenceCursorSkip(self._storage, self._step)
            twin._idx = self._idx
            twin._expected_mod = self._mod_count
            return twin

class CustomSequence(Generic[T]):
    def __init__(self, items: Iterable[T] = ()) -> None:
        self._data: List[T] = list(items)
        self._mod_lock = threading.RLock()
        self._mod_count = 0
    
    def _bump_mod(self) -> None:
        with self._mod_lock:
            self._mod_count += 1
    
    def add(self, item: T) -> None:
        with self._mod_lock:
            self._data.append(item)
            self._bump_mod()
    
    def create_forward_cursor(self) -> CustomSequenceCursor[T]:
        return CustomSequenceCursor(self._data)
    
    def create_reverse_cursor(self) -> CustomSequenceCursorReverse[T]:
        return CustomSequenceCursorReverse(self._data)
    
    def create_skip_cursor(self, step: int) -> CustomSequenceCursorSkip[T]:
        return CustomSequenceCursorSkip(self._data, step)

if __name__ == "__main__":
    seq = CustomSequence([10, 20, 30, 40, 50])
    c1 = seq.create_forward_cursor()
    for val in c1:
        print(val)
    c2 = seq.create_reverse_cursor()
    for val in c2:
        print(val)
    c3 = seq.create_skip_cursor(2)
    for val in c3:
        print(val)