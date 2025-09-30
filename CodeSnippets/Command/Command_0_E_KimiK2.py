class Light:
    def on(self):
        print("Light on")
    def off(self):
        print("Light off")

class Action:
    def execute(self): pass

class LightOn(Action):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.on()

class LightOff(Action):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.off()

class Remote:
    def __init__(self):
        self.slot = None
    def set_action(self, action):
        self.slot = action
    def press(self):
        self.slot.execute()

if __name__ == "__main__":
    light = Light()
    remote = Remote()
    remote.set_action(LightOn(light))
    remote.press()
    remote.set_action(LightOff(light))
    remote.press()