class ModeBase:
    def do(self, device):
        raise NotImplementedError

class ModeA(ModeBase):
    def do(self, device):
        print("ModeA: working, switching to ModeB")
        device.set_mode(ModeB())

class ModeB(ModeBase):
    def do(self, device):
        print("ModeB: working, switching to ModeA")
        device.set_mode(ModeA())

class Device:
    def __init__(self, initial):
        self.current = initial
    def set_mode(self, m):
        self.current = m
    def request(self):
        self.current.do(self)

if __name__ == "__main__":
    d = Device(ModeA())
    d.request()
    d.request()
    d.request()