from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Light:
    def __init__(self):
        self._state = False

    def is_on(self):
        return self._state

    def turn_on(self):
        if not self._state:
            self._state = True
            print("Light is ON")
        else:
            print("Light is already ON")

    def turn_off(self):
        if self._state:
            self._state = False
            print("Light is OFF")
        else:
            print("Light is already OFF")

class GarageDoor:
    def __init__(self):
        self._open = False

    def is_open(self):
        return self._open

    def open(self):
        if not self._open:
            self._open = True
            print("Garage door opens")
        else:
            print("Garage door is already open")

    def close(self):
        if self._open:
            self._open = False
            print("Garage door closes")
        else:
            print("Garage door is already closed")

class LightOn(Operation):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.previous_state = self.light.is_on()
        self.light.turn_on()

    def undo(self):
        if self.previous_state:
            self.light.turn_on()
        else:
            self.light.turn_off()

class LightOff(Operation):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.previous_state = self.light.is_on()
        self.light.turn_off()

    def undo(self):
        if self.previous_state:
            self.light.turn_on()
        else:
            self.light.turn_off()

class OpenGarage(Operation):
    def __init__(self, door):
        self.door = door

    def execute(self):
        self.previous_state = self.door.is_open()
        self.door.open()

    def undo(self):
        if self.previous_state:
            self.door.open()
        else:
            self.door.close()

class Sequence(Operation):
    def __init__(self, operations):
        self.operations = operations

    def execute(self):
        for op in self.operations:
            op.execute()

    def undo(self):
        for op in reversed(self.operations):
            op.undo()

class Remote:
    def __init__(self):
        self.slots = [None] * 3
        self.history = []

    def set_slot(self, slot, operation):
        if 0 <= slot < len(self.slots):
            self.slots[slot] = operation

    def press_slot(self, slot):
        if 0 <= slot < len(self.slots):
            operation = self.slots[slot]
            if operation:
                operation.execute()
                self.history.append(operation)

    def undo_last(self):
        if self.history:
            last = self.history.pop()
            last.undo()

if __name__ == "__main__":
    light = Light()
    garage = GarageDoor()
    light_on = LightOn(light)
    garage_open = OpenGarage(garage)
    routine = Sequence([garage_open, light_on])
    remote = Remote()
    print("Press light on:")
    remote.set_slot(0, light_on)
    remote.press_slot(0)
    print("Undo light on:")
    remote.undo_last()
    print("Press routine:")
    remote.set_slot(1, routine)
    remote.press_slot(1)
    print("Undo routine:")
    remote.undo_last()