from abc import ABC, abstractmethod

class Light(ABC):
    def turn_on(self):
        pass

    def turn_off(self):
        pass

class LivingRoomLight(Light):
    def turn_on(self):
        print("Living room light is on")

    def turn_off(self):
        print("Living room light is off")

class Remote(ABC):
    @abstractmethod
    def execute(self):
        pass

class TurnOn(Remote):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_on()

class TurnOff(Remote):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_off()

class Switch:
    def __init__(self):
        self.current_remote = None

    def set_remote(self, remote: Remote):
        self.current_remote = remote

    def press(self):
        if self.current_remote:
            self.current_remote.execute()

if __name__ == "__main__":
    light = LivingRoomLight()
    turn_on = TurnOn(light)
    turn_off = TurnOff(light)
    switch = Switch()
    switch.set_remote(turn_on)
    switch.press()
    switch.set_remote(turn_off)
    switch.press()