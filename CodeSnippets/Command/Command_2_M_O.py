from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class ActionBase(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def undo(self) -> None:
        raise NotImplementedError


class NoOpAction(ActionBase):
    def execute(self) -> None:
        return None

    def undo(self) -> None:
        return None


class Light:
    def __init__(self) -> None:
        self.is_on = False

    def turn_on(self) -> None:
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False

    def toggle(self) -> None:
        self.is_on = not self.is_on


class SwitchOn(ActionBase):
    def __init__(self, device: Light) -> None:
        self.device = device

    def execute(self) -> None:
        self.device.turn_on()

    def undo(self) -> None:
        self.device.turn_off()


class SwitchOff(ActionBase):
    def __init__(self, device: Light) -> None:
        self.device = device

    def execute(self) -> None:
        self.device.turn_off()

    def undo(self) -> None:
        self.device.turn_on()


class ToggleSequence(ActionBase):
    def __init__(self, actions: List[ActionBase]) -> None:
        self.actions = list(actions)

    def execute(self) -> None:
        executed: List[ActionBase] = []
        try:
            for a in self.actions:
                a.execute()
                executed.append(a)
        except Exception:
            # rollback executed sub-actions in reverse order
            for e in reversed(executed):
                try:
                    e.undo()
                except Exception:
                    pass
            raise

    def undo(self) -> None:
        for a in reversed(self.actions):
            a.undo()


class RemoteControl:
    def __init__(self) -> None:
        self.slots: Dict[int, ActionBase] = {}
        self.history: List[ActionBase] = []

    def set_slot(self, slot: int, action: Optional[ActionBase]) -> None:
        if action is None:
            self.slots.pop(slot, None)
            return
        if not isinstance(action, ActionBase):
            raise TypeError("action must derive from ActionBase")
        self.slots[slot] = action

    def press(self, slot: int) -> None:
        action = self.slots.get(slot, NoOpAction())
        action.execute()
        self.history.append(action)

    def press_undo(self) -> None:
        if not self.history:
            return
        action = self.history[-1]  # peek
        action.undo()
        self.history.pop()


if __name__ == "__main__":
    lamp = Light()
    rc = RemoteControl()
    on = SwitchOn(lamp)
    off = SwitchOff(lamp)
    rc.set_slot(1, on)
    rc.set_slot(2, off)
    rc.press(1)
    print("Lamp on?", lamp.is_on)  # True
    rc.press_undo()
    print("Lamp on after undo?", lamp.is_on)  # False

    # Composite usage
    seq = ToggleSequence([on, off, on])
    rc.set_slot(3, seq)
    rc.press(3)
    print("Lamp on after sequence?", lamp.is_on)
    rc.press_undo()
    print("Lamp on after sequence undo?", lamp.is_on)