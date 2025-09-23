class Action:
    def execute(self):
        raise NotImplementedError

class Light:
    def __init__(self, name):
        self.name = name
    def on(self):
        print(f"{self.name} is ON")
    def off(self):
        print(f"{self.name} is OFF")

class LightOnAction(Action):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.on()

class LightOffAction(Action):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.off()

class Switch:
    def __init__(self):
        self._action = None
    def set_action(self, action):
        self._action = action
    def press(self):
        if self._action:
            self._action.execute()

if __name__ == "__main__":
    lamp = Light("Desk Lamp")
    on = LightOnAction(lamp)
    off = LightOffAction(lamp)
    sw = Switch()
    sw.set_action(on); sw.press()
    sw.set_action(off); sw.press()