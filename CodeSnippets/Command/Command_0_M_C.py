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

class TurnOnLight(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class TurnOffLight(Action):
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
    
    def undo_last(self):
        if self.history:
            last_action = self.history.pop()
            last_action.undo()
        else:
            print("No actions to undo")

if __name__ == "__main__":
    living_room_light = Light("Living Room")
    kitchen_light = Light("Kitchen")
    
    remote = RemoteControl()
    
    turn_on_living_room = TurnOnLight(living_room_light)
    turn_off_kitchen = TurnOffLight(kitchen_light)
    
    remote.press_button(turn_on_living_room)
    remote.press_button(turn_off_kitchen)
    
    remote.undo_last()
    remote.undo_last()