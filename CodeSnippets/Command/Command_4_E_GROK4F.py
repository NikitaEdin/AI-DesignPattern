from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self):
        pass

class Light:
    def turn_on(self):
        print("Light is on")
    def turn_off(self):
        print("Light is off")

class TurnOn:
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.turn_on()

class TurnOff:
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.turn_off()

class Remote:
    def __init__(self):
        self.operation = None
    def set_operation(self, operation):
        self.operation = operation
    def press_button(self):
        if self.operation:
            self.operation.execute()

if __name__ == "__main__":
    light = Light()
    turn_on = TurnOn(light)
    turn_off = TurnOff(light)
    remote = Remote()
    remote.set_operation(turn_on)
    remote.press_button()
    remote.set_operation(turn_off)
    remote.press_button()