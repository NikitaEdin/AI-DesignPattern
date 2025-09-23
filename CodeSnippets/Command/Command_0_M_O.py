class OperationBase:
    def perform(self):
        raise NotImplementedError
    def undo(self):
        raise NotImplementedError

class Device:
    def __init__(self, name):
        self.name = name
        self.state = False
    def activate(self):
        if not self.state:
            self.state = True
            print(f"{self.name} activated")
    def deactivate(self):
        if self.state:
            self.state = False
            print(f"{self.name} deactivated")

class TurnOn(OperationBase):
    def __init__(self, device):
        self.device = device
    def perform(self):
        self.device.activate()
    def undo(self):
        self.device.deactivate()

class TurnOff(OperationBase):
    def __init__(self, device):
        self.device = device
    def perform(self):
        self.device.deactivate()
    def undo(self):
        self.device.activate()

class MacroOperation(OperationBase):
    def __init__(self, operations):
        self.operations = list(operations)
    def perform(self):
        for op in self.operations:
            op.perform()
    def undo(self):
        for op in reversed(self.operations):
            op.undo()

class RemoteControl:
    def __init__(self):
        self.history = []
    def submit(self, operation):
        if not isinstance(operation, OperationBase):
            raise TypeError("operation must derive from OperationBase")
        try:
            operation.perform()
            self.history.append(operation)
        except Exception as e:
            print(f"Execution failed: {e}")
    def revert(self):
        if not self.history:
            print("No operations to revert")
            return
        op = self.history.pop()
        try:
            op.undo()
        except Exception as e:
            print(f"Undo failed: {e}")

if __name__ == "__main__":
    lamp = Device("Lamp")
    fan = Device("Fan")
    turn_lamp_on = TurnOn(lamp)
    turn_fan_on = TurnOn(fan)
    turn_lamp_off = TurnOff(lamp)
    all_on = MacroOperation([turn_lamp_on, turn_fan_on])
    remote = RemoteControl()
    remote.submit(turn_lamp_on)
    remote.submit(turn_lamp_off)
    remote.revert()
    remote.submit(all_on)
    remote.revert()
    remote.revert()