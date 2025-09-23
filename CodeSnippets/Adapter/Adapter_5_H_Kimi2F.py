from abc import ABC, abstractmethod
import functools
import threading

class EuropeanSocket(ABC):
    @abstractmethod
    def supply_230v(self): ...

class USASocket(ABC):
    @abstractmethod
    def supply_120v(self): ...

class GermanOutlet(EuropeanSocket):
    def supply_230v(self):
        return "230V AC"

class AmericanOutlet(USASocket):
    def supply_120v(self):
        return "120V AC"

class PowerLink:
    def __init__(self, socket: EuropeanSocket):
        self.socket = socket

    def use(self):
        return f"Device running on {self.socket.supply_230v()}"

class VoltageBridge(EuropeanSocket):
    _lock = threading.Lock()
    _instances = {}

    def __new__(cls, usa_socket: USASocket):
        with cls._lock:
            key = id(usa_socket)
            if key not in cls._instances:
                cls._instances[key] = super().__new__(cls)
                cls._instances[key]._initialized = False
            return cls._instances[key]

    def __init__(self, usa_socket: USASocket):
        if self._initialized: return
        self.usa_socket = usa_socket
        self._initialized = True

    def supply_230v(self):
        return self.usa_socket.supply_120v().replace("120V", "230V (converted)")

def main():
    outlet_de = GermanOutlet()
    device = PowerLink(outlet_de)
    print(device.use())

    outlet_us = AmericanOutlet()
    bridge = VoltageBridge(outlet_us)
    device = PowerLink(bridge)
    print(device.use())

    bridge2 = VoltageBridge(outlet_us)
    print(bridge is bridge2)

if __name__ == "__main__":
    main()