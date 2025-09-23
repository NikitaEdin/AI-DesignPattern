class Action:
    def execute(self):
        pass

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

class Light:
    def turn_on(self):
        print("Light is on")
    
    def turn_off(self):
        print("Light is off")

class RemoteControl:
    def __init__(self):
        self.action = None
    
    def set_action(self, action):
        self.action = action
    
    def press_button(self):
        self.action.execute()

if __name__ == "__main__":
    light = Light()
    on_action = LightOnAction(light)
    off_action = LightOffAction(light)
    
    remote = RemoteControl()
    remote.set_action(on_action)
    remote.press_button()
    
    remote.set_action(off_action)
    remote.press_button()