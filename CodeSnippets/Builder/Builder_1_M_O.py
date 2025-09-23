from abc import ABC, abstractmethod

class Device:
    def __init__(self, cpu=None, memory=0, storage=0, os_name=None):
        self.cpu = cpu
        self.memory = memory
        self.storage = storage
        self.os = os_name

    def __repr__(self):
        return f"Device(cpu={self.cpu!r}, memory={self.memory}GB, storage={self.storage}GB, os={self.os!r})"

class Assembler(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def add_cpu(self, cpu: str):
        pass

    @abstractmethod
    def add_memory(self, gb: int):
        pass

    @abstractmethod
    def add_storage(self, gb: int):
        pass

    @abstractmethod
    def install_os(self, os_name: str):
        pass

    @abstractmethod
    def retrieve_device(self) -> Device:
        pass

class PCAssembler(Assembler):
    def __init__(self):
        self.reset()

    def reset(self):
        self._device = Device()

    def add_cpu(self, cpu: str):
        if not cpu or not isinstance(cpu, str):
            raise ValueError("CPU must be a non-empty string")
        self._device.cpu = cpu

    def add_memory(self, gb: int):
        if not isinstance(gb, int) or gb <= 0:
            raise ValueError("Memory must be a positive integer (GB)")
        self._device.memory = gb

    def add_storage(self, gb: int):
        if not isinstance(gb, int) or gb <= 0:
            raise ValueError("Storage must be a positive integer (GB)")
        self._device.storage = gb

    def install_os(self, os_name: str):
        if not os_name or not isinstance(os_name, str):
            raise ValueError("OS name must be a non-empty string")
        self._device.os = os_name

    def retrieve_device(self) -> Device:
        if not self._device.cpu or self._device.memory <= 0:
            raise ValueError("Incomplete device configuration: CPU and memory are required")
        result = self._device
        self.reset()
        return result

    def run_quality_check(self) -> bool:
        cpu = (self._device.cpu or "").lower()
        if "i9" in cpu:
            return self._device.memory >= 32
        return True

class Orchestrator:
    def __init__(self, assembler: Assembler):
        self.assembler = assembler

    def assemble_minimal_system(self) -> Device:
        self.assembler.reset()
        self.assembler.add_cpu("Intel i3")
        self.assembler.add_memory(8)
        self.assembler.add_storage(256)
        self.assembler.install_os("Linux")
        return self.assembler.retrieve_device()

    def assemble_high_performance_system(self, quality_check: bool = False) -> Device:
        self.assembler.reset()
        self.assembler.add_cpu("Intel i9")
        self.assembler.add_memory(32)
        self.assembler.add_storage(2000)
        self.assembler.install_os("Windows 11")
        if quality_check and hasattr(self.assembler, "run_quality_check"):
            if not self.assembler.run_quality_check():
                raise RuntimeError("Quality check failed for high performance system")
        return self.assembler.retrieve_device()

if __name__ == "__main__":
    assembler = PCAssembler()
    director = Orchestrator(assembler)
    basic = director.assemble_minimal_system()
    print(basic)
    try:
        gaming = director.assemble_high_performance_system(quality_check=True)
        print(gaming)
    except Exception as e:
        print("Error:", e)