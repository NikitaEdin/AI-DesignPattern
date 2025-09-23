class On:
    def press(self, switch):
        print("Turning off")
        switch.current = Off()

class Off:
    def press(self, switch):
        print("Turning on")
        switch.current = On()

class Switch:
    def __init__(self):
        self.current = Off()
    
    def press(self):
        self.current.press(self)

if __name__ == "__main__":
    switch = Switch()
    switch.press()
    switch.press()
    switch.press()