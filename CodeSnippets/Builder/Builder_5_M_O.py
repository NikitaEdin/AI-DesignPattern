from abc import ABC, abstractmethod

class ComputerSystem:
    def __init__(self):
        self.cpu = None
        self.ram_gb = None
        self.storage_gb = None
        self.gpu = None
        self.os = None

    def summary(self):
        return {
            "CPU": self.cpu,
            "RAM(GB)": self.ram_gb,
            "Storage(GB)": self.storage_gb,
            "GPU": self.gpu,
            "OS": self.os,
        }

class Configurator(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def set_cpu(self, cpu: str):
        pass

    @abstractmethod
    def set_ram(self, gb: int):
        pass

    @abstractmethod
    def set_storage(self, gb: int):
        pass

    @abstractmethod
    def set_gpu(self, gpu: str):
        pass

    @abstractmethod
    def set_os(self, os_name: str):
        pass

    @abstractmethod
    def finalize(self) -> ComputerSystem:
        pass

class GamingConfigurator(Configurator):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = ComputerSystem()
        return self

    def set_cpu(self, cpu: str):
        self._product.cpu = cpu
        return self

    def set_ram(self, gb: int):
        self._product.ram_gb = gb
        return self

    def set_storage(self, gb: int):
        self._product.storage_gb = gb
        return self

    def set_gpu(self, gpu: str):
        self._product.gpu = gpu
        return self

    def set_os(self, os_name: str):
        self._product.os = os_name
        return self

    def finalize(self) -> ComputerSystem:
        if not self._product.cpu or not self._product.ram_gb:
            raise ValueError("Essential components missing: CPU and RAM are required.")
        result = self._product
        self.reset()
        return result

class OfficeConfigurator(Configurator):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = ComputerSystem()
        return self

    def set_cpu(self, cpu: str):
        self._product.cpu = cpu
        return self

    def set_ram(self, gb: int):
        self._product.ram_gb = gb
        return self

    def set_storage(self, gb: int):
        self._product.storage_gb = gb
        return self

    def set_gpu(self, gpu: str):
        self._product.gpu = gpu
        return self

    def set_os(self, os_name: str):
        self._product.os = os_name
        return self

    def finalize(self) -> ComputerSystem:
        if not self._product.cpu or not self._product.ram_gb:
            raise ValueError("Essential components missing: CPU and RAM are required.")
        if not self._product.storage_gb:
            self._product.storage_gb = 256
        result = self._product
        self.reset()
        return result

class AssemblyCoordinator:
    def __init__(self, configurator: Configurator):
        self.configurator = configurator

    def assemble_high_end_gaming(self) -> ComputerSystem:
        return (
            self.configurator
            .set_cpu("Ryzen 9 7950X")
            .set_ram(32)
            .set_storage(2000)
            .set_gpu("NVIDIA RTX 4090")
            .set_os("Windows 11")
            .finalize()
        )

    def assemble_standard_office(self) -> ComputerSystem:
        return (
            self.configurator
            .set_cpu("Intel i5")
            .set_ram(8)
            .set_storage(512)
            .set_os("Windows 11 Pro")
            .finalize()
        )

if __name__ == "__main__":
    gamer = GamingConfigurator()
    office = OfficeConfigurator()

    coordinator = AssemblyCoordinator(gamer)
    try:
        gaming_pc = coordinator.assemble_high_end_gaming()
        print("Gaming PC:", gaming_pc.summary())
    except ValueError as e:
        print("Error assembling gaming PC:", e)

    coordinator.configurator = office
    try:
        workstation = coordinator.assemble_standard_office()
        print("Office PC:", workstation.summary())
    except ValueError as e:
        print("Error assembling office PC:", e)