class Light:
    def on(self): print("Light is ON")
    def off(self): print("Light is OFF")
class Action:
    def execute(self): raise NotImplementedError
class TurnOnAction(Action):
    def __init__(self, r): self.r = r
    def execute(self): self.r.on()
class TurnOffAction(Action):
    def __init__(self, r): self.r = r
    def execute(self): self.r.off()
class Switch:
    def __init__(self): self.action = None
    def set_action(self, action): self.action = action
    def press(self):
        if self.action: self.action.execute()
if __name__ == "__main__":
    lamp = Light()
    on = TurnOnAction(lamp); off = TurnOffAction(lamp)
    sw = Switch()
    sw.set_action(on); sw.press()
    sw.set_action(off); sw.press()