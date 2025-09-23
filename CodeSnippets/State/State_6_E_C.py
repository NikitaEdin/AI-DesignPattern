class On:
    def press(self, context):
        print("Turning off")
        context.mode = Off()

class Off:
    def press(self, context):
        print("Turning on")
        context.mode = On()

class Switch:
    def __init__(self):
        self.mode = Off()
    
    def press(self):
        self.mode.press(self)

if __name__ == "__main__":
    switch = Switch()
    switch.press()
    switch.press()
    switch.press()