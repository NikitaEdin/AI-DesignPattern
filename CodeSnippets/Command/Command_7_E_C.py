class Action:
    def execute(self):
        pass

class TurnOn(Action):
    def __init__(self, device):
        self.device = device
    
    def execute(self):
        self.device.on()

class TurnOff(Action):
    def __init__(self, device):
        self.device = device
    
    def execute(self):
        self.device.off()

class Light:
    def on(self):
        print("Light is on")
    
    def off(self):
        print("Light is off")

class Remote:
    def __init__(self):
        self.action = None
    
    def set_action(self, action):
        self.action = action
    
    def press_button(self):
        if self.action:
            self.action.execute()

if __name__ == "__main__":
    light = Light()
    remote = Remote()
    
    turn_on = TurnOn(light)
    turn_off = TurnOff(light)
    
    remote.set_action(turn_on)
    remote.press_button()
    
    remote.set_action(turn_off)
    remote.press_button()