class Mode:
    def handle(self, context):
        pass

class On(Mode):
    def handle(self, context):
        print("On mode")
        context.mode = Off()

class Off(Mode):
    def handle(self, context):
        print("Off mode")
        context.mode = On()

class Device:
    def __init__(self):
        self.mode = On()
    def toggle(self):
        self.mode.handle(self)

if __name__ == "__main__":
    d = Device()
    d.toggle()
    d.toggle()