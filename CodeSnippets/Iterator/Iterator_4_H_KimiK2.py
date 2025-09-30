from __future__ import annotations
import collections.abc as abc
from typing import Any, Optional, List


class _Node:
    __slots__ = ("_data", "_next")
    def __init__(self, data: Any, nxt: Optional[_Node] = None):
        self._data = data
        self._next = nxt


class Sequence:
    def __init__(self, items: Optional[List[Any]] = None):
        self._head: Optional[_Node] = None
        self._tail: Optional[_Node] = None
        self._size: int = 0
        if items:
            for v in items:
                self.append(v)

    def append(self, value: Any) -> None:
        node = _Node(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            self._tail._next = node  # type: ignore
            self._tail = node
        self._size += 1

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> "SequenceExplorer":
        return SequenceExplorer(self)


class SequenceExplorer:
    def __init__(self, container: Sequence):
        self._container = container
        self._current: Optional[_Node] = container._head

    def __iter__(self) -> "SequenceExplorer":
        return self

    def __next__(self) -> Any:
        if self._current is None:
            raise StopIteration
        value = self._current._data
        self._current = self._current._next
        return value

    def reset(self) -> None:
        self._current = self._container._head


if __name__ == "__main__":
    seq = Sequence([10, 20, 30])
    explorer = iter(seq)
    print("First pass:", list(explorer))
    explorer.reset()
    print("Second pass:", [v for v in explorer])