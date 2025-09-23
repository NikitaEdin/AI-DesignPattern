from abc import ABC, abstractmethod

class BaseAction(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class LightReceiver:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        if self.is_on:
            raise RuntimeError("Light is already on")
        self.is_on = True
        print("Light turned on")

    def turn_off(self):
        if not self.is_on:
            raise RuntimeError("Light is already off")
        self.is_on = False
        print("Light turned off")

class TurnOn(BaseAction):
    def __init__(self, receiver: LightReceiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.turn_on()

    def undo(self):
        self.receiver.turn_off()

class TurnOff(BaseAction):
    def __init__(self, receiver: LightReceiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.turn_off()

    def undo(self):
        self.receiver.turn_on()

class Invoker:
    def __init__(self):
        self._history = []

    def perform(self, action: BaseAction):
        try:
            action.execute()
            self._history.append(action)
        except Exception as e:
            print(f"Execution failed: {e}")

    def undo_last(self):
        if not self._history:
            print("No actions to undo")
            return
        action = self._history.pop()
        try:
            action.undo()
        except Exception as e:
            print(f"Undo failed: {e}")

if __name__ == "__main__":
    light = LightReceiver()
    inv = Invoker()
    on = TurnOn(light)
    off = TurnOff(light)

    inv.perform(on)
    inv.perform(on)
    inv.perform(off)
    inv.undo_last()
    inv.undo_last()
    inv.undo_last()