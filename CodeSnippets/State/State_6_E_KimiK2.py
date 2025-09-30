class Mode:
    def handle(self, ctx): pass

class On(Mode):
    def handle(self, ctx):
        print("On")
        ctx.mode = Off()

class Off(Mode):
    def handle(self, ctx):
        print("Off")
        ctx.mode = On()

class Device:
    def __init__(self):
        self.mode = Off()
    def trigger(self):
        self.mode.handle(self)

if __name__ == "__main__":
    d = Device()
    for _ in range(4):
        d.trigger()