from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class Light:
    def __init__(self, location):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} light is ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} light is OFF")

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
    
    def press_button(self, action):
        try:
            action.execute()
            self.history.append(action)
        except Exception as e:
            print(f"Error executing action: {e}")
    
    def press_undo(self):
        if self.history:
            last_action = self.history.pop()
            last_action.undo()

if __name__ == "__main__":
    living_room_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    
    remote = RemoteControl()
    
    remote.press_button(LightOnAction(living_room_light))
    remote.press_button(LightOnAction(bedroom_light))
    remote.press_button(LightOffAction(living_room_light))
    
    remote.press_undo()
    remote.press_undo()