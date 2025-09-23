from abc import ABC, abstractmethod

class Computer:
    def __init__(self):
        self.cpu = None
        self.ram_gb = None
        self.storage_gb = None
        self.gpu = None

    def __str__(self):
        return (f"Computer Specs:\n"
                f"  CPU: {self.cpu}\n"
                f"  RAM: {self.ram_gb} GB\n"
                f"  Storage: {self.storage_gb} GB\n"
                f"  GPU: {self.gpu}")

class ComputerPreparer(ABC):
    def __init__(self):
        self._computer = Computer()

    @abstractmethod
    def prepare_cpu(self):
        pass

    @abstractmethod
    def prepare_ram(self):
        pass

    @abstractmethod
    def prepare_storage(self):
        pass

    @abstractmethod
    def prepare_gpu(self):
        pass

    def get_computer(self):
        return self._computer

    def customize_ram(self, ram_gb):
        if not isinstance(ram_gb, int) or ram_gb < 1:
            raise ValueError("RAM must be a positive integer")
        self._computer.ram_gb = ram_gb
        return self

class GamingPreparer(ComputerPreparer):
    def prepare_cpu(self):
        self._computer.cpu = "Intel Core i9-13900K"

    def prepare_ram(self):
        self._computer.ram_gb = 32

    def prepare_storage(self):
        self._computer.storage_gb = 2000

    def prepare_gpu(self):
        self._computer.gpu = "NVIDIA GeForce RTX 4090"

class OfficePreparer(ComputerPreparer):
    def prepare_cpu(self):
        self._computer.cpu = "Intel Core i5-13400"

    def prepare_ram(self):
        self._computer.ram_gb = 16

    def prepare_storage(self):
        self._computer.storage_gb = 512

    def prepare_gpu(self):
        self._computer.gpu = "Integrated Graphics"

class ComputerCoordinator:
    def __init__(self, preparer):
        self._preparer = preparer

    def construct_gaming_rig(self):
        self._preparer.prepare_cpu()
        self._preparer.prepare_ram()
        self._preparer.prepare_storage()
        self._preparer.prepare_gpu()

    def construct_office_setup(self):
        self._preparer.prepare_cpu()
        self._preparer.prepare_ram()
        self._preparer.prepare_storage()
        self._preparer.prepare_gpu()

if __name__ == "__main__":
    gaming_preparer = GamingPreparer()
    coordinator = ComputerCoordinator(gaming_preparer)
    coordinator.construct_gaming_rig()
    gaming_preparer.customize_ram(64)
    print(gaming_preparer.get_computer())

    office_preparer = OfficePreparer()
    coordinator = ComputerCoordinator(office_preparer)
    coordinator.construct_office_setup()
    print(office_preparer.get_computer())