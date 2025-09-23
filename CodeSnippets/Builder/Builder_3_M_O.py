from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class Computer:
    cpu: str = ""
    ram: str = ""
    storage: str = ""
    gpu: str = ""
    os: str = ""
    extras: dict = field(default_factory=dict)

    def description(self) -> str:
        parts = [
            f"CPU: {self.cpu}",
            f"RAM: {self.ram}",
            f"Storage: {self.storage}",
            f"GPU: {self.gpu or 'Integrated'}",
            f"OS: {self.os}"
        ]
        if self.extras:
            parts.append("Extras: " + ", ".join(f"{k}={v}" for k, v in self.extras.items()))
        return " | ".join(parts)

class ConfiguratorInterface(ABC):
    @abstractmethod
    def reset(self): ...
    @abstractmethod
    def set_cpu(self, value: str): ...
    @abstractmethod
    def set_ram(self, value: str): ...
    @abstractmethod
    def set_storage(self, value: str): ...
    @abstractmethod
    def set_gpu(self, value: str): ...
    @abstractmethod
    def set_os(self, value: str): ...
    @abstractmethod
    def get_product(self) -> Computer: ...

class ComputerConfigurator(ConfiguratorInterface):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Computer()
        return self

    def set_cpu(self, value: str):
        if not value:
            raise ValueError("CPU specification cannot be empty")
        self._product.cpu = value
        return self

    def set_ram(self, value: str):
        self._product.ram = value
        return self

    def set_storage(self, value: str):
        self._product.storage = value
        return self

    def set_gpu(self, value: str):
        self._product.gpu = value
        return self

    def set_os(self, value: str):
        self._product.os = value
        return self

    def add_extra(self, key: str, value):
        if not key:
            raise ValueError("Extra item must have a key")
        self._product.extras[key] = value
        return self

    def get_product(self) -> Computer:
        missing = [f for f in ("cpu", "ram", "storage", "os") if not getattr(self._product, f)]
        if missing:
            raise RuntimeError(f"Incomplete configuration, missing: {', '.join(missing)}")
        product = self._product
        self.reset()
        return product

class Coordinator:
    def __init__(self, configurator: ConfiguratorInterface):
        self.configurator = configurator

    def assemble_office_machine(self):
        self.configurator.reset()\
            .set_cpu("Intel i5")\
            .set_ram("16GB")\
            .set_storage("512GB SSD")\
            .set_os("Linux")

    def assemble_gaming_rig(self):
        self.configurator.reset()\
            .set_cpu("Intel i9")\
            .set_ram("32GB")\
            .set_storage("2TB NVMe")\
            .set_gpu("NVIDIA RTX 4080")\
            .set_os("Windows 11")

if __name__ == "__main__":
    configurator = ComputerConfigurator()
    manager = Coordinator(configurator)

    manager.assemble_gaming_rig()
    gaming_pc = configurator.get_product()
    print("Gaming PC:", gaming_pc.description())

    # Custom build using fluent API
    custom_pc = configurator.reset()\
        .set_cpu("AMD Ryzen 7")\
        .set_ram("32GB")\
        .set_storage("1TB SSD")\
        .set_os("Windows 11")\
        .add_extra("Cooling", "Liquid")\
        .get_product()
    print("Custom PC:", custom_pc.description())

    # Demonstrate error handling for incomplete config
    try:
        configurator.reset().set_cpu("TinyCPU").get_product()
    except RuntimeError as e:
        print("Error:", e)