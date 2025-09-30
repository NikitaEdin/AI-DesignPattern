class Mode:
    def handle(self, ctx): pass

class On(Mode):
    def handle(self, ctx):
        print("Light is on")
        ctx.mode = Off()

class Off(Mode):
    def handle(self, ctx):
        print("Light is off")
        ctx.mode = On()

class Switch:
    def __init__(self):
        self.mode = Off()
    def press(self):
        self.mode.handle(self)

if __name__ == "__main__":
    s = Switch()
    for _ in range(3):
        s.press()