from typing import List

class Device:
    def __init__(self, name: str):
        self.name = name
        self.state = "off"
        self.level = 0

    def turn_on(self):
        if self.state == "on":
            raise RuntimeError(f"{self.name} already on")
        self.state = "on"
        self.level = 100
        return f"{self.name} powered on"

    def turn_off(self):
        if self.state == "off":
            raise RuntimeError(f"{self.name} already off")
        self.state = "off"
        self.level = 0
        return f"{self.name} powered off"

    def set_level(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError("level must be 0-100")
        if self.state == "off":
            raise RuntimeError("device is off")
        self.level = value
        return f"{self.name} level set to {self.level}"

class ActionBase:
    def perform(self):
        raise NotImplementedError

    def revert(self):
        raise NotImplementedError

class TurnOn(ActionBase):
    def __init__(self, receiver: Device):
        self.receiver = receiver
        self.performed = False

    def perform(self):
        result = self.receiver.turn_on()
        self.performed = True
        return result

    def revert(self):
        if self.performed:
            return self.receiver.turn_off()
        raise RuntimeError("cannot revert before perform")

class TurnOff(ActionBase):
    def __init__(self, receiver: Device):
        self.receiver = receiver
        self.performed = False

    def perform(self):
        result = self.receiver.turn_off()
        self.performed = True
        return result

    def revert(self):
        if self.performed:
            return self.receiver.turn_on()
        raise RuntimeError("cannot revert before perform")

class AdjustLevel(ActionBase):
    def __init__(self, receiver: Device, value: int):
        self.receiver = receiver
        self.new_value = value
        self.previous = None

    def perform(self):
        self.previous = self.receiver.level
        return self.receiver.set_level(self.new_value)

    def revert(self):
        if self.previous is None:
            raise RuntimeError("cannot revert before perform")
        return self.receiver.set_level(self.previous)

class ActionManager:
    def __init__(self):
        self.history: List[ActionBase] = []

    def run_action(self, action: ActionBase):
        try:
            result = action.perform()
            self.history.append(action)
            return result
        except Exception as e:
            raise RuntimeError(f"action failed: {e}") from e

    def undo_last(self):
        if not self.history:
            raise RuntimeError("no actions to undo")
        action = self.history.pop()
        try:
            return action.revert()
        except Exception as e:
            raise RuntimeError(f"undo failed: {e}") from e

    def run_batch(self, actions: List[ActionBase]):
        executed: List[ActionBase] = []
        results = []
        try:
            for a in actions:
                results.append(a.perform())
                executed.append(a)
            self.history.extend(executed)
            return results
        except Exception as e:
            for a in reversed(executed):
                try:
                    a.revert()
                except Exception:
                    pass
            raise RuntimeError(f"batch failed and rolled back: {e}") from e

if __name__ == "__main__":
    lamp = Device("Lamp")
    manager = ActionManager()

    on = TurnOn(lamp)
    off = TurnOff(lamp)
    adjust = AdjustLevel(lamp, 50)

    print(manager.run_action(on))
    print(manager.run_action(adjust))
    print("Undo:", manager.undo_last())
    try:
        print(manager.run_action(off))
    except Exception as e:
        print("Error:", e)

    lamp2 = Device("Speaker")
    batch = [TurnOn(lamp2), AdjustLevel(lamp2, 30), AdjustLevel(lamp2, 200)]
    try:
        print("Batch:", manager.run_batch(batch))
    except Exception as e:
        print("Batch error:", e)
    print("Final states:", lamp.name, lamp.state, lamp.level, "|", lamp2.name, lamp2.state, lamp2.level)