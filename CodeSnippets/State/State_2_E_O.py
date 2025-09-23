class Mode:
    def handle(self, device): raise NotImplementedError
class OffMode(Mode):
    def handle(self, device):
        print("Device is off. Switching on.")
        device.set_mode(OnMode())
class OnMode(Mode):
    def handle(self, device):
        print("Device is on. Switching off.")
        device.set_mode(OffMode())
class Device:
    def __init__(self, mode): self._mode = mode
    def set_mode(self, mode): self._mode = mode
    def request(self): self._mode.handle(self)
if __name__ == "__main__":
    d = Device(OffMode())
    d.request(); d.request(); d.request()