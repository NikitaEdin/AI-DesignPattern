class On:
    def press(self, switch):
        print("Light is turning OFF")
        switch.current = switch.off

class Off:
    def press(self, switch):
        print("Light is turning ON")
        switch.current = switch.on

class Switch:
    def __init__(self):
        self.on = On()
        self.off = Off()
        self.current = self.off
    
    def press(self):
        self.current.press(self)

if __name__ == "__main__":
    switch = Switch()
    switch.press()
    switch.press()
    switch.press()