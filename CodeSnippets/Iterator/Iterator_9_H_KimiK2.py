from __future__ import annotations
from typing import Any, Optional
import random

class Node:
    def __init__(self, value: Any):
        self.value = value
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None

class LinkedCollection:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size = 0

    def append(self, value: Any) -> None:
        new = Node(value)
        if not self.head:
            self.head = self.tail = new
        else:
            self.tail.next = new
            new.prev = self.tail
            self.tail = new
        self._size += 1

    def __iter__(self):
        return self._ForwardTraversal(self.head)

    def reverse(self):
        return self._ReverseTraversal(self.tail)

    def random_order(self):
        return self._ShuffledTraversal(self)

    class _ForwardTraversal:
        def __init__(self, start: Optional[Node]):
            self.current = start

        def __iter__(self):
            return self

        def __next__(self):
            if not self.current:
                raise StopIteration
            value = self.current.value
            self.current = self.current.next
            return value

    class _ReverseTraversal:
        def __init__(self, start: Optional[Node]):
            self.current = start

        def __iter__(self):
            return self

        def __next__(self):
            if not self.current:
                raise StopIteration
            value = self.current.value
            self.current = self.current.prev
            return value

    class _ShuffledTraversal:
        def __init__(self, collection: 'LinkedCollection'):
            self.items = []
            node = collection.head
            while node:
                self.items.append(node.value)
                node = node.next
            random.shuffle(self.items)
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.items):
                raise StopIteration
            value = self.items[self.index]
            self.index += 1
            return value

if __name__ == "__main__":
    data = LinkedCollection()
    for num in [10, 20, 30, 40, 50]:
        data.append(num)
    
    print("Forward:", list(data))
    print("Reverse:", list(data.reverse()))
    print("Shuffled:", list(data.random_order()))