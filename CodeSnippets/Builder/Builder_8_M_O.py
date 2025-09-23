from abc import ABC, abstractmethod

class Computer:
    def __init__(self):
        self.cpu = None
        self.memory_gb = None
        self.storage_gb = None
        self.gpu = None
        self.os = None

    def summary(self):
        return (
            f"CPU: {self.cpu}, Memory: {self.memory_gb}GB, Storage: {self.storage_gb}GB, "
            f"GPU: {self.gpu or 'None'}, OS: {self.os}"
        )

class AssemblerGateway(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def add_cpu(self, model: str):
        pass

    @abstractmethod
    def add_memory(self, gb: int):
        pass

    @abstractmethod
    def add_storage(self, gb: int):
        pass

    @abstractmethod
    def add_gpu(self, model: str):
        pass

    @abstractmethod
    def install_os(self, name: str):
        pass

    @abstractmethod
    def get_product(self) -> Computer:
        pass

class GamingAssembler(AssemblerGateway):
    def __init__(self):
        self.reset()

    def reset(self):
        self._pc = Computer()

    def add_cpu(self, model: str):
        if not model:
            raise ValueError("CPU model required")
        self._pc.cpu = model

    def add_memory(self, gb: int):
        if gb <= 0:
            raise ValueError("Memory must be positive")
        self._pc.memory_gb = gb

    def add_storage(self, gb: int):
        if gb <= 0:
            raise ValueError("Storage must be positive")
        self._pc.storage_gb = gb

    def add_gpu(self, model: str):
        if not model:
            raise ValueError("GPU model required for gaming systems")
        self._pc.gpu = model

    def install_os(self, name: str):
        if not name:
            raise ValueError("OS name required")
        self._pc.os = name

    def get_product(self) -> Computer:
        missing = [k for k in ("cpu","memory_gb","storage_gb","os") if getattr(self._pc, k) is None]
        if missing:
            raise ValueError(f"Incomplete configuration, missing: {missing}")
        result = self._pc
        self.reset()
        return result

class OfficeAssembler(AssemblerGateway):
    def __init__(self):
        self.reset()

    def reset(self):
        self._pc = Computer()

    def add_cpu(self, model: str):
        if not model:
            raise ValueError("CPU model required")
        self._pc.cpu = model

    def add_memory(self, gb: int):
        if gb <= 0:
            raise ValueError("Memory must be positive")
        self._pc.memory_gb = gb

    def add_storage(self, gb: int):
        if gb <= 0:
            raise ValueError("Storage must be positive")
        self._pc.storage_gb = gb

    def add_gpu(self, model: str):
        self._pc.gpu = model or "Integrated"

    def install_os(self, name: str):
        if not name:
            raise ValueError("OS name required")
        self._pc.os = name

    def get_product(self) -> Computer:
        if self._pc.cpu is None or self._pc.memory_gb is None or self._pc.storage_gb is None or self._pc.os is None:
            raise ValueError("Incomplete configuration for office system")
        result = self._pc
        self.reset()
        return result

class ConfigurationDirector:
    def high_end_gaming(self, assembler: AssemblerGateway):
        assembler.add_cpu("AMD Ryzen 9 7950X")
        assembler.add_memory(64)
        assembler.add_storage(2000)
        assembler.add_gpu("NVIDIA RTX 4090")
        assembler.install_os("Windows 11 Pro")

    def compact_office(self, assembler: AssemblerGateway):
        assembler.add_cpu("Intel Core i5")
        assembler.add_memory(16)
        assembler.add_storage(512)
        assembler.add_gpu(None)
        assembler.install_os("Windows 11 Home")

if __name__ == "__main__":
    director = ConfigurationDirector()
    gamer = GamingAssembler()
    office = OfficeAssembler()

    director.high_end_gaming(gamer)
    gaming_pc = gamer.get_product()
    print("Gaming PC:", gaming_pc.summary())

    director.compact_office(office)
    office_pc = office.get_product()
    print("Office PC:", office_pc.summary())

    custom = GamingAssembler()
    try:
        custom.add_cpu("Intel Core i7")
        custom.add_memory(32)
        # intentionally omit storage to show error handling
        custom.install_os("Ubuntu 22.04")
        pc = custom.get_product()
        print("Custom PC:", pc.summary())
    except ValueError as e:
        print("Configuration error:", e)