class Action:
    def execute(self): raise NotImplementedError
class Light:
    def __init__(self): self.on = False
    def turn_on(self): self.on = True; print("Light is on")
    def turn_off(self): self.on = False; print("Light is off")
class TurnOn(Action):
    def __init__(self, receiver): self.receiver = receiver
    def execute(self): self.receiver.turn_on()
class TurnOff(Action):
    def __init__(self, receiver): self.receiver = receiver
    def execute(self): self.receiver.turn_off()
class Remote:
    def __init__(self): self.slot = None
    def set_slot(self, action): self.slot = action
    def press(self):
        if self.slot: self.slot.execute()
if __name__ == "__main__":
    bulb = Light(); on = TurnOn(bulb); off = TurnOff(bulb); remote = Remote()
    remote.set_slot(on); remote.press()
    remote.set_slot(off); remote.press()