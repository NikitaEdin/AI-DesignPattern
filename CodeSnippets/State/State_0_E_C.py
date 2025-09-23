class On:
    def press(self, context):
        print("Turning off")
        context.current = Off()

class Off:
    def press(self, context):
        print("Turning on")
        context.current = On()

class Switch:
    def __init__(self):
        self.current = Off()
    
    def press_button(self):
        self.current.press(self)

if __name__ == "__main__":
    switch = Switch()
    switch.press_button()
    switch.press_button()
    switch.press_button()