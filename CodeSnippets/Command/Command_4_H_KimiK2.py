import asyncio
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Any
import weakref

class Task(ABC):
    __slots__ = ("_history_ref",)
    def __init__(self, history: "History"):
        self._history_ref = weakref.ref(history)
    @abstractmethod
    async def execute(self) -> Any: ...
    @abstractmethod
    async def undo(self) -> None: ...
    def _record(self) -> None:
        hist = self._history_ref()
        if hist: hist._push(self)

class History:
    __slots__ = ("_stack", "_max_size")
    def __init__(self, max_size: int = 100):
        self._stack: List[Task] = []
        self._max_size = max_size
    def _push(self, task: Task) -> None:
        if len(self._stack) >= self._max_size:
            self._stack.pop(0)
        self._stack.append(task)
    async def revert_last(self) -> None:
        if self._stack:
            await self._stack.pop().undo()

class AddToList(Task):
    __slots__ = ("_lst", "_value", "_index")
    def __init__(self, history: History, lst: List[Any], value: Any):
        super().__init__(history)
        self._lst = lst
        self._value = value
        self._index: Optional[int] = None
    async def execute(self) -> None:
        self._index = len(self._lst)
        self._lst.append(self._value)
        self._record()
    async def undo(self) -> None:
        if self._index is not None and self._index < len(self._lst):
            self._lst.pop(self._index)

class MultiplyBy(Task):
    __slots__ = ("_target", "_factor", "_prev")
    def __init__(self, history: History, target: List[int], factor: int):
        super().__init__(history)
        self._target = target
        self._factor = factor
        self._prev: List[int] = []
    async def execute(self) -> None:
        self._prev = self._target.copy()
        for i in range(len(self._target)):
            self._target[i] *= self._factor
        self._record()
    async def undo(self) -> None:
        self._target[:] = self._prev

class Scheduler:
    __slots__ = ("_history",)
    def __init__(self):
        self._history = History()
    def add(self, lst: List[Any], value: Any) -> Task:
        return AddToList(self._history, lst, value)
    def multiply(self, target: List[int], factor: int) -> Task:
        return MultiplyBy(self._history, target, factor)
    async def revert(self):
        await self._history.revert_last()

async def main():
    sched = Scheduler()
    data, nums = [], [1, 2, 3]
    await sched.add(data, "x").execute()
    await sched.multiply(nums, 10).execute()
    print(data, nums)
    await sched.revert()
    await sched.revert()
    print(data, nums)

if __name__ == "__main__":
    asyncio.run(main())