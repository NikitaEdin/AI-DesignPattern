from abc import ABC, abstractmethod
from typing import List


class LightDevice:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False
        self.brightness = 0

    def switch(self, state: bool):
        if not isinstance(state, bool):
            raise ValueError("state must be boolean")
        self.is_on = state

    def set_brightness(self, level: int):
        if not 0 <= level <= 100:
            raise ValueError("brightness must be 0-100")
        self.brightness = level


class ActionBase(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class TurnOn(ActionBase):
    def __init__(self, device: LightDevice):
        self.device = device
        self._prev = None

    def execute(self):
        self._prev = (self.device.is_on, self.device.brightness)
        self.device.switch(True)
        if self.device.brightness == 0:
            self.device.set_brightness(50)
        return True

    def undo(self):
        if self._prev is None:
            raise RuntimeError("Nothing to undo")
        self.device.switch(self._prev[0])
        self.device.set_brightness(self._prev[1])


class TurnOff(ActionBase):
    def __init__(self, device: LightDevice):
        self.device = device
        self._prev = None

    def execute(self):
        self._prev = (self.device.is_on, self.device.brightness)
        self.device.switch(False)
        return True

    def undo(self):
        if self._prev is None:
            raise RuntimeError("Nothing to undo")
        self.device.switch(self._prev[0])
        self.device.set_brightness(self._prev[1])


class AdjustBrightness(ActionBase):
    def __init__(self, device: LightDevice, level: int):
        self.device = device
        self.level = level
        self._prev = None

    def execute(self):
        self._prev = (self.device.is_on, self.device.brightness)
        if not self.device.is_on:
            raise RuntimeError("Device must be on to adjust brightness")
        self.device.set_brightness(self.level)
        return True

    def undo(self):
        if self._prev is None:
            raise RuntimeError("Nothing to undo")
        self.device.switch(self._prev[0])
        self.device.set_brightness(self._prev[1])


class GroupAction(ActionBase):
    def __init__(self, actions: List[ActionBase]):
        self.actions = actions
        self._executed: List[ActionBase] = []

    def execute(self):
        self._executed = []
        for act in self.actions:
            try:
                act.execute()
                self._executed.append(act)
            except Exception:
                for done in reversed(self._executed):
                    try:
                        done.undo()
                    except Exception:
                        pass
                raise
        return True

    def undo(self):
        for act in reversed(self._executed):
            act.undo()


class Controller:
    def __init__(self):
        self.history: List[ActionBase] = []

    def execute_action(self, action: ActionBase):
        try:
            result = action.execute()
            if result:
                self.history.append(action)
        except Exception as e:
            raise RuntimeError(f"Execution failed: {e}")

    def undo_last(self):
        if not self.history:
            raise RuntimeError("No actions to undo")
        action = self.history.pop()
        action.undo()


if __name__ == "__main__":
    lamp = LightDevice("DeskLamp")
    ctrl = Controller()
    try:
        on = TurnOn(lamp)
        bright = AdjustBrightness(lamp, 80)
        off = TurnOff(lamp)
        combo = GroupAction([on, bright])
        ctrl.execute_action(combo)
        print(lamp.name, lamp.is_on, lamp.brightness)
        ctrl.execute_action(off)
        print(lamp.name, lamp.is_on, lamp.brightness)
        ctrl.undo_last()
        print(lamp.name, lamp.is_on, lamp.brightness)
        ctrl.undo_last()
        print(lamp.name, lamp.is_on, lamp.brightness)
    except Exception as e:
        print("Error:", e)