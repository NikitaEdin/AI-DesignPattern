class Light:
    def turn_on(self):
        print("Light is on")
    def turn_off(self):
        print("Light is off")

class SwitchOn:
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.turn_on()

class SwitchOff:
    def __init__(self, device):
        self.device = device
    def execute(self):
        self.device.turn_off()

class Remote:
    def __init__(self):
        self.slot = None
    def set_slot(self, action):
        self.slot = action
    def press(self):
        self.slot.execute()

if __name__ == "__main__":
    light = Light()
    on = SwitchOn(light)
    off = SwitchOff(light)
    remote = Remote()
    remote.set_slot(on)
    remote.press()
    remote.set_slot(off)
    remote.press()