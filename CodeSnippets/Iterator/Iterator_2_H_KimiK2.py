from __future__ import annotations
from typing import List, Any


class Sequence:
    __slots__ = ("_items",)

    def __init__(self, items: List[Any] | None = None) -> None:
        self._items: List[Any] = items if items is not None else []

    def append(self, item: Any) -> None:
        self._items.append(item)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def create_walker(self) -> SequenceWalker:
        return SequenceWalker(self)


class SequenceWalker:
    __slots__ = ("_seq", "_cur", "_remaining")

    def __init__(self, seq: Sequence) -> None:
        self._seq = seq
        self._cur = 0
        self._remaining = len(seq)

    def __iter__(self) -> SequenceWalker:
        return self

    def __next__(self) -> Any:
        if self._remaining <= 0:
            raise StopIteration
        item = self._seq[self._cur]
        self._cur += 1
        self._remaining -= 1
        return item

    def peek(self, ahead: int = 0) -> Any:
        idx = self._cur + ahead
        if idx >= len(self._seq):
            raise IndexError("Peek beyond bounds")
        return self._seq[idx]

    def skip(self, n: int = 1) -> None:
        if n > self._remaining:
            n = self._remaining
        self._cur += n
        self._remaining -= n


def main() -> None:
    seq = Sequence([10, 20, 30, 40, 50])

    w1 = seq.create_walker()
    w2 = seq.create_walker()

    print(w1.__next__())
    print(w1.__next__())

    print(w2.peek())
    w2.skip(2)
    print(w2.__next__())

    for item in w1:
        print(item)

    print(list(w2))


if __name__ == "__main__":
    main()