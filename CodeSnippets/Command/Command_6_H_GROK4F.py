from abc import ABC, abstractmethod

class Executable(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class NoOpExecutable(Executable):
    def execute(self):
        pass

    def undo(self):
        pass

class Light:
    def __init__(self):
        self._is_on = False

    def on(self):
        self._is_on = True
        print("Light is on")

    def off(self):
        self._is_on = False
        print("Light is off")

class LightOn(Executable):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class Fan:
    def __init__(self):
        self._is_on = False

    def on(self):
        self._is_on = True
        print("Fan is on")

    def off(self):
        self._is_on = False
        print("Fan is off")

class FanOn(Executable):
    def __init__(self, fan):
        self.fan = fan

    def execute(self):
        self.fan.on()

    def undo(self):
        self.fan.off()

class SequenceExecutable(Executable):
    def __init__(self, actions):
        self.actions = actions

    def execute(self):
        for action in self.actions:
            action.execute()

    def undo(self):
        for action in reversed(self.actions):
            action.undo()

class RemoteControl:
    def __init__(self):
        self.slots = [NoOpExecutable() for _ in range(5)]
        self.last_executed = None

    def set_slot(self, slot, executable):
        if 0 <= slot < len(self.slots):
            self.slots[slot] = executable

    def press_button(self, slot):
        if 0 <= slot < len(self.slots):
            self.slots[slot].execute()
            self.last_executed = self.slots[slot]

    def press_undo(self):
        if self.last_executed:
            self.last_executed.undo()
            self.last_executed = None

if __name__ == "__main__":
    light = Light()
    fan = Fan()
    remote = RemoteControl()
    light_on = LightOn(light)
    fan_on = FanOn(fan)
    macro = SequenceExecutable([light_on, fan_on])
    remote.set_slot(0, light_on)
    remote.set_slot(1, fan_on)
    remote.set_slot(2, macro)
    print("Press light on:")
    remote.press_button(0)
    print("\nUndo:")
    remote.press_undo()
    print("\nPress macro:")
    remote.press_button(2)
    print("\nUndo macro:")
    remote.press_undo()