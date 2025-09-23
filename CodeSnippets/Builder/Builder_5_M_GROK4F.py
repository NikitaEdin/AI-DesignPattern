from abc import ABC, abstractmethod

class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None

    def __str__(self):
        return f"Computer: CPU={self.cpu}, RAM={self.ram}, Storage={self.storage}, GPU={self.gpu}"

class ComputerConfigurator(ABC):
    def __init__(self):
        self.computer = Computer()

    @abstractmethod
    def configure_cpu(self):
        pass

    @abstractmethod
    def configure_ram(self):
        pass

    @abstractmethod
    def configure_storage(self):
        pass

    @abstractmethod
    def configure_gpu(self):
        pass

    def retrieve_computer(self):
        if not all([self.computer.cpu, self.computer.ram, self.computer.storage, self.computer.gpu]):
            raise ValueError("All components must be configured before retrieving the computer.")
        return self.computer

class GamingComputerConfigurator(ComputerConfigurator):
    def configure_cpu(self):
        self.computer.cpu = "Intel Core i9"

    def configure_ram(self):
        self.computer.ram = "32GB DDR5"

    def configure_storage(self):
        self.computer.storage = "2TB NVMe SSD"

    def configure_gpu(self):
        self.computer.gpu = "NVIDIA RTX 4080"

class OfficeComputerConfigurator(ComputerConfigurator):
    def configure_cpu(self):
        self.computer.cpu = "Intel Core i5"

    def configure_ram(self):
        self.computer.ram = "16GB DDR4"

    def configure_storage(self):
        self.computer.storage = "512GB SSD"

    def configure_gpu(self):
        self.computer.gpu = "Integrated Graphics"

class AssemblyCoordinator:
    def __init__(self, configurator):
        self.configurator = configurator

    def assemble(self):
        self.configurator.configure_cpu()
        self.configurator.configure_ram()
        self.configurator.configure_storage()
        self.configurator.configure_gpu()

if __name__ == "__main__":
    gaming_config = GamingComputerConfigurator()
    coordinator = AssemblyCoordinator(gaming_config)
    coordinator.assemble()
    gaming_pc = gaming_config.retrieve_computer()
    print(f"Gaming PC: {gaming_pc}")

    office_config = OfficeComputerConfigurator()
    coordinator = AssemblyCoordinator(office_config)
    coordinator.assemble()
    office_pc = office_config.retrieve_computer()
    print(f"Office PC: {office_pc}")