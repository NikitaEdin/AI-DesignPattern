import abc
from typing import List, Optional

class Task(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None: ...
    @abc.abstractmethod
    def undo(self) -> None: ...

class NoOp(Task):
    def execute(self) -> None: pass
    def undo(self) -> None: pass

class LightOn(Task):
    def __init__(self, light): self._light = light
    def execute(self) -> None: self._light.switch(True)
    def undo(self) -> None: self._light.switch(False)

class LightOff(Task):
    def __init__(self, light): self._light = light
    def execute(self) -> None: self._light.switch(False)
    def undo(self) -> None: self._light.switch(True)

class Macro(Task):
    def __init__(self, tasks: List[Task]): self._tasks = tasks
    def execute(self) -> None:
        for t in self._tasks: t.execute()
    def undo(self) -> None:
        for t in reversed(self._tasks): t.undo()

class DelayDecorator(Task):
    def __init__(self, task: Task, delay: float): self._task = task; self._delay = delay
    def execute(self) -> None:
        import time; time.sleep(self._delay); self._task.execute()
    def undo(self) -> None: self._task.undo()

class Invoker:
    def __init__(self): self._history: List[Task] = []; self._future: List[Task] = []
    def submit(self, task: Task) -> None:
        task.execute(); self._history.append(task); self._future.clear()
    def undo(self) -> None:
        if self._history: t = self._history.pop(); t.undo(); self._future.append(t)
    def redo(self) -> None:
        if self._future: t = self._future.pop(); t.execute(); self._history.append(t)

class Light:
    def __init__(self, name): self._name = name; self._state = False
    def switch(self, state: bool) -> None:
        self._state = state; print(f"{self._name} {'ON' if state else 'OFF'}")
    @property
    def state(self): return self._state

if __name__ == "__main__":
    living = Light("Living Room"); bedroom = Light("Bedroom")
    invoker = Invoker()
    invoker.submit(Macro([LightOn(living), LightOff(bedroom)]))
    invoker.undo(); invoker.redo()
    invoker.submit(DelayDecorator(LightOn(bedroom), 0.2))