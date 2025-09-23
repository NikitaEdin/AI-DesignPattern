from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class Light:
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        return "Light is ON"
    
    def turn_off(self):
        self.is_on = False
        return "Light is OFF"

class TurnOnAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        return self.light.turn_on()
    
    def undo(self):
        return self.light.turn_off()

class TurnOffAction(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        return self.light.turn_off()
    
    def undo(self):
        return self.light.turn_on()

class RemoteControl:
    def __init__(self):
        self.history = []
    
    def press_button(self, action):
        try:
            result = action.execute()
            self.history.append(action)
            return result
        except Exception as e:
            return f"Error: {e}"
    
    def undo_last(self):
        if self.history:
            last_action = self.history.pop()
            return last_action.undo()
        return "No actions to undo"

if __name__ == "__main__":
    light = Light()
    remote = RemoteControl()
    
    turn_on = TurnOnAction(light)
    turn_off = TurnOffAction(light)
    
    print(remote.press_button(turn_on))
    print(remote.press_button(turn_off))
    print(remote.undo_last())
    print(remote.undo_last())