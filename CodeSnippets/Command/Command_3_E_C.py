class Action:
    def execute(self):
        pass

class LightOnAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()

class Light:
    def turn_on(self):
        print("Light is on")

class RemoteControl:
    def __init__(self):
        self.action = None
    
    def set_action(self, action):
        self.action = action
    
    def press_button(self):
        if self.action:
            self.action.execute()

if __name__ == "__main__":
    light = Light()
    light_on = LightOnAction(light)
    remote = RemoteControl()
    remote.set_action(light_on)
    remote.press_button()