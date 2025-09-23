class Lamp:
    def turn_on(self):
        print("Lamp is on")

    def turn_off(self):
        print("Lamp is off")

class TurnOnAction:
    def __init__(self, lamp):
        self.lamp = lamp

    def execute(self):
        self.lamp.turn_on()

class TurnOffAction:
    def __init__(self, lamp):
        self.lamp = lamp

    def execute(self):
        self.lamp.turn_off()

class Switch:
    def __init__(self):
        self.current_action = None

    def set_action(self, action):
        self.current_action = action

    def press(self):
        if self.current_action:
            self.current_action.execute()

if __name__ == "__main__":
    lamp = Lamp()
    switch = Switch()
    switch.set_action(TurnOnAction(lamp))
    switch.press()
    switch.set_action(TurnOffAction(lamp))
    switch.press()