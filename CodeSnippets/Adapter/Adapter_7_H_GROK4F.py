import logging
from abc import ABC, abstractmethod
from typing import Optional

class PowerOutlet(ABC):
    @abstractmethod
    def connect_device(self, device_name: str, power_watts: int) -> bool:
        pass

class StandardOutlet(PowerOutlet):
    def connect_device(self, device_name: str, power_watts: int) -> bool:
        if power_watts > 1500:
            raise ValueError("Exceeds standard outlet capacity")
        print(f"Standard outlet powering {device_name} with {power_watts}W")
        return True

class IndustrialSocket:
    def energize_machine(self, voltage: int) -> bool:
        max_watts = 5000
        if voltage != 220:
            logging.warning("Voltage mismatch for industrial socket")
            return False
        print(f"Industrial socket energizing at 220V, capacity up to {max_watts}W")
        return True

class VoltageTransformer:
    def __init__(self, supported_voltages: set = None):
        self.supported_voltages = supported_voltages or {110, 220}

    def transform_to(self, target_voltage: int) -> bool:
        if target_voltage not in self.supported_voltages:
            logging.error(f"Unsupported voltage: {target_voltage}")
            return False
        print(f"Transforming voltage to {target_voltage}V")
        return True

class IndustrialConnector(PowerOutlet):
    def __init__(self, socket: IndustrialSocket, transformer: Optional[VoltageTransformer] = None):
        self.socket = socket
        self.transformer = transformer or VoltageTransformer()

    def connect_device(self, device_name: str, power_watts: int) -> bool:
        try:
            if power_watts > 5000:
                raise ValueError("Exceeds industrial socket capacity")
            if power_watts <= 0:
                raise ValueError("Invalid power requirement")
            if not self.transformer.transform_to(110):
                return False
            return self.socket.energize_machine(220)
        except ValueError as e:
            logging.error(f"Connection error for {device_name}: {e}")
            return False

def main():
    standard = StandardOutlet()
    success = standard.connect_device("Laptop", 60)
    print(f"Laptop connection: {success}")

    socket = IndustrialSocket()
    connector = IndustrialConnector(socket)
    success = connector.connect_device("Machinery", 4000)
    print(f"Machinery connection: {success}")

    try:
        connector.connect_device("Overload Device", 6000)
    except ValueError as e:
        print(f"Overload handled: {e}")

    bad_transformer = VoltageTransformer({220})
    bad_connector = IndustrialConnector(socket, bad_transformer)
    success = bad_connector.connect_device("Incompatible Device", 100)
    print(f"Incompatible device connection: {success}")

    invalid_power = connector.connect_device("Invalid Device", -10)
    print(f"Invalid power connection: {invalid_power}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()