class Action:
    def execute(self):
        raise NotImplementedError

class Light:
    def __init__(self):
        self.is_on = False
    def on(self):
        self.is_on = True
    def off(self):
        self.is_on = False
    def __str__(self):
        return "Light is on" if self.is_on else "Light is off"

class TurnOn(Action):
    def __init__(self, receiver):
        self.receiver = receiver
    def execute(self):
        self.receiver.on()

class TurnOff(Action):
    def __init__(self, receiver):
        self.receiver = receiver
    def execute(self):
        self.receiver.off()

class Remote:
    def __init__(self):
        self.slot = None
    def set_action(self, action):
        self.slot = action
    def press(self):
        if self.slot:
            self.slot.execute()

if __name__ == "__main__":
    lamp = Light()
    on_action = TurnOn(lamp)
    off_action = TurnOff(lamp)
    remote = Remote()
    remote.set_action(on_action)
    remote.press()
    print(lamp)
    remote.set_action(off_action)
    remote.press()
    print(lamp)