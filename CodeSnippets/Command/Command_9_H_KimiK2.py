from __future__ import annotations
from abc import ABC, abstractmethod
import time
from typing import List, Optional, Dict, Any
import threading

class Task(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

class LightOn(Task):
    def __init__(self, light: 'Light') -> None:
        self.light = light
        self._prev_state: Optional[bool] = None

    def execute(self) -> None:
        self._prev_state = self.light.is_on
        self.light.turn_on()

    def undo(self) -> None:
        if self._prev_state is False:
            self.light.turn_off()

class LightOff(Task):
    def __init__(self, light: 'Light') -> None:
        self.light = light
        self._prev_state: Optional[bool] = None

    def execute(self) -> None:
        self._prev_state = self.light.is_on
        self.light.turn_off()

    def undo(self) -> None:
        if self._prev_state is True:
            self.light.turn_on()

class Light:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_on = False

    def turn_on(self) -> None:
        self.is_on = True
        print(f"{self.name} light is ON")

    def turn_off(self) -> None:
        self.is_on = False
        print(f"{self.name} light is OFF")

class DelayedTask(Task):
    def __init__(self, task: Task, delay: float) -> None:
        self.task = task
        self.delay = delay

    def execute(self) -> None:
        threading.Timer(self.delay, self.task.execute).start()

    def undo(self) -> None:
        threading.Timer(self.delay, self.task.undo).start()

class Macro(Task):
    def __init__(self, tasks: List[Task]) -> None:
        self.tasks = tasks

    def execute(self) -> None:
        for t in self.tasks:
            t.execute()

    def undo(self) -> None:
        for t in reversed(self.tasks):
            t.undo()

class Remote:
    def __init__(self) -> None:
        self._history: List[Task] = []
        self._macro_registry: Dict[str, Macro] = {}

    def submit(self, task: Task) -> None:
        task.execute()
        self._history.append(task)

    def replay_last(self) -> None:
        if self._history:
            self._history[-1].execute()

    def rollback(self) -> None:
        if self._history:
            self._history.pop().undo()

    def record_macro(self, name: str, tasks: List[Task]) -> None:
        self._macro_registry[name] = Macro(tasks)

    def run_macro(self, name: str) -> None:
        if name in self._macro_registry:
            self.submit(self._macro_registry[name])

if __name__ == "__main__":
    living = Light("Living Room")
    kitchen = Light("Kitchen")
    remote = Remote()

    remote.submit(LightOn(living))
    remote.submit(DelayedTask(LightOff(kitchen), 1))
    remote.record_macro("Arrive", [LightOn(kitchen), LightOn(living)])
    remote.run_macro("Arrive")
    time.sleep(1.2)
    remote.rollback()
    remote.rollback()