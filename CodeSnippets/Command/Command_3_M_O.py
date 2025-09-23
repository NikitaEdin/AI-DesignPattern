from abc import ABC, abstractmethod

class ActionInterface(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Device:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False

    def on(self):
        if self.is_on:
            raise RuntimeError(f"{self.name} is already on")
        self.is_on = True
        print(f"{self.name} turned on")

    def off(self):
        if not self.is_on:
            raise RuntimeError(f"{self.name} is already off")
        self.is_on = False
        print(f"{self.name} turned off")

    def __repr__(self):
        return f"<Device {self.name} is_on={self.is_on}>"

class TurnOn(ActionInterface):
    def __init__(self, device: Device):
        self.device = device

    def execute(self):
        self.device.on()

    def undo(self):
        self.device.off()

class TurnOff(ActionInterface):
    def __init__(self, device: Device):
        self.device = device

    def execute(self):
        self.device.off()

    def undo(self):
        self.device.on()

class GroupAction(ActionInterface):
    def __init__(self, actions):
        self.actions = list(actions)

    def execute(self):
        executed = []
        try:
            for act in self.actions:
                act.execute()
                executed.append(act)
        except Exception as e:
            for act in reversed(executed):
                try:
                    act.undo()
                except Exception:
                    pass
            raise

    def undo(self):
        for act in reversed(self.actions):
            act.undo()

class Controller:
    def __init__(self):
        self._history = []

    def invoke(self, action: ActionInterface):
        try:
            action.execute()
            self._history.append(action)
        except Exception as e:
            print(f"Invocation failed: {e}")

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
    lamp = Device("Lamp")
    fan = Device("Fan")
    controller = Controller()

    on_lamp = TurnOn(lamp)
    off_lamp = TurnOff(lamp)
    on_fan = TurnOn(fan)

    controller.invoke(on_lamp)
    controller.invoke(on_fan)

    scene = GroupAction([off_lamp, on_fan])
    controller.invoke(scene)  # will attempt group; off_lamp may raise if lamp already off

    controller.undo_last()  # undo the last successful action
    controller.undo_last()
    controller.undo_last()
    controller.undo_last()