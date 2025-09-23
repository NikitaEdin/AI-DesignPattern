from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def power_on(self, device):
        pass
    
    @abstractmethod
    def power_off(self, device):
        pass
    
    @abstractmethod
    def get_status(self):
        pass

class OffMode(Mode):
    def power_on(self, device):
        print("Device powering on...")
        device.set_mode(OnMode())
    
    def power_off(self, device):
        print("Device is already off")
    
    def get_status(self):
        return "OFF"

class OnMode(Mode):
    def power_on(self, device):
        print("Device is already on")
    
    def power_off(self, device):
        print("Device powering off...")
        device.set_mode(OffMode())
    
    def get_status(self):
        return "ON"

class Device:
    def __init__(self):
        self._current_mode = OffMode()
        self._power_cycles = 0
    
    def set_mode(self, mode):
        if mode.__class__ != self._current_mode.__class__:
            self._power_cycles += 1
        self._current_mode = mode
    
    def press_power(self):
        if self._current_mode.get_status() == "OFF":
            self._current_mode.power_on(self)
        else:
            self._current_mode.power_off(self)
    
    def get_status(self):
        return self._current_mode.get_status()
    
    def get_power_cycles(self):
        return self._power_cycles

if __name__ == "__main__":
    device = Device()
    
    print(f"Initial status: {device.get_status()}")
    device.press_power()
    print(f"Current status: {device.get_status()}")
    device.press_power()
    print(f"Final status: {device.get_status()}")
    print(f"Power cycles: {device.get_power_cycles()}")