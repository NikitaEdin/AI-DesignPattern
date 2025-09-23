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

class TurnOnAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class TurnOffAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()

class RemoteControl:
    def __init__(self):
        self.actions = []
        self.current_position = -1
    
    def execute_action(self, action):
        if self.current_position < len(self.actions) - 1:
            self.actions = self.actions[:self.current_position + 1]
        self.actions.append(action)
        action.execute()
        self.current_position += 1
    
    def undo_last(self):
        if self.current_position >= 0:
            self.actions[self.current_position].undo()
            self.current_position -= 1
        else:
            print("Nothing to undo")

if __name__ == "__main__":
    living_room_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    
    remote = RemoteControl()
    
    remote.execute_action(TurnOnAction(living_room_light))
    remote.execute_action(TurnOnAction(bedroom_light))
    remote.execute_action(TurnOffAction(living_room_light))
    
    print("Undoing last action:")
    remote.undo_last()
    
    print("Undoing another action:")
    remote.undo_last()