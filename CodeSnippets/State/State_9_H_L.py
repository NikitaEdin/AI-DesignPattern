class Machine:
    def __init__(self):
        self.state = "off"
    
    def turn_on(self):
        if self.state == "off":
            self.state = "on"
            print("The machine has been turned on.")
        
    def turn_off(self):
        if self.state == "on":
            self.state = "off"
            print("The machine has been turned off.")
            
class OnState:
    def __init__(self, context):
        self.context = context
        
    def handle(self, event):
        if event == "turn_on":
            return "on"
        elif event == "turn_off":
            return "off"
    
class OffState:
    def __init__(self, context):
        self.context = context
        
    def handle(self, event):
        if event == "turn_on":
            return "on"
        elif event == "turn_off":
            return "off"