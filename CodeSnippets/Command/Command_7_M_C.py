class LightBulb:
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print("Light is now ON")
        else:
            print("Light is already ON")
    
    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print("Light is now OFF")
        else:
            print("Light is already OFF")

class Action:
    def execute(self):
        raise NotImplementedError
    
    def undo(self):
        raise NotImplementedError

class TurnOnAction(Action):
    def __init__(self, device):
        self.device = device
    
    def execute(self):
        self.device.turn_on()
    
    def undo(self):
        self.device.turn_off()

class TurnOffAction(Action):
    def __init__(self, device):
        self.device = device
    
    def execute(self):
        self.device.turn_off()
    
    def undo(self):
        self.device.turn_on()

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
    bulb = LightBulb()
    remote = RemoteControl()
    
    on_action = TurnOnAction(bulb)
    off_action = TurnOffAction(bulb)
    
    remote.press_button(on_action)
    remote.press_button(off_action)
    remote.undo_last()
    remote.undo_last()
    remote.undo_last()