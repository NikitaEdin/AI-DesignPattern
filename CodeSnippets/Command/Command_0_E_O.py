class Action:
    def execute(self): raise NotImplementedError
class Light:
    def __init__(self, name): self.name = name
    def on(self): print(f"{self.name} is on")
    def off(self): print(f"{self.name} is off")
class TurnOn(Action):
    def __init__(self, device): self.device = device
    def execute(self): self.device.on()
class TurnOff(Action):
    def __init__(self, device): self.device = device
    def execute(self): self.device.off()
class Remote:
    def __init__(self): self._action = None
    def set(self, action): self._action = action
    def press(self):
        if self._action: self._action.execute()
if __name__ == "__main__":
    lamp = Light("Lamp")
    on = TurnOn(lamp)
    off = TurnOff(lamp)
    r = Remote()
    r.set(on); r.press()
    r.set(off); r.press()