from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self): pass

class Light:
    def on(self): print("Light is on")
    def off(self): print("Light is off")

class LightOn(Action):
    def __init__(self, light): self.light = light
    def execute(self): self.light.on()

class LightOff(Action):
    def __init__(self, light): self.light = light
    def execute(self): self.light.off()

class Remote:
    def submit(self, action): action.execute()

if __name__ == "__main__":
    light = Light()
    remote = Remote()
    remote.submit(LightOn(light))
    remote.submit(LightOff(light))