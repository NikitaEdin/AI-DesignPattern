class On:
    def press(self, switch):
        print("Light is now OFF")
        switch.current = Off()

class Off:
    def press(self, switch):
        print("Light is now ON")
        switch.current = On()

class LightSwitch:
    def __init__(self):
        self.current = Off()
    
    def press(self):
        self.current.press(self)

if __name__ == "__main__":
    switch = LightSwitch()
    switch.press()
    switch.press()
    switch.press()