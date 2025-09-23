from abc import ABC, abstractmethod

class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print("Light is on")

    def turn_off(self):
        self.is_on = False
        print("Light is off")

class Executable(ABC):
    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def reverse(self):
        pass

class TurnOn(Executable):
    def __init__(self, light):
        self.light = light

    def perform(self):
        self.light.turn_on()

    def reverse(self):
        self.light.turn_off()

class TurnOff(Executable):
    def __init__(self, light):
        self.light = light

    def perform(self):
        self.light.turn_off()

    def reverse(self):
        self.light.turn_on()

class Remote:
    def __init__(self):
        self.current = None
        self.history = []

    def set_operation(self, operation):
        if not isinstance(operation, Executable):
            raise ValueError("Invalid operation")
        self.current = operation

    def press(self):
        if self.current:
            self.current.perform()
            self.history.append(self.current)
            self.current = None
        else:
            print("No operation set")

    def undo(self):
        if self.history:
            last = self.history.pop()
            last.reverse()
        else:
            print("Nothing to undo")

if __name__ == "__main__":
    light = Light()
    remote = Remote()
    on_op = TurnOn(light)
    off_op = TurnOff(light)
    remote.set_operation(on_op)
    remote.press()
    remote.set_operation(off_op)
    remote.press()
    remote.undo()
    remote.undo()