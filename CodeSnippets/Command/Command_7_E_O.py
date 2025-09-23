class Action:
    def run(self):
        raise NotImplementedError

class Light:
    def turn_on(self):
        print("Light: ON")
    def turn_off(self):
        print("Light: OFF")

class TurnOn(Action):
    def __init__(self, device):
        self.device = device
    def run(self):
        self.device.turn_on()

class TurnOff(Action):
    def __init__(self, device):
        self.device = device
    def run(self):
        self.device.turn_off()

class Controller:
    def __init__(self):
        self.slot = None
    def set_action(self, action):
        self.slot = action
    def invoke(self):
        if self.slot:
            self.slot.run()

if __name__ == "__main__":
    lamp = Light()
    ctrl = Controller()
    on = TurnOn(lamp)
    off = TurnOff(lamp)
    ctrl.set_action(on)
    ctrl.invoke()
    ctrl.set_action(off)
    ctrl.invoke()