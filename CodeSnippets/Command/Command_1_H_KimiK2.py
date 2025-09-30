from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
import time


class Task(ABC):
    def __init__(self) -> None:
        self._timestamp: float = time.time()

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def revoke(self) -> None:
        pass


class Light:
    def __init__(self) -> None:
        self.level = 0

    def set_level(self, value: int) -> None:
        self.level = value


class LightOn(Task):
    def __init__(self, light: Light) -> None:
        super().__init__()
        self.light = light
        self.old_level = light.level

    def run(self) -> None:
        self.old_level = self.light.level
        self.light.set_level(100)

    def revoke(self) -> None:
        self.light.set_level(self.old_level)


class LightOff(Task):
    def __init__(self, light: Light) -> None:
        super().__init__()
        self.light = light
        self.old_level = light.level

    def run(self) -> None:
        self.old_level = self.light.level
        self.light.set_level(0)

    def revoke(self) -> None:
        self.light.set_level(self.old_level)


class ChangeBrightness(Task):
    def __init__(self, light: Light, delta: int) -> None:
        super().__init__()
        self.light = light
        self.delta = delta
        self.old_level = light.level

    def run(self) -> None:
        self.old_level = self.light.level
        self.light.set_level(max(0, min(100, self.light.level + self.delta)))

    def revoke(self) -> None:
        self.light.set_level(self.old_level)


class Macro(Task):
    def __init__(self) -> None:
        super().__init__()
        self.tasks: List[Task] = []

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def run(self) -> None:
        for t in self.tasks:
            t.run()

    def revoke(self) -> None:
        for t in reversed(self.tasks):
            t.revoke()


class QueueManager:
    def __init__(self) -> None:
        self.past: List[Task] = []
        self.future: List[Task] = []

    def schedule(self, task: Task) -> None:
        task.run()
        self.past.append(task)
        self.future.clear()

    def undo(self) -> None:
        if self.past:
            t = self.past.pop()
            t.revoke()
            self.future.append(t)

    def redo(self) -> None:
        if self.future:
            t = self.future.pop()
            t.run()
            self.past.append(t)


if __name__ == "__main__":
    light = Light()
    manager = QueueManager()
    mac = Macro()
    mac.add(LightOn(light))
    mac.add(ChangeBrightness(light, -45))
    manager.schedule(mac)
    manager.undo()
    manager.redo()