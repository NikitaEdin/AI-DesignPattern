class Light:
    def turn_on(self):
        print("Light is on")

    def turn_off(self):
        print("Light is off")

class TurnOnAction:
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

class TurnOffAction:
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

class Switch:
    def __init__(self):
        self.action = None

    def set_action(self, action):
        self.action = action

    def press(self):
        self.action.execute()

if __name__ == "__main__":
    light = Light()
    switch = Switch()
    switch.set_action(TurnOnAction(light))
    switch.press()
    switch.set_action(TurnOffAction(light))
    switch.press()