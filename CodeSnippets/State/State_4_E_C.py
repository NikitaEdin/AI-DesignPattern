class Off:
    def press(self, context):
        context.mode = On()
        return "Turning on"

class On:
    def press(self, context):
        context.mode = Off()
        return "Turning off"

class Switch:
    def __init__(self):
        self.mode = Off()
    
    def press_button(self):
        return self.mode.press(self)

if __name__ == "__main__":
    switch = Switch()
    print(switch.press_button())
    print(switch.press_button())
    print(switch.press_button())