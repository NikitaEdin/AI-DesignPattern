from abc import ABC, abstractmethod

class PowerInterface(ABC):
    @abstractmethod
    def supply_power(self, device_name: str, power_level: int) -> bool:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

class UsbPowerBank(PowerInterface):
    def supply_power(self, device_name: str, power_level: int) -> bool:
        if power_level > 18:
            print(f"Limited power for {device_name}: max 18W")
            return False
        print(f"Supplying {power_level}W to {device_name} via USB power bank.")
        return True

    def get_status(self) -> str:
        return "Power bank active, 80% charge"

class IndustrialPowerGrid:
    def deliver_industrial_power(self, device_name: str, voltage: float) -> bool:
        print(f"Delivering {voltage}V industrial power to {device_name}.")
        return True

class PowerConverter(PowerInterface):
    def __init__(self, grid: IndustrialPowerGrid, conversion_rate: float = 44.0):
        self.grid = grid
        self.conversion_rate = conversion_rate
        self._is_connected = True
        self.max_power = 100

    def supply_power(self, device_name: str, power_level: int) -> bool:
        if not self._is_connected:
            print("Power converter not connected.")
            return False
        if power_level > self.max_power:
            print(f"Power level {power_level}W exceeds converter limit {self.max_power}W")
            return False
        try:
            voltage = power_level * 5 / 3 * self.conversion_rate
            success = self.grid.deliver_industrial_power(device_name, voltage)
            if success:
                print(f"Converted to {power_level}W for {device_name}.")
            return success
        except Exception as e:
            print(f"Conversion failed: {e}")
            return False

    def get_status(self) -> str:
        return "Power converter operational" if self._is_connected else "Disconnected"

    def disconnect(self):
        self._is_connected = False

class Laptop:
    def __init__(self, power_source: PowerInterface):
        self.power_source = power_source

    def power_on(self, power_needed: int = 30):
        status = self.power_source.get_status()
        print(f"Laptop status check: {status}")
        success = self.power_source.supply_power("Laptop", power_needed)
        if success:
            print("Laptop powered on successfully.")
        else:
            print("Failed to power on laptop.")

if __name__ == "__main__":
    power_bank = UsbPowerBank()
    laptop1 = Laptop(power_bank)
    laptop1.power_on(10)
    laptop1.power_on(25)

    grid = IndustrialPowerGrid()
    converter = PowerConverter(grid)
    laptop2 = Laptop(converter)
    laptop2.power_on(15)
    converter.disconnect()
    laptop2.power_on(15)
    converter = PowerConverter(grid)
    laptop2 = Laptop(converter)
    laptop2.power_on(120)