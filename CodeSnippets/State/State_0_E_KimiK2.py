class Mode:
    def handle(self, context): pass

class On(Mode):
    def handle(self, context):
        print("Light is on")
        context.current = Off()

class Off(Mode):
    def handle(self, context):
        print("Light is off")
        context.current = On()

class Light:
    def __init__(self):
        self.current = Off()
    def toggle(self):
        self.current.handle(self)

if __name__ == "__main__":
    l = Light()
    [l.toggle() for _ in range(4)]