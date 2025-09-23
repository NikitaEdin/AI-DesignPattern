class Light:
    def __init__(self, name): self.name = name
    def on(self): print(f"{self.name} is on")
    def off(self): print(f"{self.name} is off")

class ActionInterface:
    def execute(self): raise NotImplementedError

class TurnOn(ActionInterface):
    def __init__(self, device): self.device = device
    def execute(self): self.device.on()

class TurnOff(ActionInterface):
    def __init__(self, device): self.device = device
    def execute(self): self.device.off()

class Remote:
    def __init__(self): self.slot = None
    def set(self, action): self.slot = action
    def press(self):
        if self.slot: self.slot.execute()

if __name__ == "__main__":
    lamp = Light("Lamp")
    remote = Remote()
    remote.set(TurnOn(lamp)); remote.press()
    remote.set(TurnOff(lamp)); remote.press()