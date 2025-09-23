from abc import ABC, abstractmethod

class Computer:
    def __init__(self):
        self.cpu = None
        self.gpu = None
        self.ram_gb = 0
        self.storages = []
        self.psu = None
        self.prices = {}

    def total_price(self):
        return sum(self.prices.values())

    def summary(self):
        return {
            "cpu": self.cpu,
            "gpu": self.gpu,
            "ram_gb": self.ram_gb,
            "storages": list(self.storages),
            "psu": self.psu,
            "total_price": self.total_price(),
        }

class ConfiguratorBase(ABC):
    def __init__(self):
        self._computer = Computer()

    @abstractmethod
    def set_cpu(self, model: str):
        pass

    @abstractmethod
    def set_gpu(self, model: str):
        pass

    @abstractmethod
    def set_ram(self, gb: int):
        pass

    @abstractmethod
    def add_storage(self, kind: str, size_gb: int, price: float):
        pass

    @abstractmethod
    def set_power(self, model: str, price: float):
        pass

    def get_result(self) -> Computer:
        c = self._computer
        if not c.cpu or not c.ram_gb or not c.psu:
            raise ValueError("Configuration incomplete: cpu, ram, and psu are required")
        return c

class GamingConfig(ConfiguratorBase):
    def set_cpu(self, model: str):
        self._computer.cpu = model
        self._computer.prices['cpu'] = 400.0
        return self

    def set_gpu(self, model: str):
        self._computer.gpu = model
        self._computer.prices['gpu'] = 700.0
        return self

    def set_ram(self, gb: int):
        if gb % 8 != 0:
            raise ValueError("Gaming RAM must be a multiple of 8GB")
        self._computer.ram_gb = gb
        self._computer.prices['ram'] = 50.0 * (gb // 8)
        return self

    def add_storage(self, kind: str, size_gb: int, price: float):
        self._computer.storages.append({"type": kind, "size_gb": size_gb})
        self._computer.prices[f"storage_{len(self._computer.storages)}"] = price
        return self

    def set_power(self, model: str, price: float):
        self._computer.psu = model
        self._computer.prices['psu'] = price
        return self

class OfficeConfig(ConfiguratorBase):
    def set_cpu(self, model: str):
        self._computer.cpu = model
        self._computer.prices['cpu'] = 150.0
        return self

    def set_gpu(self, model: str):
        self._computer.gpu = model
        self._computer.prices['gpu'] = 0.0
        return self

    def set_ram(self, gb: int):
        if gb < 4:
            raise ValueError("Office RAM must be at least 4GB")
        self._computer.ram_gb = gb
        self._computer.prices['ram'] = 25.0 * (gb // 4)
        return self

    def add_storage(self, kind: str, size_gb: int, price: float):
        self._computer.storages.append({"type": kind, "size_gb": size_gb})
        self._computer.prices[f"storage_{len(self._computer.storages)}"] = price
        return self

    def set_power(self, model: str, price: float):
        self._computer.psu = model
        self._computer.prices['psu'] = price
        return self

class Assembler:
    def __init__(self, configurator: ConfiguratorBase):
        self.configurator = configurator

    def assemble_high_end(self):
        self.configurator.set_cpu("Ryzen 9 7950X").set_gpu("RTX 4090").set_ram(32)
        self.configurator.add_storage("NVMe", 2000, 250.0)
        self.configurator.set_power("1000W Gold", 180.0)
        return self.configurator.get_result()

    def assemble_budget(self):
        self.configurator.set_cpu("Intel i3").set_gpu("Integrated").set_ram(8)
        self.configurator.add_storage("SATA SSD", 500, 50.0)
        self.configurator.set_power("450W Bronze", 40.0)
        return self.configurator.get_result()

if __name__ == "__main__":
    gaming = GamingConfig()
    assembler = Assembler(gaming)
    pc1 = assembler.assemble_high_end()
    print(pc1.summary())

    office = OfficeConfig()
    assembler2 = Assembler(office)
    pc2 = assembler2.assemble_budget()
    print(pc2.summary())

    custom = GamingConfig()
    custom.set_cpu("Ryzen 7 7700X").set_ram(16).add_storage("NVMe", 1000, 120.0).set_power("750W Gold", 120.0)
    print(custom.get_result().summary())