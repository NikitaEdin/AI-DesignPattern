class Context:
    def __init__(self):
        self.mode = OffMode(self)
    
    def set_mode(self, mode):
        self.mode = mode
    
    def press_button(self):
        self.mode.handle()

class OffMode:
    def __init__(self, context):
        self.context = context
    
    def handle(self):
        print("Turning on")
        self.context.set_mode(OnMode(self.context))

class OnMode:
    def __init__(self, context):
        self.context = context
    
    def handle(self):
        print("Turning off")
        self.context.set_mode(OffMode(self.context))

if __name__ == "__main__":
    device = Context()
    device.press_button()
    device.press_button()
    device.press_button()