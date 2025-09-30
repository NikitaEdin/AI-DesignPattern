class Switch:
    def on(self):
        print("Light turned ON")
    def off(self):
        print("Light turned OFF")

class FlipOn:
    def __init__(self, switch):
        self.switch = switch
    def execute(self):
        self.switch.on()

class FlipOff:
    def __init__(self, switch):
        self.switch = switch
    def execute(self):
        self.switch.off()

class Remote:
    def __init__(self):
        self.history = []
    def press(self, action):
        action.execute()
        self.history.append(action)

if __name__ == "__main__":
    light = Switch()
    on = FlipOn(light)
    off = FlipOff(light)
    remote = Remote()
    remote.press(on)
    remote.press(off)