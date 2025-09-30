class Action:
    def execute(self):
        pass

class Light:
    def turn_on(self):
        print("Light is on")
    
    def turn_off(self):
        print("Light is off")

class LightOnAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()

class LightOffAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()

class Remote:
    def __init__(self):
        self.slot = None
    
    def set_action(self, action):
        self.slot = action
    
    def press_button(self):
        self.slot.execute()

if __name__ == "__main__":
    light = Light()
    on_action = LightOnAction(light)
    off_action = LightOffAction(light)
    
    remote = Remote()
    
    remote.set_action(on_action)
    remote.press_button()
    
    remote.set_action(off_action)
    remote.press_button()