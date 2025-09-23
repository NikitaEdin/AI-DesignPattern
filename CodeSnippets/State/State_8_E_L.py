# Design Pattern: State
# This implementation demonstrates a simple state machine with two states: "on" and "off".

class LightState:
    def __init__(self, light):
        self.light = light

    def on(self):
        print("Turning on the light...")
        self.light.state = "on"

    def off(self):
        print("Turning off the light...")
        self.light.state = "off"

class Light:
    def __init__(self):
        self.state = "off"

    def turn_on(self):
        # Create a new State instance and pass in this Light instance
        self.state = LightState(self)
        self.state.on()

    def turn_off(self):
        self.state.off()

# Usage:
light = Light()
light.turn_on()
light.turn_off()