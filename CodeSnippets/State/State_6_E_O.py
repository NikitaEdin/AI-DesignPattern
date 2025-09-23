class ModeBase:
    def handle(self, context): raise NotImplementedError
class OffMode(ModeBase):
    def handle(self, context):
        print("Device is now ON")
        context.set_mode(OnMode())
class OnMode(ModeBase):
    def handle(self, context):
        print("Device is now OFF")
        context.set_mode(OffMode())
class Device:
    def __init__(self, mode): self.current_mode = mode
    def set_mode(self, mode): self.current_mode = mode
    def press(self): self.current_mode.handle(self)
if __name__ == '__main__':
    device = Device(OffMode())
    device.press()
    device.press()
    device.press()