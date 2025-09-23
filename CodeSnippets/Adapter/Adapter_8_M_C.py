class EuropeanSocket:
    def __init__(self):
        self.voltage = 230
        self.frequency = 50
    
    def get_power(self):
        return {"live": 1, "neutral": -1, "earth": 0, "voltage": self.voltage}

class AmericanDevice:
    def __init__(self, name):
        self.name = name
        self.required_voltage = 120
        self.is_on = False
    
    def power_on(self, live, neutral, voltage):
        if voltage != self.required_voltage:
            raise ValueError(f"Voltage mismatch: expected {self.required_voltage}V, got {voltage}V")
        if live == 1 and neutral == -1:
            self.is_on = True
            return f"{self.name} is now ON"
        raise ValueError("Invalid power connection")

class VoltageConverter:
    def __init__(self, european_socket):
        self.socket = european_socket
        self.conversion_ratio = 230 / 120
    
    def get_converted_power(self):
        power = self.socket.get_power()
        converted_voltage = int(power["voltage"] / self.conversion_ratio)
        converted_live = power["live"]
        converted_neutral = power["neutral"]
        return {
            "live": converted_live,
            "neutral": converted_neutral,
            "voltage": converted_voltage
        }

class PowerManager:
    def __init__(self):
        self.devices = []
    
    def connect_device(self, device, power_source):
        try:
            power = power_source.get_converted_power()
            result = device.power_on(power["live"], power["neutral"], power["voltage"])
            self.devices.append(device)
            return result
        except ValueError as e:
            return f"Connection failed: {e}"

if __name__ == "__main__":
    european_outlet = EuropeanSocket()
    american_laptop = AmericanDevice("Gaming Laptop")
    voltage_bridge = VoltageConverter(european_outlet)
    manager = PowerManager()
    
    print(f"European socket provides: {european_outlet.get_power()['voltage']}V")
    print(f"American device requires: {american_laptop.required_voltage}V")
    print(f"Converter output: {voltage_bridge.get_converted_power()['voltage']}V")
    
    result = manager.connect_device(american_laptop, voltage_bridge)
    print(result)
    print(f"Device status: {'Connected' if american_laptop.is_on else 'Disconnected'}")