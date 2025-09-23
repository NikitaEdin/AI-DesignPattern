class Context:
    def __init__(self):
        self.current = OffMode(self)
    
    def press_button(self):
        self.current.handle()
    
    def change_to(self, mode):
        self.current = mode

class OffMode:
    def __init__(self, context):
        self.context = context
    
    def handle(self):
        print("Turning on")
        self.context.change_to(OnMode(self.context))

class OnMode:
    def __init__(self, context):
        self.context = context
    
    def handle(self):
        print("Turning off")
        self.context.change_to(OffMode(self.context))

if __name__ == "__main__":
    device = Context()
    device.press_button()
    device.press_button()
    device.press_button()