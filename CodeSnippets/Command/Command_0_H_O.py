from abc import ABC, abstractmethod
from typing import List, Optional


class ActionBase(ABC):
    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def revert(self) -> bool:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class Device:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False
        self.level = 0

    def turn_on(self):
        self.is_on = True
        return True

    def turn_off(self):
        self.is_on = False
        return True

    def set_level(self, value: int):
        if not (0 <= value <= 100):
            raise ValueError("level out of range")
        self.level = value
        return True

    def state(self):
        return {"name": self.name, "is_on": self.is_on, "level": self.level}


class TurnOn(ActionBase):
    def __init__(self, device: Device):
        self.device = device
        self.previous = None

    def execute(self) -> bool:
        try:
            self.previous = self.device.state().copy()
            return self.device.turn_on()
        except Exception:
            return False

    def revert(self) -> bool:
        try:
            if self.previous is None:
                return False
            if not self.previous["is_on"]:
                return self.device.turn_off()
            return True
        except Exception:
            return False

    def describe(self) -> str:
        return f"TurnOn({self.device.name})"


class TurnOff(ActionBase):
    def __init__(self, device: Device):
        self.device = device
        self.previous = None

    def execute(self) -> bool:
        try:
            self.previous = self.device.state().copy()
            return self.device.turn_off()
        except Exception:
            return False

    def revert(self) -> bool:
        try:
            if self.previous is None:
                return False
            if self.previous["is_on"]:
                return self.device.turn_on()
            return True
        except Exception:
            return False

    def describe(self) -> str:
        return f"TurnOff({self.device.name})"


class SetLevel(ActionBase):
    def __init__(self, device: Device, level: int):
        self.device = device
        self.level = level
        self.previous = None

    def execute(self) -> bool:
        try:
            self.previous = self.device.state().copy()
            return self.device.set_level(self.level)
        except Exception:
            return False

    def revert(self) -> bool:
        try:
            if self.previous is None:
                return False
            return self.device.set_level(self.previous["level"])
        except Exception:
            return False

    def describe(self) -> str:
        return f"SetLevel({self.device.name}, {self.level})"


class GroupAction(ActionBase):
    def __init__(self, actions: List[ActionBase]):
        self.actions = actions

    def execute(self) -> bool:
        executed = []
        for a in self.actions:
            ok = a.execute()
            if not ok:
                for e in reversed(executed):
                    e.revert()
                return False
            executed.append(a)
        return True

    def revert(self) -> bool:
        success = True
        for a in reversed(self.actions):
            success = a.revert() and success
        return success

    def describe(self) -> str:
        parts = ", ".join(a.describe() for a in self.actions)
        return f"Group([{parts}])"


class Controller:
    def __init__(self):
        self.history: List[ActionBase] = []
        self.future: List[ActionBase] = []

    def perform(self, action: ActionBase) -> bool:
        try:
            ok = action.execute()
        except Exception:
            ok = False
        if ok:
            self.history.append(action)
            self.future.clear()
        return ok

    def undo(self) -> bool:
        if not self.history:
            return False
        action = self.history.pop()
        try:
            ok = action.revert()
        except Exception:
            ok = False
        if ok:
            self.future.append(action)
        return ok

    def redo(self) -> bool:
        if not self.future:
            return False
        action = self.future.pop()
        try:
            ok = action.execute()
        except Exception:
            ok = False
        if ok:
            self.history.append(action)
        return ok

    def status(self):
        return {
            "history": [a.describe() for a in self.history],
            "future": [a.describe() for a in self.future],
        }


if __name__ == "__main__":
    d = Device("Lamp")
    c = Controller()

    a1 = TurnOn(d)
    a2 = SetLevel(d, 30)
    a3 = SetLevel(d, 150)
    a4 = TurnOff(d)

    print("Perform a1", c.perform(a1), d.state())
    print("Perform a2", c.perform(a2), d.state())
    print("Attempt a3 (invalid)", c.perform(a3), d.state())
    group = GroupAction([SetLevel(d, 60), TurnOff(d)])
    print("Perform group", c.perform(group), d.state())
    print("History/Future", c.status())
    print("Undo", c.undo(), d.state())
    print("Undo", c.undo(), d.state())
    print("Redo", c.redo(), d.state())
    print("Final History/Future", c.status())