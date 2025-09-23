import abc
from typing import List

class ActionBase(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass

class Device:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False

    def turn_on(self):
        if self.is_on:
            raise RuntimeError(f"{self.name} is already on")
        self.is_on = True
        return f"{self.name} turned on"

    def turn_off(self):
        if not self.is_on:
            raise RuntimeError(f"{self.name} is already off")
        self.is_on = False
        return f"{self.name} turned off"

class TurnOn(ActionBase):
    def __init__(self, device: Device):
        self.device = device

    def execute(self):
        return self.device.turn_on()

    def undo(self):
        return self.device.turn_off()

class TurnOff(ActionBase):
    def __init__(self, device: Device):
        self.device = device

    def execute(self):
        return self.device.turn_off()

    def undo(self):
        return self.device.turn_on()

class CompositeAction(ActionBase):
    def __init__(self, actions: List[ActionBase]):
        self.actions = actions

    def execute(self):
        results = []
        for a in self.actions:
            results.append(a.execute())
        return results

    def undo(self):
        results = []
        for a in reversed(self.actions):
            results.append(a.undo())
        return results

class Remote:
    def __init__(self):
        self.history: List[ActionBase] = []

    def invoke(self, action: ActionBase):
        try:
            result = action.execute()
            self.history.append(action)
            return result
        except Exception as e:
            return f"Error during execution: {e}"

    def undo_last(self):
        if not self.history:
            return "Nothing to undo"
        action = self.history.pop()
        try:
            return action.undo()
        except Exception as e:
            return f"Error during undo: {e}"

if __name__ == "__main__":
    lamp = Device("Lamp")
    fan = Device("Fan")
    turn_lamp_on = TurnOn(lamp)
    turn_fan_on = TurnOn(fan)
    turn_lamp_off = TurnOff(lamp)

    remote = Remote()
    print(remote.invoke(turn_lamp_on))
    print(remote.invoke(turn_fan_on))

    morning_routine = CompositeAction([turn_lamp_on, turn_fan_on])
    print(remote.invoke(morning_routine))

    print(remote.undo_last())
    print(remote.undo_last())
    print(remote.undo_last())
    print(remote.undo_last())