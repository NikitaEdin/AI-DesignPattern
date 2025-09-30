class Light:
    def on(self):
        print("Light is ON")
    def off(self):
        print("Light is OFF")

class SwitchOn:
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.on()

class SwitchOff:
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.off()

class Remote:
    def __init__(self):
        self.buttons = {}
    def set(self, name, action):
        self.buttons[name] = action
    def press(self, name):
        self.buttons[name].execute()

if __name__ == "__main__":
    lamp = Light()
    remote = Remote()
    remote.set("A", SwitchOn(lamp))
    remote.set("B", SwitchOff(lamp))
    remote.press("A")
    remote.press("B")