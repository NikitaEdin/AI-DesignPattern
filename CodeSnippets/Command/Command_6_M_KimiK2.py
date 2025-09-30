import time

class Light:
    def __init__(self, name):
        self.name = name
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.name} light is ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.name} light is OFF")

class Action:
    def execute(self): pass
    def undo(self): pass

class LightOnAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class LightOffAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()

class RemoteControl:
    def __init__(self):
        self.history = []
    
    def press(self, action):
        action.execute()
        self.history.append(action)
    
    def press_undo(self):
        if self.history:
            last_action = self.history.pop()
            last_action.undo()

if __name__ == "__main__":
    living_room = Light("Living Room")
    kitchen = Light("Kitchen")
    
    remote = RemoteControl()
    
    remote.press(LightOnAction(living_room))
    remote.press(LightOnAction(kitchen))
    remote.press_undo()
    remote.press(LightOffAction(living_room))
    remote.press_undo()