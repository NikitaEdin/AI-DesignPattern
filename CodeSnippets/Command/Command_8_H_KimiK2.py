import abc
from typing import List, Optional
import time


class Task(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None: ...
    @abc.abstractmethod
    def undo(self) -> None: ...


class LightControl:
    def __init__(self, room: str):
        self.room = room
        self.state = False

    def turn_on(self) -> None:
        self.state = True
        print(f"{self.room} light ON")

    def turn_off(self) -> None:
        self.state = False
        print(f"{self.room} light OFF")


class LightOn(Task):
    def __init__(self, light: LightControl):
        self.light = light
        self.executed = False

    def execute(self) -> None:
        if not self.light.state:
            self.light.turn_on()
            self.executed = True

    def undo(self) -> None:
        if self.executed:
            self.light.turn_off()
            self.executed = False


class LightOff(Task):
    def __init__(self, light: LightControl):
        self.light = light
        self.executed = False

    def execute(self) -> None:
        if self.light.state:
            self.light.turn_off()
            self.executed = True

    def undo(self) -> None:
        if self.executed:
            self.light.turn_on()
            self.executed = False


class DelayedTask(Task):
    def __init__(self, inner: Task, delay: float):
        self.inner = inner
        self.delay = delay

    def execute(self) -> None:
        time.sleep(self.delay)
        self.inner.execute()

    def undo(self) -> None:
        time.sleep(self.delay)
        self.inner.undo()


class Invoker:
    def __init__(self):
        self.history: List[Task] = []

    def submit(self, task: Task) -> None:
        task.execute()
        self.history.append(task)

    def last_undo(self) -> Optional[Task]:
        if not self.history:
            return None
        task = self.history.pop()
        task.undo()
        return task


if __name__ == "__main__":
    living_light = LightControl("Living Room")
    bedroom_light = LightControl("Bedroom")

    remote = Invoker()
    remote.submit(LightOn(living_light))
    remote.submit(DelayedTask(LightOn(bedroom_light), 0.5))
    remote.submit(LightOff(living_light))
    print("Undo last:", remote.last_undo())
    print("Undo last:", remote.last_undo())