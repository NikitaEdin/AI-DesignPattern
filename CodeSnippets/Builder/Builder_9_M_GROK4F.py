class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None

    def __str__(self):
        return f"Computer(CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, GPU: {self.gpu})"

class ComputerConfigurator:
    def __init__(self):
        self._computer = Computer()

    def set_cpu(self, cpu):
        if not isinstance(cpu, str) or len(cpu) == 0:
            raise ValueError("CPU must be a non-empty string")
        self._computer.cpu = cpu
        return self

    def set_ram(self, ram):
        if not isinstance(ram, str) or len(ram) == 0:
            raise ValueError("RAM must be a non-empty string")
        self._computer.ram = ram
        return self

    def set_storage(self, storage):
        if not isinstance(storage, str) or len(storage) == 0:
            raise ValueError("Storage must be a non-empty string")
        self._computer.storage = storage
        return self

    def set_gpu(self, gpu):
        if not isinstance(gpu, str) or len(gpu) == 0:
            raise ValueError("GPU must be a non-empty string")
        self._computer.gpu = gpu
        return self

    def create(self):
        if not all([self._computer.cpu, self._computer.ram, self._computer.storage]):
            raise ValueError("Computer must have CPU, RAM, and storage specified")
        return self._computer

class ComputerFactory:
    def __init__(self, configurator):
        self._configurator = configurator

    def assemble_gaming_rig(self):
        return (self._configurator
                .set_cpu("Intel i9")
                .set_ram("32GB")
                .set_storage("1TB SSD")
                .set_gpu("NVIDIA RTX 4080")
                .create())

    def assemble_office_machine(self):
        return (self._configurator
                .set_cpu("AMD Ryzen 5")
                .set_ram("16GB")
                .set_storage("512GB SSD")
                .create())

if __name__ == "__main__":
    factory = ComputerFactory(ComputerConfigurator())
    gaming_pc = factory.assemble_gaming_rig()
    print(gaming_pc)

    office_pc = factory.assemble_office_machine()
    print(office_pc)