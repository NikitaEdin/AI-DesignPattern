class EuropeanSocket:
    def voltage(self):
        return 230
    
    def live(self):
        return 1
    
    def neutral(self):
        return -1
    
    def earth(self):
        return 0

class AmericanElectronics:
    def __init__(self, voltage):
        self.voltage = voltage
    
    def power_on(self):
        if self.voltage > 120:
            raise ValueError("Voltage too high! Device damaged.")
        return f"American device running on {self.voltage}V"

class VoltageConverter:
    def __init__(self, european_socket):
        self._socket = european_socket
        self._conversion_ratio = 0.52
    
    def voltage(self):
        return int(self._socket.voltage() * self._conversion_ratio)
    
    def live(self):
        return self._socket.live()
    
    def neutral(self):
        return self._socket.neutral()

def charge_device(power_source, device):
    try:
        voltage = power_source.voltage()
        device.voltage = voltage
        return device.power_on()
    except ValueError as e:
        return f"Error: {e}"

if __name__ == "__main__":
    eu_socket = EuropeanSocket()
    us_device = AmericanElectronics(0)
    
    print("Direct connection:")
    result = charge_device(eu_socket, us_device)
    print(result)
    
    print("\nWith converter:")
    converter = VoltageConverter(eu_socket)
    result = charge_device(converter, us_device)
    print(result)