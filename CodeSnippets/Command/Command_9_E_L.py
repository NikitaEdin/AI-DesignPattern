class Light
    def __init__(self):
        self.state = False

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False

class RemoteControl
    def __init__(self, light):
        self.light = light

    def press_button(self):
        if self.light.state:
            self.light.turn_off()
        else:
            self.light.turn_on()