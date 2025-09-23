from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def change(self, device):
        pass

class OffMode(Mode):
    def __init__(self, device):
        self.device = device

    def change(self, device):
        device.current_mode = OnMode(device)
        print("Device is now on.")

class OnMode(Mode):
    def __init__(self, device):
        self.device = device

    def change(self, device):
        device.current_mode = OffMode(device)
        print("Device is now off.")

class Device:
    def __init__(self):
        self.current_mode = OffMode(self)

    def toggle(self):
        self.current_mode.change(self)

if __name__ == "__main__":
    device = Device()
    print("Initial: off")
    device.toggle()
    device.toggle()
    device.toggle()