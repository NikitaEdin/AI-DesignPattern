class Light:
    def on(self): print("Light is ON")
    def off(self): print("Light is OFF")
class BaseAction:
    def perform(self): raise NotImplementedError
class TurnOn(BaseAction):
    def __init__(self, device): self.device = device
    def perform(self): self.device.on()
class TurnOff(BaseAction):
    def __init__(self, device): self.device = device
    def perform(self): self.device.off()
class Remote:
    def set_action(self, action): self.action = action
    def press(self): self.action.perform()
if __name__ == "__main__":
    lamp = Light()
    on = TurnOn(lamp); off = TurnOff(lamp)
    remote = Remote()
    remote.set_action(on); remote.press()
    remote.set_action(off); remote.press()