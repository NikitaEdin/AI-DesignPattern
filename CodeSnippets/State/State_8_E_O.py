class ModeBase:
    def handle(self, context):
        raise NotImplementedError
class ModeA(ModeBase):
    def handle(self, context):
        print("Operating in Mode A")
        context.change_mode(ModeB())
class ModeB(ModeBase):
    def handle(self, context):
        print("Operating in Mode B")
        context.change_mode(ModeA())
class Context:
    def __init__(self, mode):
        self.current = mode
    def request(self):
        self.current.handle(self)
    def change_mode(self, mode):
        self.current = mode
if __name__ == "__main__":
    device = Context(ModeA())
    for _ in range(4):
        device.request()