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
    def __init__(self, power_source):
        self.power_source = power_source
    
    def power_on(self):
        if hasattr(self.power_source, 'voltage') and self.power_source.voltage() == 110:
            return f"Device powered on with {self.power_source.voltage()}V"
        else:
            raise ValueError("Incompatible voltage - device requires 110V")

class PowerConverter:
    def __init__(self, european_socket):
        self._socket = european_socket
    
    def voltage(self):
        return 110
    
    def live(self):
        return self._socket.live() * 0.5
    
    def neutral(self):
        return self._socket.neutral() * 0.5

class SafetyMonitor:
    def __init__(self, converter):
        self.converter = converter
    
    def check_safety(self):
        if hasattr(self.converter, '_socket'):
            earth_value = self.converter._socket.earth()
            return earth_value == 0
        return False

if __name__ == "__main__":
    eu_socket = EuropeanSocket()
    print(f"European socket: {eu_socket.voltage()}V")
    
    converter = PowerConverter(eu_socket)
    print(f"Converted voltage: {converter.voltage()}V")
    
    american_device = AmericanElectronics(converter)
    result = american_device.power_on()
    print(result)
    
    safety = SafetyMonitor(converter)
    is_safe = safety.check_safety()
    print(f"Safety check: {'Passed' if is_safe else 'Failed'}")