class Device:
    def __init__(self):
        self.mode = OffMode()
        self.status = "Off"

    def toggle(self):
        self.mode = self.mode.toggle(self)

    def display(self):
        print(self.status)

class OffMode:
    def toggle(self, device):
        device.status = "Low"
        return LowMode()

class LowMode:
    def toggle(self, device):
        device.status = "High"
        return HighMode()

class HighMode:
    def toggle(self, device):
        device.status = "Off"
        return OffMode()

if __name__ == "__main__":
    d = Device()
    d.display()
    d.toggle()
    d.display()
    d.toggle()
    d.display()
    d.toggle()
    d.display()