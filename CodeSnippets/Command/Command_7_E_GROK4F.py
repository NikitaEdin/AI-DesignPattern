from abc import ABC, abstractmethod

class Light:
    def turn_on(self):
        print("Light is on")

    def turn_off(self):
        print("Light is off")

class Operation(ABC):
    @abstractmethod
    def execute(self):
        pass

class TurnOn(Operation):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

class TurnOff(Operation):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

class RemoteControl:
    def __init__(self):
        self.current_action = None

    def set_action(self, action):
        self.current_action = action

    def press_button(self):
        if self.current_action:
            self.current_action.execute()

if __name__ == "__main__":
    light = Light()
    remote = RemoteControl()
    turn_on = TurnOn(light)
    remote.set_action(turn_on)
    remote.press_button()
    turn_off = TurnOff(light)
    remote.set_action(turn_off)
    remote.press_button()