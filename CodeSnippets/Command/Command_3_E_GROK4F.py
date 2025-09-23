class LightBulb:
    def turn_on(self):
        print("Light turned on")

    def turn_off(self):
        print("Light turned off")

class TurnOn:
    def __init__(self, bulb):
        self.bulb = bulb

    def execute(self):
        self.bulb.turn_on()

class TurnOff:
    def __init__(self, bulb):
        self.bulb = bulb

    def execute(self):
        self.bulb.turn_off()

class RemoteControl:
    def __init__(self):
        self.action = None

    def set_action(self, action):
        self.action = action

    def press_button(self):
        if self.action:
            self.action.execute()

if __name__ == "__main__":
    bulb = LightBulb()
    turn_on = TurnOn(bulb)
    turn_off = TurnOff(bulb)
    remote = RemoteControl()
    remote.set_action(turn_on)
    remote.press_button()
    remote.set_action(turn_off)
    remote.press_button()