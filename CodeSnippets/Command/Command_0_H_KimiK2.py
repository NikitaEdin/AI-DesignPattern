from __future__ import annotations
import sys
from typing import Optional, List, Any


class WorkUnit:
    def execute(self) -> None:
        raise NotImplementedError

    def revoke(self) -> None:
        raise NotImplementedError


class SetValue(WorkUnit):
    def __init__(self, target: List[int], index: int, value: int) -> None:
        self.target = target
        self.index = index
        self.value = value
        self.previous = None

    def execute(self) -> None:
        self.previous = self.target[self.index]
        self.target[self.index] = self.value

    def revoke(self) -> None:
        self.target[self.index] = self.previous


class History:
    def __init__(self, limit: int = 50) -> None:
        self.limit = limit
        self.past: List[WorkUnit] = []
        self.future: List[WorkUnit] = []

    def invoke(self, work: WorkUnit) -> None:
        work.execute()
        self.past.append(work)
        self.future.clear()
        if len(self.past) > self.limit:
            self.past.pop(0)

    def undo(self) -> None:
        if not self.past:
            return
        work = self.past.pop()
        work.revoke()
        self.future.append(work)

    def redo(self) -> None:
        if not self.future:
            return
        work = self.future.pop()
        work.execute()
        self.past.append(work)

    def batch(self, works: List[WorkUnit]) -> Any:
        batch_past = []
        for w in works:
            try:
                w.execute()
                batch_past.append(w)
            except Exception:
                for bw in reversed(batch_past):
                    bw.revoke()
                raise
        self.past.extend(batch_past)
        self.future.clear()
        if len(self.past) > self.limit:
            self.past = self.past[-self.limit:]


if __name__ == "__main__":
    data = [0, 0, 0]
    h = History(3)
    a = SetValue(data, 1, 10)
    b = SetValue(data, 2, 20)
    c = SetValue(data, 0, 30)
    h.invoke(a)
    h.invoke(b)
    h.invoke(c)
    print(data)
    h.undo()
    print(data)
    h.redo()
    print(data)
    h.undo()
    h.undo()
    print(data)