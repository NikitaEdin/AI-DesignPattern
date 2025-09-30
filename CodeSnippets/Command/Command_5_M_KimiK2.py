class LightBulb:
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print("Light is ON")
    
    def turn_off(self):
        self.is_on = False
        print("Light is OFF")

class SwitchAction:
    def execute(self):
        pass
    
    def undo(self):
        pass

class TurnOnAction(SwitchAction):
    def __init__(self, bulb):
        self.bulb = bulb
    
    def execute(self):
        self.bulb.turn_on()
    
    def undo(self):
        self.bulb.turn_off()

class TurnOffAction(SwitchAction):
    def __init__(self, bulb):
        self.bulb = bulb
    
    def execute(self):
        self.bulb.turn_off()
    
    def undo(self):
        self.bulb.turn_on()

class Switch:
    def __init__(self):
        self.history = []
    
    def perform(self, action):
        action.execute()
        self.history.append(action)
    
    def undo_last(self):
        if self.history:
            action = self.history.pop()
            action.undo()

if __name__ == "__main__":
    bulb = LightBulb()
    switch = Switch()
    
    on_action = TurnOnAction(bulb)
    off_action = TurnOffAction(bulb)
    
    switch.perform(on_action)
    switch.perform(off_action)
    switch.undo_last()
    switch.undo_last()