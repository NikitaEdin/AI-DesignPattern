class Mode:
    def handle(self, context): pass

class On(Mode):
    def handle(self, context):
        print("On")
        context.mode = Off()

class Off(Mode):
    def handle(self, context):
        print("Off")
        context.mode = On()

class Switch:
    def __init__(self):
        self.mode = Off()
    def press(self):
        self.mode.handle(self)

if __name__ == "__main__":
    s = Switch()
    [s.press() for _ in range(3)]