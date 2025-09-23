from abc import ABC, abstractmethod

class ActionBase(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Lamp:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        if self.is_on:
            raise RuntimeError("Lamp is already on")
        self.is_on = True

    def turn_off(self):
        if not self.is_on:
            raise RuntimeError("Lamp is already off")
        self.is_on = False

class TurnOn(ActionBase):
    def __init__(self, receiver):
        self.receiver = receiver
        self._prev = None

    def execute(self):
        if not hasattr(self.receiver, "turn_on"):
            raise TypeError("Receiver cannot be turned on")
        self._prev = self.receiver.is_on
        self.receiver.turn_on()

    def undo(self):
        if self._prev is None:
            raise RuntimeError("No previous state recorded")
        if not self._prev:
            self.receiver.turn_off()

class TurnOff(ActionBase):
    def __init__(self, receiver):
        self.receiver = receiver
        self._prev = None

    def execute(self):
        if not hasattr(self.receiver, "turn_off"):
            raise TypeError("Receiver cannot be turned off")
        self._prev = self.receiver.is_on
        self.receiver.turn_off()

    def undo(self):
        if self._prev is None:
            raise RuntimeError("No previous state recorded")
        if self._prev:
            self.receiver.turn_on()

class Remote:
    def __init__(self):
        self._history = []

    def execute_action(self, action):
        if not isinstance(action, ActionBase):
            raise TypeError("Invalid action")
        try:
            action.execute()
            self._history.append(action)
        except Exception as e:
            raise RuntimeError(f"Execution failed: {e}")

    def undo_last(self):
        if not self._history:
            raise RuntimeError("No actions to undo")
        action = self._history.pop()
        try:
            action.undo()
        except Exception as e:
            raise RuntimeError(f"Undo failed: {e}")

if __name__ == "__main__":
    lamp = Lamp()
    remote = Remote()

    on_action = TurnOn(lamp)
    off_action = TurnOff(lamp)

    try:
        remote.execute_action(on_action)
        print("Lamp state after on:", lamp.is_on)
        remote.execute_action(off_action)
        print("Lamp state after off:", lamp.is_on)
        remote.undo_last()
        print("Lamp state after undo:", lamp.is_on)
        remote.undo_last()
        print("Lamp state after second undo:", lamp.is_on)
    except Exception as err:
        print("Error:", err)