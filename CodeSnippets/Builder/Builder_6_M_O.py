from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Computer:
    cpu: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    gpu: Optional[str] = None
    os: Optional[str] = None

    def summary(self) -> str:
        return (
            f"CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, "
            f"GPU: {self.gpu or 'None'}, OS: {self.os or 'None'}"
        )


class AssemblerProtocol(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def set_cpu(self, spec: str) -> None:
        pass

    @abstractmethod
    def set_ram(self, spec: str) -> None:
        pass

    @abstractmethod
    def set_storage(self, spec: str) -> None:
        pass

    @abstractmethod
    def set_gpu(self, spec: str) -> None:
        pass

    @abstractmethod
    def set_os(self, spec: str) -> None:
        pass

    @abstractmethod
    def get_product(self) -> Computer:
        pass


class ComputerAssembler(AssemblerProtocol):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = Computer()

    def set_cpu(self, spec: str) -> None:
        if not spec:
            raise ValueError("CPU specification cannot be empty")
        self._product.cpu = spec

    def set_ram(self, spec: str) -> None:
        if not spec:
            raise ValueError("RAM specification cannot be empty")
        self._product.ram = spec

    def set_storage(self, spec: str) -> None:
        if not spec:
            raise ValueError("Storage specification cannot be empty")
        self._product.storage = spec

    def set_gpu(self, spec: str) -> None:
        self._product.gpu = spec or None

    def set_os(self, spec: str) -> None:
        self._product.os = spec or None

    def get_product(self) -> Computer:
        if not (self._product.cpu and self._product.ram and self._product.storage):
            raise ValueError("Incomplete configuration: CPU, RAM, and Storage are required")
        product = self._product
        self.reset()
        return product


class Coordinator:
    def prepare_gaming_system(self, assembler: AssemblerProtocol) -> None:
        assembler.reset()
        assembler.set_cpu("Intel i9-13900K")
        assembler.set_ram("32GB DDR5")
        assembler.set_storage("2TB NVMe")
        assembler.set_gpu("NVIDIA RTX 4090")
        assembler.set_os("Windows 11 Pro")

    def prepare_office_system(self, assembler: AssemblerProtocol) -> None:
        assembler.reset()
        assembler.set_cpu("Intel i5-13400")
        assembler.set_ram("16GB DDR4")
        assembler.set_storage("512GB SSD")
        assembler.set_gpu("")  # no dedicated GPU
        assembler.set_os("Ubuntu 24.04 LTS")

    def prepare_minimal_system(self, assembler: AssemblerProtocol, cpu: str, ram: str, storage: str) -> None:
        assembler.reset()
        assembler.set_cpu(cpu)
        assembler.set_ram(ram)
        assembler.set_storage(storage)


if __name__ == "__main__":
    coordinator = Coordinator()
    assembler = ComputerAssembler()

    try:
        coordinator.prepare_gaming_system(assembler)
        gaming_pc = assembler.get_product()
        print("Gaming PC:", gaming_pc.summary())

        coordinator.prepare_office_system(assembler)
        office_pc = assembler.get_product()
        print("Office PC:", office_pc.summary())

        coordinator.prepare_minimal_system(assembler, cpu="AMD Ryzen 5 7600", ram="8GB DDR4", storage="256GB SSD")
        tiny_pc = assembler.get_product()
        print("Minimal PC:", tiny_pc.summary())

        assembler.reset()
        assembler.set_cpu("")  # trigger error
        assembler.set_ram("4GB")
        assembler.set_storage("128GB")
        incomplete = assembler.get_product()
        print(incomplete.summary())
    except ValueError as exc:
        print("Configuration error:", exc)